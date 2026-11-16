import { describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'

vi.mock('frappe-ui', () => ({
	Avatar: {
		props: ['label', 'image', 'size'],
		template: '<div><slot name="indicator" /></div>',
	},
}))

import UserAvatar from '@/components/UserAvatar.vue'

describe('UserAvatar', () => {
	it.each(['Work', 'Hiring'])('does not display the retired %s badge', (openTo) => {
		const wrapper = mount(UserAvatar, {
			props: { user: { full_name: 'A', open_to: openTo } as any, size: '2xl' },
		})
		expect(wrapper.text()).not.toMatch(/work|hiring/i)
		expect(wrapper.find('.lucide-briefcase').exists()).toBe(false)
		expect(wrapper.find('.lucide-badge-check').exists()).toBe(false)
	})
})
