<template>
	<Home v-if="isLoggedIn" />
	<GuestHome v-else />
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { sessionStore } from '@/stores/session'
import GuestHome from './GuestHome.vue'
import Home from './Home.vue'

const { isLoggedIn } = storeToRefs(sessionStore())
</script>
