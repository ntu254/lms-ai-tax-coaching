import { describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import LearnerCourseCard from '@/components/Courses/LearnerCourseCard.vue'

vi.mock('@/utils', () => ({ formatRating: (value: number) => String(value) }))
const mountCard = (course: Record<string, unknown>) => mount(LearnerCourseCard, {
	props: { course, to: { name: 'CourseDetail', params: { courseName: 'course-1' } } },
	global: { mocks: { __: (text: string) => text }, stubs: { RouterLink: { name: 'RouterLink', props: ['to'], template: '<a><slot /></a>' } } },
})
describe('learner course card', () => {
	it('shows the published course details and no rating when none exists', () => {
		const wrapper = mountCard({ title: 'Kế toán cơ bản', category: 'Kế toán', instructors: [{ full_name: 'Nguyễn An' }], rating: 0, paid_course: 1, price: '850.000 ₫' })
		expect(wrapper.text()).toContain('Kế toán cơ bản')
		expect(wrapper.text()).toContain('Nguyễn An')
		expect(wrapper.text()).toContain('Chưa có đánh giá')
		expect(wrapper.text()).toContain('850.000 ₫')
		expect(wrapper.findComponent({ name: 'RouterLink' }).props('to')).toEqual({ name: 'CourseDetail', params: { courseName: 'course-1' } })
	})
	it('shows free courses and learner progress', () => {
		const wrapper = mountCard({ title: 'Thuế cơ bản', rating: 4, paid_course: 0, membership: { progress: 42 } })
		expect(wrapper.text()).toContain('Miễn phí')
		expect(wrapper.text()).toContain('42%')
		expect(wrapper.text()).toContain('★ 4')
	})
	it('does not label a course as free when its pricing is unavailable', () => {
		const wrapper = mountCard({ title: 'Khóa học' })
		expect(wrapper.text()).not.toContain('Miễn phí')
	})
})

