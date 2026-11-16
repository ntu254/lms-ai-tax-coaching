<template>
	<div class="guest-chat-root">
		<button v-if="!isOpen" type="button" class="guest-chat-trigger" aria-label="Mở trợ lý tư vấn khóa học" @click="toggleChat">
			<img :src="mascot" alt="" />
			<span>{{ __('Hỏi trợ lý') }}</span>
		</button>
		<section v-if="isOpen" class="guest-chat-panel" role="dialog" aria-label="Trợ lý tư vấn khóa học">
			<header class="guest-chat-header">
				<div class="guest-chat-profile"><div class="guest-chat-avatar"><img :src="mascot" alt="" /></div><div><h3>Ai Coaching Vietnam</h3><p>{{ __('Trợ lý tư vấn khóa học') }}</p></div></div>
				<div class="guest-chat-controls">
					<button type="button" :title="__('Làm mới cuộc trò chuyện')" :aria-label="__('Làm mới')" @click="clearChat"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 12a9 9 0 0 1 15.7-6.3L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.7 6.3L3 16m0 5v-5h5" /></svg></button>
					<button type="button" :title="__('Đóng cửa sổ')" :aria-label="__('Đóng')" @click="toggleChat"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12" /></svg></button>
				</div>
			</header>
			<div ref="messagesContainer" class="guest-chat-messages" aria-live="polite" aria-relevant="additions">
				<div v-for="(msg, idx) in messages" :key="idx" class="guest-chat-message" :class="{ 'is-user': msg.role === 'user' }">
					<div class="guest-chat-bubble"><span v-html="formatMessage(msg.text)"></span><router-link v-if="msg.unavailable" :to="{ name: 'Courses' }" class="guest-chat-catalog">{{ __('Xem khóa học') }}</router-link></div>
					<span class="guest-chat-time">{{ msg.time }}</span>
				</div>
				<div v-if="isLoading" class="guest-chat-loading" role="status">{{ __('Trợ lý đang soạn câu trả lời...') }}</div>
				<div v-if="messages.length <= 2" class="guest-chat-suggestions"><p>{{ __('Bạn có thể hỏi') }}</p><div><button v-for="(prompt, idx) in quickPrompts" :key="idx" type="button" :disabled="isLoading" @click="sendQuickPrompt(prompt)">{{ __(prompt) }}</button></div></div>
			</div>
			<form class="guest-chat-form" @submit.prevent="sendMessage">
				<div class="guest-chat-input-wrap"><input ref="inputField" v-model="inputQuery" type="text" :placeholder="__('Nhập câu hỏi của bạn...')" :aria-label="__('Nhập câu hỏi của bạn')" :disabled="isLoading" /><button type="submit" :disabled="!inputQuery.trim() || isLoading" :aria-label="__('Gửi câu hỏi')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m22 2-7 20-4-9-9-4ZM22 2 11 13" /></svg></button></div>
				<p>{{ __('Thông tin từ trợ lý chỉ mang tính tham khảo.') }}</p>
			</form>
		</section>
	</div>
</template>
<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { call } from 'frappe-ui'
import mascot from '@/assets/images/mascot/welcome.png'

interface ChatMessage {
	role: 'user' | 'assistant'
	text: string
	time: string
	unavailable?: boolean
}

const isOpen = ref(false)
const isLoading = ref(false)
const inputQuery = ref('')
const messagesContainer = ref<HTMLDivElement | null>(null)
const inputField = ref<HTMLInputElement | null>(null)

const quickPrompts = [
	'Các khóa học về kế toán',
	'Tôi muốn tìm khóa học về thuế',
	'Xem thông tin lớp học',
	'Hướng dẫn đăng ký khóa học',
]
const nowTime = () => {
	const d = new Date()
	return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
}

const DEFAULT_WELCOME: ChatMessage = {
	role: 'assistant',
	text: 'Xin chào! Tôi là trợ lý tư vấn khóa học của **Ai Coaching Vietnam**. Tôi có thể giúp bạn tìm hiểu về khóa học và lớp học. Bạn đang quan tâm đến nội dung nào?',
	time: nowTime(),
}
const messages = ref<ChatMessage[]>([DEFAULT_WELCOME])

const scrollToBottom = () => {
	nextTick(() => {
		if (messagesContainer.value) {
			messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
		}
	})
}

const toggleChat = () => {
	isOpen.value = !isOpen.value
	if (isOpen.value) {
		scrollToBottom()
		nextTick(() => {
			inputField.value?.focus()
		})
	}
}

const clearChat = () => {
	messages.value = [DEFAULT_WELCOME]
	try {
		localStorage.removeItem('ai_coach_course_chat_v3')
	} catch {}
}

const formatMessage = (text: string) => {
	if (!text) return ''
	// Chuyển markdown cơ bản: **bold** sang <strong>
	let formatted = text
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
		.replace(/\*(.*?)\*/g, '<em>$1</em>')
	return formatted
}

const sendQuickPrompt = (prompt: string) => {
	inputQuery.value = prompt
	sendMessage()
}

const sendMessage = async () => {
	const query = inputQuery.value.trim()
	if (!query || isLoading.value) return

	messages.value.push({
		role: 'user',
		text: query,
		time: nowTime(),
	})
	inputQuery.value = ''
	isLoading.value = true
	scrollToBottom()

	try {
		const res = await call('lms.lms.ai_coach.guest_ai_chat', {
			message: query,
		})

		const reply = res?.response || 'Rất tiếc, đã có gián đoạn tạm thời. Bạn vui lòng thử lại sau giây lát.'
		messages.value.push({
			role: 'assistant',
			text: reply,
			time: nowTime(),
			unavailable: res?.status === 'unavailable',
		})
	} catch (err: any) {
		messages.value.push({
			role: 'assistant',
			text: 'Trợ lý tư vấn hiện tạm thời không khả dụng. Bạn có thể xem danh sách khóa học trong lúc chờ.',
			time: nowTime(),
			unavailable: true,
		})
	} finally {
		isLoading.value = false
		scrollToBottom()
		saveHistory()
	}
}

const saveHistory = () => {
	try {
		localStorage.setItem(
			'ai_coach_course_chat_v3',
			JSON.stringify(messages.value.slice(-10))
		)
	} catch {}
}

onMounted(() => {
	try {
		const saved = localStorage.getItem('ai_coach_course_chat_v3')
		if (saved) {
			const parsed = JSON.parse(saved)
			if (Array.isArray(parsed) && parsed.length > 0) {
				messages.value = parsed
			}
		}
	} catch {}
})
</script>

<style scoped>
.guest-chat-root { position:fixed; right:22px; bottom:22px; z-index:50; font-family:Inter,ui-sans-serif,system-ui,sans-serif; color:#0b1220; }
.guest-chat-trigger { display:flex; align-items:center; gap:4px; min-height:64px; padding:0 17px 0 3px; border:1px solid #ffe0cc; border-radius:999px; background:#fff; box-shadow:0 10px 36px rgba(16,24,40,.17); color:#9a3908; font-size:13px; font-weight:700; cursor:pointer; }
.guest-chat-trigger img { display:block; width:64px; height:64px; object-fit:contain; }
.guest-chat-trigger:hover { box-shadow:0 12px 38px rgba(255,116,23,.22); transform:translateY(-2px); }
.guest-chat-panel { display:flex; flex-direction:column; width:min(390px,calc(100vw - 32px)); height:min(560px,calc(100dvh - 32px)); overflow:hidden; background:#fff; border:1px solid #e8ebf2; border-radius:24px 24px 8px 24px; box-shadow:0 24px 80px rgba(16,24,40,.2); }
.guest-chat-header { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:16px; border-bottom:1px solid #f0e5df; background:linear-gradient(115deg,#fff7f3,#fffaf2); }
.guest-chat-profile { display:flex; align-items:center; gap:10px; min-width:0; }.guest-chat-avatar { display:grid; place-items:center; flex-shrink:0; width:48px; height:48px; border-radius:15px; background:#fff; border:1px solid #ffe8db; }.guest-chat-avatar img { width:47px; height:47px; object-fit:contain; }.guest-chat-profile h3 { margin:0; font-size:14px; font-weight:750; }.guest-chat-profile p { margin:4px 0 0; color:#667085; font-size:12px; }
.guest-chat-controls { display:flex; gap:4px; }.guest-chat-controls button { display:grid; place-items:center; width:36px; height:36px; border:0; border-radius:10px; background:transparent; color:#667085; cursor:pointer; }.guest-chat-controls button:hover { background:#fff; color:#a83e05; }.guest-chat-controls svg,.guest-chat-input-wrap svg { width:19px; height:19px; }
.guest-chat-messages { flex:1; min-height:0; overflow-y:auto; padding:18px 16px; background:#fbfbfd; }.guest-chat-message { display:flex; flex-direction:column; align-items:flex-start; margin-bottom:14px; }.guest-chat-message.is-user { align-items:flex-end; }.guest-chat-bubble { max-width:88%; padding:12px 14px; border:1px solid #e8ebf2; border-radius:16px 16px 16px 4px; background:#fff; color:#344054; font-size:13px; line-height:1.55; white-space:pre-line; overflow-wrap:anywhere; }.is-user .guest-chat-bubble { border-color:transparent; border-radius:16px 16px 4px 16px; background:#b54708; color:#fff; }.guest-chat-catalog { display:block; margin-top:10px; color:#a83e05; font-weight:700; text-decoration:underline; text-underline-offset:3px; }.guest-chat-time { margin:5px 4px 0; color:#667085; font-size:11px; }.guest-chat-loading { color:#667085; font-size:12px; }
.guest-chat-suggestions { margin-top:18px; }.guest-chat-suggestions p { margin:0 0 9px; color:#667085; font-size:12px; font-weight:600; }.guest-chat-suggestions div { display:flex; flex-wrap:wrap; gap:7px; }.guest-chat-suggestions button { padding:8px 11px; border:1px solid #f5d2bd; border-radius:999px; background:#fff; color:#9a3908; font-size:12px; text-align:left; cursor:pointer; }.guest-chat-suggestions button:hover { background:#fff5ed; }.guest-chat-suggestions button:disabled { opacity:.55; cursor:not-allowed; }
.guest-chat-form { padding:12px 14px 10px; border-top:1px solid #e8ebf2; background:#fff; }.guest-chat-input-wrap { display:flex; align-items:center; gap:8px; padding:4px; border:1px solid #d0d5dd; border-radius:14px; }.guest-chat-input-wrap:focus-within { border-color:#b54708; box-shadow:0 0 0 3px rgba(181,71,8,.16); }.guest-chat-input-wrap input { flex:1; min-width:0; height:38px; padding:0 9px; border:0; outline:0; background:transparent; color:#0b1220; font-size:13px; }.guest-chat-input-wrap input:focus, .guest-chat-input-wrap input:focus-visible { outline:none !important; box-shadow:none !important; border:0 !important; }.guest-chat-input-wrap button { display:grid; place-items:center; width:38px; height:38px; flex-shrink:0; border:0; border-radius:11px 11px 5px 11px; background:linear-gradient(115deg,#ff5b55,#ff7417); color:#fff; cursor:pointer; }.guest-chat-input-wrap button:disabled { opacity:.45; cursor:not-allowed; }.guest-chat-form>p { margin:8px 0 0; color:#667085; text-align:center; font-size:11px; }
.guest-chat-root button:focus-visible { outline:3px solid #9a3908; outline-offset:3px; }
@media (max-width:540px) { .guest-chat-root { right:12px; bottom:12px; }.guest-chat-trigger { min-height:56px; }.guest-chat-trigger img { width:56px; height:56px; }.guest-chat-panel { width:calc(100vw - 24px); height:min(560px,calc(100dvh - 24px)); } }
@media (prefers-reduced-motion:reduce) { .guest-chat-trigger:hover { transform:none; } }
@media print { .guest-chat-root { display:none; } }
</style>
