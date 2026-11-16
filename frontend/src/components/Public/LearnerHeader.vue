<template>
	<header class="learner-site-header">
		<router-link :to="{ name: 'Home' }" class="learner-site-brand"><img :src="brandLogo" :alt="brand.name || __('AI Coaching Vietnam')" /></router-link>
		<nav class="learner-site-nav" :aria-label="__('Điều hướng học tập')">
			<router-link :to="{ name: 'Home' }">{{ __('Trang chủ') }}</router-link>
			<router-link :to="{ name: 'Courses' }">{{ __('Khóa học') }}</router-link>
			<router-link :to="{ name: 'Batches' }">{{ __('Lớp học') }}</router-link>
		</nav>
		<router-link v-if="userResource.data?.username" :to="{ name: 'Profile', params: { username: userResource.data.username } }" class="learner-site-account">{{ userResource.data.full_name || __('Tài khoản') }}</router-link>
	</header>
</template>
<script setup>
import brandLogo from '@/assets/images/ai-coaching-vietnam.png'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/user'
const { brand } = sessionStore()
const { userResource } = usersStore()
</script>
<style scoped>
.learner-site-header { display:flex; align-items:center; gap:24px; height:68px; padding:0 24px; background:#fff; border-bottom:1px solid #e8ebf2; z-index:25; }
.learner-site-brand { flex-shrink:0; }.learner-site-brand img { display:block; width:140px; height:46px; object-fit:contain; }
.learner-site-nav { display:flex; align-items:center; justify-content:center; gap:28px; flex:1; height:100%; }.learner-site-nav a { display:flex; align-items:center; height:100%; color:#344054; font-size:14px; font-weight:700; text-decoration:none; }.learner-site-nav a.router-link-active { color:#a83e05; border-bottom:2px solid #ff7417; }
.learner-site-account { max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:#a83e05; font-size:13px; font-weight:700; text-decoration:none; }.learner-site-header a:focus-visible { outline:3px solid #b54708; outline-offset:3px; }
@media(max-width:767px) { .learner-site-header { height:58px; padding:0 16px; }.learner-site-brand img { width:120px; height:40px; }.learner-site-nav { display:none; }.learner-site-account { margin-left:auto; max-width:150px; } }
</style>
