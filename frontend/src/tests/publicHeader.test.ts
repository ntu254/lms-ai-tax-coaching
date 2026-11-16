import { describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import PublicHeader from '@/components/Public/PublicHeader.vue'

vi.mock('@/stores/session', () => ({ sessionStore: () => ({ brand: { name: 'Ai Coaching Vietnam' } }) }))
const render = (active: string) => mount(PublicHeader, {
	props: { active },
	global: { mocks: { __: (text: string) => text }, stubs: { RouterLink: { name: 'RouterLink', props: ['to'], template: '<a><slot /></a>' } } },
})
describe('public header', () => {
	it.each(['home', 'courses'])('uses the same navigation on %s', (active) => {
		const wrapper = render(active)
		expect(wrapper.findAll('.site-links a')).toHaveLength(4)
		expect(wrapper.get('.site-brand img').attributes('alt')).toBe('Ai Coaching Vietnam')
		expect(wrapper.get('.site-login').attributes('href')).toBe('/login')
		expect(wrapper.get('.site-links .is-active').text()).toBe(active === 'home' ? 'Trang chủ' : 'Khóa học')
		expect(wrapper.findAll('.site-links a')[3].attributes('href')).toBe(active === 'home' ? '#guest-topics-title' : '/lms/#guest-topics-title')
	})
})
