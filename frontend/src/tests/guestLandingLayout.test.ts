import { beforeEach, describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'

const { state } = vi.hoisted(() => ({
	state: { loggedIn: false, mobile: false, route: 'Home', user: null as any },
}))

vi.mock('frappe-ui', () => ({ FrappeUIProvider: { template: '<div><slot /></div>' } }))
vi.mock('vue-router', () => ({
	useRoute: () => ({ name: state.route, path: '/', fullPath: '/', query: {}, matched: [] }),
	useRouter: () => ({}),
}))
vi.mock('@/stores/session', () => ({ sessionStore: () => ({ isLoggedIn: state.loggedIn }) }))
vi.mock('@/stores/user', () => ({ usersStore: () => ({ userResource: { data: state.user } }) }))
vi.mock('@/stores/settings', () => ({ useSettings: () => ({ settings: { data: {} } }) }))
vi.mock('@/utils/composables', () => ({ useScreenSize: () => ({ isMobile: ref(state.mobile) }) }))
vi.mock('@/composables/useFormRoute', () => ({ formBackgroundPath: () => null }))
vi.mock('@/composables/dialogLayering', () => ({ useDialogLayering: () => {} }))
vi.mock('@/utils/dialogs', () => ({ Dialogs: { template: '<div />' } }))
vi.mock('@/utils/onboarding', () => ({ seesOnboarding: () => false }))
vi.mock('@framework/ui/components/Onboarding/index', () => ({ showHelpModal: ref(false) }))
vi.mock('@/components/Layouts/pages/desktop/DesktopLayout.vue', () => ({
	default: { props: ['learner'], template: '<div data-testid="desktop" :data-learner="learner || false"><slot /></div>' },
}))
vi.mock('@/components/Layouts/pages/mobile/MobileLayout.vue', () => ({
	default: { props: ['learner'], template: '<div data-testid="mobile" :data-learner="learner || false"><slot /></div>' },
}))
vi.mock('@/components/Layouts/pages/desktop/NoSidebarLayout.vue', () => ({
	default: { template: '<div data-testid="no-sidebar"><slot /></div>' },
}))
vi.mock('@/components/Layouts/pages/PublicCourseLayout.vue', () => ({
	default: { template: '<div data-testid="public-courses"><slot /></div>' },
}))
vi.mock('@/components/InstallPrompt.vue', () => ({ default: { template: '<div />' } }))
vi.mock('@/components/Notifications/NotificationPanel.vue', () => ({ default: { template: '<div />' } }))
vi.mock('@/components/ContinueCoursePanel.vue', () => ({ default: { template: '<div />' } }))

import App from '@/App.vue'

describe('guest landing layout', () => {
	beforeEach(() => {
		state.loggedIn = false
		state.mobile = false
		state.route = 'Home'
		state.user = null
	})

	it.each([false, true])('uses the sidebar-free layout on mobile=%s', (mobile) => {
		state.mobile = mobile
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.find('[data-testid="no-sidebar"]').exists()).toBe(true)
		expect(wrapper.find('[data-testid="desktop"]').exists()).toBe(false)
		expect(wrapper.find('[data-testid="mobile"]').exists()).toBe(false)
	})

	it.each([false, true])('shows the component showcase without a sidebar when loggedIn=%s', (loggedIn) => {
		state.loggedIn = loggedIn
		state.route = 'ComponentShowcase'
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.find('[data-testid="no-sidebar"]').exists()).toBe(true)
	})

	it('keeps the desktop app layout for signed-in users', () => {
		state.loggedIn = true
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.find('[data-testid="desktop"]').exists()).toBe(true)
	})

	it.each(['Billing'])('uses the public layout for guest %s', (route) => {
		state.route = route
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.find('[data-testid="public-courses"]').exists()).toBe(true)
	})

	it.each(['Courses', 'CourseDetail', 'Batches', 'BatchDetail', 'Programs', 'ProgramDetail'])('uses the original app layout for guest %s', (route) => {
		state.route = route
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.find('[data-testid="desktop"]').exists()).toBe(true)
	})

	it('keeps the app layout for signed-in course pages', () => {
		state.loggedIn = true
		state.route = 'Courses'
		state.user = { is_student: true }
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.get('[data-testid="desktop"]').attributes('data-learner')).toBe('false')
	})

	it.each([false, true])('enables learner styling for students on mobile=%s', (mobile) => {
		state.loggedIn = true
		state.mobile = mobile
		state.user = { is_student: true, is_system_manager: false }
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.get(`[data-testid="${mobile ? 'mobile' : 'desktop'}"]`).attributes('data-learner')).toBe('true')
	})

	it.each(['is_instructor', 'is_moderator', 'is_evaluator', 'is_system_manager'])('keeps staff styling for %s', (role) => {
		state.loggedIn = true
		state.user = { is_student: true, [role]: true }
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.get('[data-testid="desktop"]').attributes('data-learner')).toBe('false')
	})

	it('keeps the mobile app layout on other guest pages', () => {
		state.mobile = true
		state.route = 'Profile'
		const wrapper = mount(App, { global: { stubs: ['router-view'] } })
		expect(wrapper.find('[data-testid="mobile"]').exists()).toBe(true)
	})
})
