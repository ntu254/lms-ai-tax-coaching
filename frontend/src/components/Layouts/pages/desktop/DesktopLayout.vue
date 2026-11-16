<template>
	<div class="flex h-dvh w-screen" :class="{ 'learner-desktop': learner }">
		<LearnerHeader v-if="learner" />
		<a
			href="#main-content"
			@click.prevent="skipToContent('main-content')"
			class="sr-only focus:not-sr-only focus:absolute focus:start-4 focus:top-4 focus:z-50 focus:rounded-4 focus:bg-surface-base focus:px-4 focus:py-2 focus:text-ink-gray-9 focus:shadow-md focus:focus-ring"
		>
			{{ __('Skip to main content') }}
		</a>
		<div class="h-full border-e bg-surface-sidebar">
			<AppSidebar />
		</div>
		<main
			id="main-content"
			tabindex="-1"
			class="flex-1 flex flex-col h-full overflow-auto bg-surface-base focus:outline-none"
		>
			<slot />
		</main>
	</div>
</template>
<script setup>
import { skipToContent } from '@/utils/a11y'
import AppSidebar from '@/components/Sidebar/AppSidebar.vue'
import LearnerHeader from '@/components/Public/LearnerHeader.vue'
defineProps({ learner: { type: Boolean, default: false } })
</script>

<style scoped>
.learner-desktop { position:relative; width:100%; }
.learner-desktop :deep(.learner-site-header) { position:absolute; inset:0 0 auto; }
.learner-desktop > div, .learner-desktop > main { margin-top:68px; height:calc(100% - 68px); }
</style>
