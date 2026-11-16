<template>
	<header class="site-header">
		<nav class="site-nav" :aria-label="__('Điều hướng chính')">
			<router-link :to="{ name: 'Home' }" class="site-brand"><img :src="brandLogo" :alt="brand.name || __('AI Coaching Vietnam')" /></router-link>
			<div class="site-links">
				<router-link :to="{ name: 'Home' }" :class="{ 'is-active': active === 'home' }" :aria-current="active === 'home' ? 'page' : undefined">{{ __('Trang chủ') }}</router-link>
				<router-link :to="{ name: 'Courses' }" :class="{ 'is-active': active === 'courses' }" :aria-current="active === 'courses' ? 'page' : undefined">{{ __('Khóa học') }}</router-link>
				<router-link :to="{ name: 'Batches' }" :class="{ 'is-active': active === 'batches' }" :aria-current="active === 'batches' ? 'page' : undefined">{{ __('Lớp học') }}</router-link>
				<a :href="active === 'home' ? '#guest-topics-title' : '/lms/#guest-topics-title'">{{ __('Lĩnh vực đào tạo') }}</a>
			</div>
			<a href="/login" class="site-login">{{ __('Đăng nhập') }}</a>
		</nav>
	</header>
</template>
<script setup>
import { sessionStore } from '@/stores/session'
import brandLogo from '@/assets/images/ai-coaching-vietnam.png'
const { brand } = sessionStore()
defineProps({ active: { type: String, default: 'home' } })
</script>
<style scoped>
.site-header { position:sticky; top:0; z-index:30; background:rgba(255,255,255,.94); border-bottom:1px solid #e8ebf2; backdrop-filter:blur(16px); }
.site-nav { width:min(1200px,calc(100% - 48px)); margin-inline:auto; min-height:80px; display:flex; align-items:center; gap:24px; }
.site-brand { display:flex; flex-shrink:0; align-items:center; text-decoration:none; }.site-brand img { display:block; width:150px; height:48px; object-fit:contain; }
.site-links { display:flex; align-items:center; justify-content:center; flex:1; gap:30px; }.site-links a { display:flex; align-items:center; position:relative; min-height:80px; color:#344054; font-size:14px; font-weight:700; text-decoration:none; white-space:nowrap; }.site-links a:hover,.site-links a.is-active { color:#a83e05; }.site-links a.is-active:after { content:''; position:absolute; bottom:0; left:0; right:0; height:2px; background:#ff7417; }
.site-login { display:inline-flex; justify-content:center; align-items:center; min-height:46px; padding:0 20px; border-radius:12px 12px 5px 12px; background:linear-gradient(115deg,#ff5b55,#ff7417); color:#fff; font-size:14px; font-weight:750; text-decoration:none; box-shadow:0 8px 20px rgba(255,116,23,.2); white-space:nowrap; }.site-login:hover { color:#fff; filter:brightness(.9); }.site-header a:focus-visible { outline:3px solid #b54708; outline-offset:3px; }
@media(max-width:1000px) { .site-nav { flex-wrap:wrap; gap:10px; padding-block:10px; }.site-links { order:3; flex-basis:100%; justify-content:flex-start; gap:22px; overflow-x:auto; }.site-links a { min-height:40px; }.site-login { margin-left:auto; } }
@media(max-width:650px) { .site-nav { width:calc(100% - 32px); }.site-brand img { width:125px; height:38px; }.site-links { gap:18px; }.site-login { min-height:40px; padding-inline:12px; font-size:13px; } }
</style>
