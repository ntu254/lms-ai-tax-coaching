import { describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'

const { session } = vi.hoisted(() => ({ session: { isLoggedIn: false } }))
vi.mock('pinia', () => ({ storeToRefs: () => ({ isLoggedIn: ref(session.isLoggedIn) }) }))
vi.mock('@/stores/session', () => ({ sessionStore: () => session }))
vi.mock('@/pages/Home/GuestHome.vue', () => ({ default: { template: '<div>Guest home</div>' } }))
vi.mock('@/pages/Home/Home.vue', () => ({ default: { template: '<div>Member home</div>' } }))

import HomeEntry from '@/pages/Home/HomeEntry.vue'

describe('home entry', () => {
	it('shows the guest introduction when signed out', () => {
		session.isLoggedIn = false
		expect(mount(HomeEntry).text()).toBe('Guest home')
	})

	it('keeps the existing home for signed-in users', () => {
		session.isLoggedIn = true
		expect(mount(HomeEntry).text()).toBe('Member home')
	})
})
