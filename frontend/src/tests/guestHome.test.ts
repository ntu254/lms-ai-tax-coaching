import { beforeEach, describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'

const { push, list } = vi.hoisted(() => ({
	push: vi.fn(),
	list: { data: [] as any[], list: { loading: false, error: null as any } },
}))

vi.mock('vue-router', () => ({ useRouter: () => ({ push }) }))
vi.mock('@/stores/session', () => ({ sessionStore: () => ({ brand: { name: 'Ai Coaching Vietnam' } }) }))
vi.mock('frappe-ui', () => ({
	Button: { template: '<button><slot /></button>' },
	FormControl: {
		props: ['modelValue'],
		emits: ['update:modelValue'],
		template: '<input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
	},
	createListResource: () => list,
	usePageMeta: vi.fn(),
}))
vi.mock('@/components/CourseCard.vue', () => ({
	default: { props: ['course', 'to'], template: '<div>{{ course.title }}</div>' },
}))

import GuestHome from '@/pages/Home/GuestHome.vue'

describe('guest home', () => {
	beforeEach(() => {
		push.mockReset()
		list.data = []
		list.list.loading = false
		list.list.error = null
	})

	function render() {
		return mount(GuestHome, {
			global: {
				mocks: { __: (text: string) => text },
				stubs: { RouterLink: { name: 'RouterLink', props: ['to'], template: '<a><slot /></a>' } },
			},
		})
	}

	it('scrolls to training fields when opened from another public page', async () => {
		const scrollIntoView = vi.fn()
		const getById = vi.spyOn(document, 'getElementById').mockReturnValue({ scrollIntoView } as unknown as HTMLElement)
		window.history.replaceState({}, '', '/lms/#guest-topics-title')
		const wrapper = render()
		await wrapper.vm.$nextTick()
		expect(getById).toHaveBeenCalledWith('guest-topics-title')
		expect(scrollIntoView).toHaveBeenCalled()
		getById.mockRestore()
		window.history.replaceState({}, '', '/lms/')
	})

	it('passes a search to the existing course catalog', async () => {
		const wrapper = render()
		await wrapper.get('input').setValue('  kế toán  ')
		await wrapper.get('form').trigger('submit')
		expect(push).toHaveBeenCalledWith({ name: 'Courses', query: { title: 'kế toán' } })
	})

	it('opens the catalog with the selected field as a search term', () => {
		const wrapper = render()
		const topic = wrapper.findAllComponents({ name: 'RouterLink' }).find((link) => link.text() === 'Kế toán')
		expect(topic?.props('to')).toEqual({ name: 'Courses', query: { title: 'Kế toán' } })
	})

	it('introduces the company and its training fields', () => {
		const text = render().text()
		expect(text).toContain('Ai Coaching Vietnam')
		expect(text).toContain('Kế toán, Kiểm toán, Thuế, Tài chính, Nhân sự')
		expect(text).toContain('Quản trị doanh nghiệp')
	})

	it('provides working course and class links in the closing call to action and footer', () => {
		const wrapper = render()
		const ctaLinks = wrapper.get('.guest-cta').findAllComponents({ name: 'RouterLink' })
		expect(ctaLinks.map((link) => link.props('to'))).toEqual([{ name: 'Courses' }, { name: 'Batches' }])
		const footer = wrapper.get('footer')
		expect(footer.get('a[href="/login"]').text()).toBe('Đăng nhập')
		expect(footer.findAllComponents({ name: 'RouterLink' }).map((link) => link.props('to'))).toContainEqual({ name: 'Courses' })
	})

	it('renders real courses returned by the catalog', () => {
		list.data = [{ name: 'course-1', title: 'Khóa học mẫu' }]
		expect(render().text()).toContain('Khóa học mẫu')
	})

	it('shows featured courses ahead of the rest when any are available', () => {
		list.data = [
			{ name: 'featured', title: 'Nổi bật', featured: 1 },
			{ name: 'other', title: 'Khóa khác', featured: 0 },
		]
		const wrapper = render()
		expect(wrapper.text()).toContain('Khóa học nổi bật')
		expect(wrapper.text()).toContain('Nổi bật')
		expect(wrapper.text()).not.toContain('Khóa khác')
	})

	it('distinguishes a failed request from an empty catalog', () => {
		list.list.error = new Error('offline')
		expect(render().get('[role="alert"]').text()).toContain('Không thể tải')
	})
})

