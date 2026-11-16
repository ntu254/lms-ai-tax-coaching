<template>
	<Avatar
		class="avatar border border-outline-gray-2 cursor-auto"
		v-if="user"
		:label="user.full_name"
		:image="user.user_image"
		:size="size"
		v-bind="$attrs"
	>
	</Avatar>
</template>
<script setup lang="ts">
import { Avatar } from 'frappe-ui'
import type { UserInfo } from '@/types'

defineProps<{
	user?: Pick<UserInfo, 'full_name' | 'user_image'> | null
	size?: string
}>()

</script>
