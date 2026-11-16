import { describe, expect, it, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import GuestAiChatbot from '@/components/AiChatbot/GuestAiChatbot.vue'

vi.stubGlobal('__', (text: string) => text)

const { callMocks } = vi.hoisted(() => ({
	callMocks: vi.fn(),
}))

vi.mock('frappe-ui', () => ({
	call: (...args: unknown[]) => callMocks(...args),
}))

describe('GuestAiChatbot component', () => {
	beforeEach(() => {
		callMocks.mockReset()
		try {
			localStorage.clear()
		} catch {}
	})

	it('renders floating trigger button initially', () => {
		const wrapper = mount(GuestAiChatbot, { global: { mocks: { __: (text: string) => text }, stubs: { RouterLink: true } } })
		const btn = wrapper.find('button[aria-label="Mở trợ lý tư vấn khóa học"]')
		expect(btn.exists()).toBe(true)
		expect(wrapper.find('[role="dialog"]').exists()).toBe(false)
	})

	it('opens chat dialog on clicking floating button', async () => {
		const wrapper = mount(GuestAiChatbot, { global: { mocks: { __: (text: string) => text }, stubs: { RouterLink: true } } })
		const btn = wrapper.find('button[aria-label="Mở trợ lý tư vấn khóa học"]')
		await btn.trigger('click')

		expect(wrapper.find('[role="dialog"]').exists()).toBe(true)
		expect(wrapper.text()).toContain('Ai Coaching Vietnam')
		expect(wrapper.text()).toContain('Trợ lý tư vấn khóa học')
		expect(wrapper.find('.guest-chat-profile img').exists()).toBe(true)
	})

	it('sends user message and displays AI reply', async () => {
		callMocks.mockResolvedValueOnce({
			response: 'Lộ trình Giám đốc Tài chính CFO gồm 4 học phần chuyên sâu.',
			status: 'success',
		})

		const wrapper = mount(GuestAiChatbot, { global: { mocks: { __: (text: string) => text }, stubs: { RouterLink: true } } })
		await wrapper.find('button[aria-label="Mở trợ lý tư vấn khóa học"]').trigger('click')

		const input = wrapper.find('input[type="text"]')
		await input.setValue('Tư vấn khóa CFO')
		await wrapper.find('form').trigger('submit')

		expect(callMocks).toHaveBeenCalledWith('lms.lms.ai_coach.guest_ai_chat', {
			message: 'Tư vấn khóa CFO',
		})

		await flushPromises()

		expect(wrapper.text()).toContain('Tư vấn khóa CFO')
		expect(wrapper.text()).toContain('Lộ trình Giám đốc Tài chính CFO gồm 4 học phần chuyên sâu.')
	})

	it('shows a catalog link when the assistant is unavailable', async () => {
		callMocks.mockResolvedValueOnce({ status: 'unavailable', response: 'Trợ lý tư vấn hiện tạm thời không khả dụng.' })
		const wrapper = mount(GuestAiChatbot, { global: { mocks: { __: (text: string) => text }, stubs: { RouterLink: { props: ['to'], template: '<a><slot /></a>' } } } })
		await wrapper.find('button[aria-label="Mở trợ lý tư vấn khóa học"]').trigger('click')
		await wrapper.find('input[type="text"]').setValue('Tư vấn khóa học')
		await wrapper.find('form').trigger('submit')
		await flushPromises()
		expect(wrapper.text()).toContain('tạm thời không khả dụng')
		expect(wrapper.find('.guest-chat-catalog').text()).toBe('Xem khóa học')
	})

	it('shows message markup as text rather than injecting HTML', async () => {
		callMocks.mockResolvedValueOnce({ response: '<img src=x onerror=alert(1)> **Lưu ý**' })
		const wrapper = mount(GuestAiChatbot, { global: { mocks: { __: (text: string) => text }, stubs: { RouterLink: true } } })
		await wrapper.find('button[aria-label="Mở trợ lý tư vấn khóa học"]').trigger('click')
		await wrapper.find('input[type="text"]').setValue('<script>bad</script>')
		await wrapper.find('form').trigger('submit')
		await flushPromises()
		expect(wrapper.find('.guest-chat-messages img').exists()).toBe(false)
		expect(wrapper.find('.guest-chat-messages script').exists()).toBe(false)
		expect(wrapper.findAll('.guest-chat-messages strong').map((item) => item.text())).toContain('Lưu ý')
	})

	it('supports clicking a quick prompt to send message', async () => {
		callMocks.mockResolvedValueOnce({
			response: 'Thanh toán VietQR qua PayOS được xác nhận tự động trong 3-5 giây.',
			status: 'success',
		})

		const wrapper = mount(GuestAiChatbot, { global: { mocks: { __: (text: string) => text }, stubs: { RouterLink: true } } })
		await wrapper.find('button[aria-label="Mở trợ lý tư vấn khóa học"]').trigger('click')

		const quickBtn = wrapper.findAll('button').find((b) => b.text().includes('Các khóa học về kế toán'))
		expect(quickBtn?.exists()).toBe(true)
		await quickBtn!.trigger('click')

		await flushPromises()

		expect(callMocks).toHaveBeenCalled()
		expect(wrapper.text()).toContain('Thanh toán VietQR qua PayOS được xác nhận tự động trong 3-5 giây.')
	})
})
