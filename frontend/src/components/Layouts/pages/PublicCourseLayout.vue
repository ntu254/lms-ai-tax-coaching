<template>
	<div class="public-course-layout">
		<a href="#public-course-content" class="public-skip">{{ __('Skip to main content') }}</a>
		<PublicHeader :active="activeSection" />
		<main id="public-course-content" class="public-content"><slot /></main>
		<footer class="public-footer"><div class="public-container public-footer-inner"><div><router-link :to="{ name: 'Home' }" class="public-footer-brand">{{ brand.name || __('AI Coaching Vietnam') }}</router-link><p>{{ __('Đào tạo Kế toán, Kiểm toán, Thuế, Tài chính, Nhân sự và Quản trị doanh nghiệp.') }}</p></div><nav :aria-label="__('Khám phá')"><strong>{{ __('Khám phá') }}</strong><router-link :to="{ name: 'Courses' }">{{ __('Khóa học') }}</router-link><router-link :to="{ name: 'Batches' }">{{ __('Lớp học') }}</router-link><a href="/login">{{ __('Đăng nhập') }}</a></nav></div></footer>
	</div>
</template>
<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { sessionStore } from '@/stores/session'
import PublicHeader from '@/components/Public/PublicHeader.vue'
const { brand } = sessionStore()
const route = useRoute()
const activeSection = computed(() => ['Batches', 'BatchDetail'].includes(route.name) ? 'batches' : 'courses')
</script>
<style scoped>
.public-course-layout { min-height:100%; background:#fff; color:#0b1220; font-family:Inter,ui-sans-serif,system-ui,sans-serif; }.public-container { width:min(1200px,calc(100% - 48px)); margin-inline:auto; }.public-header { position:sticky; top:0; z-index:20; background:rgba(255,255,255,.97); border-bottom:1px solid #e8ebf2; }.public-nav { min-height:80px; display:flex; align-items:center; gap:24px; }.public-brand img { display:block; width:150px; height:48px; object-fit:contain; }.public-links { display:flex; align-items:center; justify-content:center; gap:30px; flex:1; }.public-links a { position:relative; display:flex; align-items:center; min-height:80px; color:#344054; font-size:14px; font-weight:700; text-decoration:none; }.public-links a.active { color:#a83e05; }.public-links a.active:after { content:''; position:absolute; bottom:0; left:0; right:0; height:2px; background:#ff7417; }.public-login { display:inline-flex; align-items:center; justify-content:center; min-height:46px; padding:0 20px; border-radius:12px 12px 5px 12px; background:linear-gradient(115deg,#ff5b55,#ff7417); color:#fff; font-size:14px; font-weight:700; text-decoration:none; }.public-skip { position:absolute; left:-9999px; }.public-skip:focus { left:16px; top:16px; z-index:99; padding:12px; background:white; }.public-content { min-height:65vh; }.public-footer { background:#0b1220; color:#fff; }.public-footer-inner { display:grid; grid-template-columns:2fr 1fr; gap:40px; padding-block:55px; }.public-footer-brand { font-size:18px; font-weight:700; color:#fff; text-decoration:none; }.public-footer p { max-width:410px; margin-top:12px; color:#cbd5e1; line-height:1.7; }.public-footer nav { display:flex; flex-direction:column; gap:12px; }.public-footer nav a { color:#e2e8f0; text-decoration:none; }.public-course-layout a:focus-visible { outline:3px solid #a83e05; outline-offset:3px; }.public-footer a:focus-visible { outline-color:#fff; }
@media(max-width:650px) { .public-container { width:calc(100% - 32px); }.public-nav { flex-wrap:wrap; gap:8px; padding-block:8px; }.public-brand img { width:125px; height:38px; }.public-login { margin-left:auto; min-height:40px; }.public-links { order:3; flex-basis:100%; justify-content:flex-start; gap:24px; }.public-links a { min-height:38px; }.public-footer-inner { grid-template-columns:1fr; gap:28px; } }
</style>
