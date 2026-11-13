<template>
	<Dialog
		v-model:open="show"
		:title="__('Trợ lý học tập AI (Google Gemini)')"
		size="2xl"
	>
		<template #default>
			<div class="flex flex-col gap-4">
				<div class="flex items-center justify-between bg-surface-gray-2 p-3 rounded-lg text-sm">
					<div class="font-medium text-ink-gray-8 truncate">
						📖 {{ props.lessonTitle }}
					</div>
					<Button
						variant="subtle"
						size="sm"
						:loading="isSummarizing"
						@click="getSummary"
					>
						✨ {{ __('Tóm tắt bài học') }}
					</Button>
				</div>

				<div v-if="conversation.length" class="flex flex-col gap-3 max-h-[350px] overflow-y-auto p-1">
					<div
						v-for="(msg, idx) in conversation"
						:key="idx"
						:class="[
							'p-3.5 rounded-lg text-sm leading-relaxed whitespace-pre-wrap',
							msg.role === 'user'
								? 'bg-primary-50 text-primary-900 dark:bg-primary-950/30 ms-8 text-right'
								: 'bg-surface-gray-2 text-ink-gray-9 me-8'
						]"
					>
						<div class="text-xs font-semibold mb-1 opacity-70">
							{{ msg.role === 'user' ? __('Bạn') : __('Trợ lý AI') }}
						</div>
						{{ msg.text }}
					</div>
				</div>
				<div v-else class="text-center py-6 text-sm text-ink-gray-5">
					{{ __('Hãy đặt bất kỳ câu hỏi nào về nội dung bài học hoặc bấm Tóm tắt.') }}
				</div>

				<div class="flex gap-2 items-end pt-2 border-t">
					<FormControl
						type="textarea"
						:rows="2"
						class="flex-1"
						:placeholder="__('Nhập thắc mắc của bạn về bài giảng...')"
						v-model="question"
						@keydown.enter.prevent="askQuestion"
					/>
					<Button
						variant="solid"
						:loading="isAsking"
						:disabled="!question.trim()"
						@click="askQuestion"
					>
						{{ __('Gửi') }}
					</Button>
				</div>
			</div>
		</template>
	</Dialog>
</template>

<script setup lang="ts">
import { Dialog, FormControl, Button, createResource, toast } from 'frappe-ui'
import { ref } from 'vue'

const show = defineModel<boolean>({ default: false })

const props = defineProps<{
	lessonTitle: string
	lessonContent: string
}>()

interface Message {
	role: 'user' | 'assistant'
	text: string
}

const question = ref('')
const conversation = ref<Message[]>([])
const isAsking = ref(false)
const isSummarizing = ref(false)

const askTutorResource = createResource({
	url: 'lms.lms.ai.gemini.ask_lesson_tutor',
})

const summaryResource = createResource({
	url: 'lms.lms.ai.gemini.summarize_lesson',
})

async function askQuestion() {
	const q = question.value.trim()
	if (!q || isAsking.value) return

	conversation.value.push({ role: 'user', text: q })
	question.value = ''
	isAsking.value = true

	try {
		const res = await askTutorResource.submit({
			lesson_title: props.lessonTitle,
			lesson_content: props.lessonContent,
			question: q,
		})
		conversation.value.push({ role: 'assistant', text: res.answer })
	} catch (err: any) {
		toast.error(err.message || __('Lỗi kết nối Gemini AI'))
	} finally {
		isAsking.value = false
	}
}

async function getSummary() {
	if (isSummarizing.value) return
	isSummarizing.value = true

	try {
		const res = await summaryResource.submit({
			lesson_title: props.lessonTitle,
			lesson_content: props.lessonContent,
		})
		conversation.value.push({
			role: 'assistant',
			text: `📌 TÓM TẮT BÀI HỌC:\n\n${res.summary}`,
		})
	} catch (err: any) {
		toast.error(err.message || __('Lỗi khi tóm tắt bài học'))
	} finally {
		isSummarizing.value = false
	}
}
</script>
