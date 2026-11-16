<template>
	<div class="relative">
		<img
			v-if="image"
			:src="safeUrl(image)"
			:alt="fullName"
			class="object-cover h-[100px] w-[100px] rounded-full border-4 border-[color:var(--surface-base)]"
		/>
		<div
			v-else
			class="flex items-center justify-center h-[100px] w-[100px] rounded-full border-4 border-[color:var(--surface-base)] bg-surface-gray-2 text-4xl-semibold text-ink-gray-7"
		>
			{{ fullName.charAt(0).toUpperCase() }}
		</div>
	</div>
</template>
<script setup lang="ts">
import { safeUrl } from '@/utils/safeUrl'

defineProps<{
	image?: string | null
	fullName: string
}>()
</script>
