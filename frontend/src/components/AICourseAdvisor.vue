<template>
	<div class="fixed bottom-6 right-6 z-50 flex flex-col items-end font-sans">
		<!-- Chat Window Card -->
		<transition
			enter-active-class="transition duration-250 ease-out"
			enter-from-class="transform scale-90 opacity-0 translate-y-6"
			enter-to-class="transform scale-100 opacity-100 translate-y-0"
			leave-active-class="transition duration-200 ease-in"
			leave-from-class="transform scale-100 opacity-100 translate-y-0"
			leave-to-class="transform scale-90 opacity-0 translate-y-6"
		>
			<div
				v-if="isOpen"
				class="mb-3 w-[360px] sm:w-[410px] h-[560px] max-h-[82vh] flex flex-col bg-white dark:bg-zinc-900 border border-slate-200 dark:border-zinc-800"
				style="border-radius: 24px; box-shadow: 0 25px 60px -15px rgba(15, 23, 42, 0.25), 0 0 0 1px rgba(226, 232, 240, 0.8); overflow: hidden;"
			>
				<!-- Rounded Soft Header -->
				<div
					class="px-5 py-3.5 flex items-center justify-between shadow-sm select-none shrink-0"
					style="background: #18181b; color: #ffffff; border-radius: 24px 24px 0 0;"
				>
					<div class="flex items-center gap-3">
						<div class="w-9 h-9 rounded-full bg-white/20 flex items-center justify-center backdrop-blur-md shadow-inner">
							<Sparkles class="w-4.5 h-4.5 text-amber-300 animate-pulse" />
						</div>
						<div>
							<div class="font-bold text-sm leading-tight text-white tracking-wide">
								{{ __('Trợ lý Tuyển sinh AI') }}
							</div>
							<div class="text-[11px] text-zinc-400 flex items-center gap-1.5 mt-0.5">
								<span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping inline-block" style="animation-duration: 2s;" />
								<span>{{ __('Gemini AI • Trực tuyến 24/7') }}</span>
							</div>
						</div>
					</div>
					<div class="flex items-center gap-1">
						<button
							type="button"
							class="w-8 h-8 rounded-full flex items-center justify-center text-white/80 hover:text-white hover:bg-white/20 transition-all duration-150"
							:title="__('Xóa đoạn chat')"
							@click="clearChat"
						>
							<Trash2 class="w-4 h-4" />
						</button>
						<button
							type="button"
							class="w-8 h-8 rounded-full flex items-center justify-center text-white/80 hover:text-white hover:bg-white/20 transition-all duration-150"
							:title="__('Thu nhỏ')"
							@click="isOpen = false"
						>
							<X class="w-4.5 h-4.5" />
						</button>
					</div>
				</div>

				<!-- Messages Area -->
				<div
					ref="chatContainer"
					class="flex-1 overflow-y-auto p-4 space-y-4 text-sm"
					style="background-color: #f8fafc;"
				>
					<!-- Welcome Message -->
					<div class="flex gap-2.5 items-start">
						<div
							class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5 shadow-sm"
							style="background: #18181b; color: #ffffff;"
						>
							<Bot class="w-4.5 h-4.5" />
						</div>
						<div
							class="p-4 shadow-sm max-w-[85%] text-sm leading-relaxed"
							style="background-color: #ffffff; color: #0f172a; border-radius: 4px 20px 20px 20px; border: 1px solid #f1f5f9; box-shadow: 0 4px 12px rgba(0,0,0,0.03);"
						>
							{{ __('Xin chào! Mình là trợ lý tuyển sinh AI. Bạn đang muốn tìm khóa học theo mục tiêu hay ngân sách nào để mình tư vấn phù hợp nhất nhé? 😊') }}
						</div>
					</div>

					<!-- Messages List -->
					<div
						v-for="(msg, index) in messages"
						:key="index"
						:class="['flex gap-2.5 items-start', msg.role === 'user' ? 'justify-end' : 'justify-start']"
					>
						<div
							v-if="msg.role === 'assistant'"
							class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5 shadow-sm"
							style="background: #18181b; color: #ffffff;"
						>
							<Bot class="w-4.5 h-4.5" />
						</div>
						<div
							v-if="msg.role === 'user'"
							class="px-4 py-2.5 max-w-[82%] text-sm leading-relaxed shadow-md whitespace-pre-wrap font-medium"
							style="background: #18181b; color: #ffffff; border-radius: 20px 4px 20px 20px; box-shadow: 0 4px 14px rgba(0,0,0,0.15);"
						>
							{{ msg.text }}
						</div>
						<div
							v-else
							class="p-4 max-w-[85%] text-sm leading-relaxed shadow-sm whitespace-pre-wrap"
							style="background-color: #ffffff; color: #0f172a; border-radius: 4px 20px 20px 20px; border: 1px solid #f1f5f9; box-shadow: 0 4px 12px rgba(0,0,0,0.03);"
							v-html="renderFormattedMessage(msg.text)"
							@click="handleMessageLinkClick"
						/>
					</div>

					<!-- Typing Animation Indicator -->
					<div v-if="isLoading" class="flex gap-2.5 items-start">
						<div
							class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm"
							style="background: #18181b; color: #ffffff;"
						>
							<Bot class="w-4.5 h-4.5" />
						</div>
						<div
							class="px-4 py-3 flex items-center gap-1.5 shadow-sm"
							style="background-color: #ffffff; border-radius: 4px 18px 18px 18px; border: 1px solid #f1f5f9;"
						>
							<span class="w-2 h-2 rounded-full bg-blue-600 animate-bounce" style="animation-delay: 0ms" />
							<span class="w-2 h-2 rounded-full bg-blue-600 animate-bounce" style="animation-delay: 150ms" />
							<span class="w-2 h-2 rounded-full bg-blue-600 animate-bounce" style="animation-delay: 300ms" />
						</div>
					</div>
				</div>

				<!-- Rounded Quick Chips -->
				<div
					v-if="!messages.length"
					class="px-4 py-2.5 bg-white border-t border-slate-100 flex flex-wrap gap-1.5 shrink-0"
				>
					<button
						v-for="(chip, i) in promptChips"
						:key="i"
						type="button"
						class="text-[12px] font-medium px-3.5 py-1.5 rounded-full transition-all duration-150 active:scale-95 text-left flex items-center gap-1.5 shadow-sm"
						style="background-color: #f4f4f5; color: #18181b; border: 1px solid #e4e4e7;"
						@click="sendPreset(chip.query)"
					>
						<span>{{ chip.icon }}</span>
						<span>{{ chip.label }}</span>
					</button>
				</div>

				<!-- Rounded Input Area -->
				<div class="p-3 bg-white border-t border-slate-200 flex gap-2 items-center shrink-0">
					<textarea
						ref="inputArea"
						v-model="inputText"
						rows="1"
						class="flex-1 rounded-full px-4 py-2 text-sm text-slate-800 placeholder:text-slate-400 resize-none outline-none transition-all max-h-24 leading-relaxed border border-slate-300 focus:border-blue-600 focus:ring-1 focus:ring-blue-600"
						style="background-color: #f8fafc;"
						:placeholder="__('Hỏi về khóa học, học phí, lộ trình...')"
						:disabled="isLoading"
						@keydown.enter.prevent="sendMessage"
					/>
					<button
						type="button"
						:disabled="!inputText.trim() || isLoading"
						class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 transition-all duration-150 hover:scale-105 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed shadow-md cursor-pointer"
						style="background: #18181b; color: #ffffff;"
						@click="sendMessage"
					>
						<Send class="w-4 h-4 text-white ml-0.5" />
					</button>
				</div>
			</div>
		</transition>

		<!-- Floating Round Circle Button (FAB) -->
		<button
			type="button"
			class="w-14 h-14 rounded-full flex items-center justify-center shadow-2xl transition-all duration-300 transform hover:scale-110 active:scale-95 cursor-pointer border-2 border-white/50 select-none"
			style="background: #18181b; color: #ffffff; box-shadow: 0 12px 30px -4px rgba(0, 0, 0, 0.45); border: 2px solid rgba(255, 255, 255, 0.2);"
			:title="isOpen ? __('Thu nhỏ') : __('Tư vấn khóa học AI')"
			@click="toggleChat"
		>
			<X v-if="isOpen" class="w-6 h-6 text-white transition-transform duration-200" />
			<Sparkles v-else class="w-6 h-6 text-amber-300 animate-pulse" />
		</button>
	</div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { call, toast } from 'frappe-ui'
import {
	Sparkles,
	Send,
	Trash2,
	X,
	Bot,
} from 'lucide-vue-next'

interface Message {
	role: 'user' | 'assistant'
	text: string
}

const router = useRouter()
const isOpen = ref(false)
const isLoading = ref(false)
const inputText = ref('')
const messages = ref<Message[]>([])
const chatContainer = ref<HTMLElement | null>(null)
const inputArea = ref<HTMLTextAreaElement | null>(null)

const promptChips = [
	{ icon: '🎯', label: 'Khóa học cho người mới?', query: 'Khóa học nào phù hợp cho người mới bắt đầu?' },
	{ icon: '💰', label: 'Học phí các khóa học?', query: 'Học phí các khóa học hiện tại như thế nào?' },
	{ icon: '📊', label: 'Khóa Thuế TNCN dạy gì?', query: 'Khóa học Thuế thu nhập cá nhân dạy những gì?' },
]

function toggleChat() {
	isOpen.value = !isOpen.value
	if (isOpen.value) {
		nextTick(() => {
			inputArea.value?.focus()
			scrollToBottom()
		})
	}
}

function clearChat() {
	messages.value = []
}

function sendPreset(text: string) {
	inputText.value = text
	sendMessage()
}

async function sendMessage() {
	const text = inputText.value.trim()
	if (!text || isLoading.value) return

	messages.value.push({ role: 'user', text })
	inputText.value = ''
	isLoading.value = true
	scrollToBottom()

	try {
		const res = await call('lms.lms.ai.gemini.advise_courses', {
			message: text,
			history: JSON.stringify(messages.value.map(m => ({ role: m.role, text: m.text }))),
		})

		const replyText = res?.reply || res?.message?.reply || (typeof res === 'string' ? res : __('Rất tiếc, mình chưa thể phản hồi lúc này.'))
		messages.value.push({
			role: 'assistant',
			text: replyText,
		})
	} catch (err: any) {
		toast.error(err.message || __('Lỗi kết nối tới Trợ lý AI.'))
		messages.value.push({
			role: 'assistant',
			text: __('⚠️ Đã xảy ra lỗi khi kết nối với AI. Vui lòng thử lại sau ít phút.'),
		})
	} finally {
		isLoading.value = false
		scrollToBottom()
	}
}

function scrollToBottom() {
	nextTick(() => {
		if (chatContainer.value) {
			chatContainer.value.scrollTop = chatContainer.value.scrollHeight
		}
	})
}

// Convert markdown like **bold**, bullet points, and [Label](/courses/slug) to clickable styled links
function renderFormattedMessage(rawText: string): string {
	if (!rawText) return ''

	let escaped = rawText
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')

	// Convert bold **text** to <strong>
	escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-slate-900">$1</strong>')

	// Convert markdown links [Label](url) to styled buttons/anchors
	escaped = escaped.replace(
		/\[([^\]]+)\]\(([^)]+)\)/g,
		'<a href="$2" data-nav="$2" class="inline-flex items-center gap-1 font-semibold text-zinc-900 bg-zinc-100 hover:bg-zinc-200 px-2.5 py-1 rounded-lg border border-zinc-300 underline decoration-zinc-400 transition-colors my-1">$1</a>'
	)

	return escaped
}

// Intercept clicks on links inside messages to use client-side router navigation
function handleMessageLinkClick(e: MouseEvent) {
	const target = (e.target as HTMLElement).closest('a[data-nav]') as HTMLAnchorElement | null
	if (target) {
		e.preventDefault()
		const route = target.getAttribute('data-nav')
		if (route) {
			if (route.startsWith('/')) {
				router.push(route)
			} else {
				router.push(`/${route}`)
			}
		}
	}
}
</script>
