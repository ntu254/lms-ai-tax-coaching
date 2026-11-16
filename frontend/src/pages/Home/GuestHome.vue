<template>
	<div class="guest-home">
		<PublicHeader active="home" />
		<main>
			<section class="guest-hero" aria-labelledby="guest-hero-title">
				<div class="guest-container guest-hero-grid">
					<div class="guest-hero-copy">
						<div class="guest-hero-label"><span>{{ __('Ai Coaching Vietnam') }}</span>{{ __('Học tập và phát triển chuyên môn') }}</div>
						<h1 id="guest-hero-title">{{ __('Khám phá kiến thức') }}<br />{{ __('nâng tầm') }} <em>{{ __('chuyên môn') }}</em></h1>
						<p>{{ __('Đào tạo Kế toán, Kiểm toán, Thuế, Tài chính, Nhân sự và Quản trị doanh nghiệp.') }}</p>
						<div class="guest-hero-actions">
							<router-link :to="{ name: 'Courses' }" class="guest-primary">{{ __('Khám phá khóa học') }}</router-link>
							<router-link :to="{ name: 'Batches' }" class="guest-secondary">{{ __('Xem lớp học') }}</router-link>
						</div>
						<form class="guest-search" @submit.prevent="searchCourses">
							<FormControl v-model="search" type="search" class="guest-search-field" :placeholder="__('Bạn muốn học gì?')" :aria-label="__('Tìm khóa học')" />
							<Button type="submit" variant="solid" class="guest-search-btn">{{ __('Tìm kiếm') }}</Button>
						</form>
					</div>
					<div class="guest-hero-visual">
						<div class="guest-visual-orbit" aria-hidden="true"></div>
						<div class="guest-visual-card">
							<img :src="safeUrl(learningImage)" :alt="__('Học tập cùng AI Coaching Vietnam')" />
							<div class="guest-visual-content">
								<span>{{ __('Khám phá khóa học') }}</span>
								<strong>{{ visibleCourses[0]?.title || __('Khóa học dành cho bạn') }}</strong>
								<router-link v-if="visibleCourses.length" :to="{ name: 'CourseDetail', params: { courseName: visibleCourses[0].name } }">{{ __('Xem chi tiết') }}</router-link>
								<router-link v-else :to="{ name: 'Courses' }">{{ __('Xem khóa học') }}</router-link>
							</div>
						</div>
						<div class="guest-float guest-float-one"><span class="lucide-book-open" aria-hidden="true"></span><div><strong>{{ __('Khóa học') }}</strong><small>{{ __('Khám phá kiến thức') }}</small></div></div>
						<img class="guest-mascot-welcome" :src="welcomeMascot" alt="" aria-hidden="true" />
						<div class="guest-float guest-float-two"><span class="lucide-calendar-days" aria-hidden="true"></span><div><strong>{{ __('Lớp học') }}</strong><small>{{ __('Học cùng giảng viên') }}</small></div></div>
					</div>
				</div>
			</section>
			<div class="guest-capability-wrap"><div class="guest-container"><div class="guest-capability-strip">
				<router-link :to="{ name: 'Courses' }"><span class="lucide-book-open" aria-hidden="true"></span><div><strong>{{ __('Khóa học') }}</strong><small>{{ __('Khám phá nội dung đào tạo') }}</small></div></router-link>
				<router-link :to="{ name: 'Batches' }"><span class="lucide-users" aria-hidden="true"></span><div><strong>{{ __('Lớp học') }}</strong><small>{{ __('Học tập cùng giảng viên') }}</small></div></router-link>
				<a href="#guest-topics-title"><span class="lucide-grid-2x2" aria-hidden="true"></span><div><strong>{{ __('Lĩnh vực đào tạo') }}</strong><small>{{ __('Tìm chủ đề phù hợp') }}</small></div></a>
				<a href="/login"><span class="lucide-user-round" aria-hidden="true"></span><div><strong>{{ __('Tài khoản học viên') }}</strong><small>{{ __('Đăng nhập để học tập') }}</small></div></a>
			</div></div></div>
			<section class="guest-container guest-topics" aria-labelledby="guest-topics-title">
				<div class="guest-section-header"><span>{{ __('Lĩnh vực đào tạo') }}</span><h2 id="guest-topics-title">{{ __('Tìm theo lĩnh vực') }}</h2><p>{{ __('Chọn chủ đề bạn quan tâm để tìm khóa học phù hợp.') }}</p></div>
				<div class="guest-topic-list"><router-link v-for="topic in topics" :key="topic" :to="{ name: 'Courses', query: { title: topic } }" class="guest-topic"><span class="lucide-book-open" aria-hidden="true"></span><strong>{{ __(topic) }}</strong></router-link></div>
			</section>
			<section class="guest-course-section"><div class="guest-container guest-courses" aria-labelledby="guest-courses-title">
				<div class="guest-courses-heading"><div class="guest-section-header"><span>{{ __('Bắt đầu học tập') }}</span><h2 id="guest-courses-title">{{ hasFeaturedCourses ? __('Khóa học nổi bật') : __('Khóa học dành cho bạn') }}</h2></div><router-link :to="{ name: 'Courses' }" class="guest-text-link">{{ __('Xem tất cả') }}</router-link></div>
				<div v-if="courses.list.loading && !courses.data" class="guest-state" role="status">{{ __('Loading...') }}</div>
				<p v-else-if="courses.list.error" class="guest-state" role="alert">{{ __('Không thể tải khóa học. Vui lòng thử lại sau.') }}</p>
				<div v-else-if="visibleCourses.length" class="guest-course-grid"><CourseCard v-for="course in visibleCourses" :key="course.name" :course="course" :to="{ name: 'CourseDetail', params: { courseName: course.name } }" /></div>
				<p v-else class="guest-state">{{ __('Chưa có khóa học để hiển thị.') }}</p>
			</div></section>
			<section class="guest-cta" aria-labelledby="guest-cta-title"><div class="guest-container guest-cta-box"><img class="guest-mascot-learning" :src="learningMascot" alt="" aria-hidden="true" /><div class="guest-cta-inner"><div><span>{{ __('Ai Coaching Vietnam') }}</span><h2 id="guest-cta-title">{{ __('Bắt đầu hành trình học tập của bạn') }}</h2><p>{{ __('Tìm khóa học hoặc lớp học phù hợp với mục tiêu của bạn.') }}</p></div><div class="guest-cta-actions"><router-link :to="{ name: 'Courses' }" class="guest-cta-primary">{{ __('Xem khóa học') }}</router-link><router-link :to="{ name: 'Batches' }" class="guest-cta-secondary">{{ __('Xem lớp học') }}</router-link></div></div></div></section>
		</main>
		<footer class="guest-footer"><div class="guest-container guest-footer-grid"><div class="guest-footer-about"><router-link :to="{ name: 'Home' }" class="guest-footer-brand">{{ brand.name || __('AI Coaching Vietnam') }}</router-link><p>{{ __('Đào tạo Kế toán, Kiểm toán, Thuế, Tài chính, Nhân sự và Quản trị doanh nghiệp.') }}</p></div><nav :aria-label="__('Khám phá')" class="guest-footer-column"><h2>{{ __('Khám phá') }}</h2><router-link :to="{ name: 'Courses' }">{{ __('Khóa học') }}</router-link><router-link :to="{ name: 'Batches' }">{{ __('Lớp học') }}</router-link><a href="#guest-topics-title">{{ __('Lĩnh vực đào tạo') }}</a></nav><nav :aria-label="__('Tài khoản')" class="guest-footer-column"><h2>{{ __('Tài khoản') }}</h2><a href="/login">{{ __('Đăng nhập') }}</a></nav></div><div class="guest-container guest-footer-bottom">{{ brand.name || __('AI Coaching Vietnam') }}</div></footer>
		<GuestAiChatbot />
	</div>
</template>
<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { Button, FormControl, createListResource, usePageMeta } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { sessionStore } from '@/stores/session'
import { safeUrl } from '@/utils/safeUrl'
import CourseCard from '@/components/CourseCard.vue'
import GuestAiChatbot from '@/components/AiChatbot/GuestAiChatbot.vue'
import PublicHeader from '@/components/Public/PublicHeader.vue'
import welcomeMascot from '@/assets/images/mascot/welcome.png'
import learningMascot from '@/assets/images/mascot/learning.png'
import './guest-home.css'

const learningImage = '/assets/lms/images/auth-learning.png'

const router = useRouter()
const { brand } = sessionStore()
onMounted(() => {
	if (window.location.hash === '#guest-topics-title') {
		nextTick(() => document.getElementById('guest-topics-title')?.scrollIntoView())
	}
})
const search = ref('')
const topics = ['Kế toán', 'Kiểm toán', 'Thuế', 'Tài chính', 'Nhân sự', 'Quản trị doanh nghiệp']
const courses = createListResource({
	doctype: 'LMS Course',
	url: 'lms.lms.utils.get_courses',
	filters: { published: 1, upcoming: 0, live: 1 },
	pageLength: 6,
	auto: true,
})
const featuredCourses = computed(() => (courses.data || []).filter((course) => course.featured))
const hasFeaturedCourses = computed(() => featuredCourses.value.length > 0)
const visibleCourses = computed(() =>
	hasFeaturedCourses.value ? featuredCourses.value : courses.data || []
)

function searchCourses() {
	const title = search.value.trim()
	router.push({ name: 'Courses', query: title ? { title } : {} })
}

usePageMeta(() => ({ title: brand.name || __('Courses'), icon: brand.favicon }))
</script>
