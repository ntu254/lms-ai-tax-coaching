<template>
	<article v-if="course.title" class="learner-card">
		<router-link :to="to" class="learner-card-link">
			<div class="learner-card-image" :class="{ 'is-placeholder': !course.image }" :style="course.image ? { backgroundImage: `url('${encodeURI(course.image)}')` } : undefined"><span v-if="!course.image" class="lucide-book-open" aria-hidden="true" /></div>
			<div class="learner-card-body">
				<span v-if="course.category" class="learner-card-category">{{ course.category }}</span>
				<h2>{{ course.title }}</h2>
				<p v-if="course.short_introduction" class="learner-card-description">{{ course.short_introduction }}</p>
				<p class="learner-card-instructor">{{ instructorNames || __('Giảng viên') }}</p>
				<div v-if="course.membership" class="learner-card-progress">{{ __('Tiến độ') }}: {{ Math.ceil(course.membership.progress || 0) }}%</div>
				<div class="learner-card-meta"><span v-if="Number(course.rating) > 0">★ {{ formatRating(course.rating) }}</span><span v-else>{{ __('Chưa có đánh giá') }}</span><strong v-if="course.paid_course != null">{{ course.paid_course ? (course.price || __('Xem chi tiết')) : __('Miễn phí') }}</strong></div>
			</div>
		</router-link>
	</article>
</template>
<script setup>
import { computed } from 'vue'
import { formatRating } from '@/utils'
const props = defineProps({ course: { type: Object, required: true }, to: { type: [Object, String], required: true } })
const instructorNames = computed(() => (props.course.instructors || []).map((item) => item.full_name).filter(Boolean).join(', '))
</script>
<style scoped>
.learner-card { height:100%; min-width:0; border:1px solid #e8ebf2; border-radius:18px; overflow:hidden; background:#fff; box-shadow:0 6px 24px rgba(16,24,40,.05); }.learner-card:hover { border-color:#f8b595; box-shadow:0 12px 32px rgba(16,24,40,.1); }.learner-card-link { display:flex; flex-direction:column; height:100%; color:#0b1220; text-decoration:none; }.learner-card-link:focus-visible { outline:3px solid #a83e05; outline-offset:-4px; }.learner-card-image { display:grid; place-items:center; min-height:165px; background-position:center; background-size:cover; }.learner-card-image.is-placeholder { background:linear-gradient(120deg,#fff1e6,#f5f2ff); color:#b54708; }.learner-card-image span { width:40px; height:40px; }.learner-card-body { display:flex; flex:1; flex-direction:column; gap:10px; padding:20px; }.learner-card-category { color:#a83e05; font-size:12px; font-weight:700; }.learner-card h2 { font-size:17px; line-height:1.4; font-weight:700; overflow-wrap:anywhere; }.learner-card-description { display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; color:#667085; font-size:13px; line-height:1.6; }.learner-card-instructor,.learner-card-progress { color:#667085; font-size:13px; }.learner-card-meta { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:auto; padding-top:12px; color:#667085; font-size:12px; }.learner-card-meta strong { color:#0b1220; font-size:15px; }
</style>
