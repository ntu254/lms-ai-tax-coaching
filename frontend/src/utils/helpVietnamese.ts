const phrases: Record<string, string> = {
  'Help': 'Trợ giúp',
  'Getting started': 'Bắt đầu',
  'Help center': 'Trung tâm trợ giúp',
  'Help centre': 'Trung tâm trợ giúp',
  'All articles': 'Tất cả bài viết',
  'Search articles...': 'Tìm bài viết...',
  'Open docs': 'Mở tài liệu',
  'More options': 'Thêm tùy chọn',
  'Maximize': 'Mở rộng',
  'Minimize': 'Thu nhỏ',
  'Close': 'Đóng',
  'Reset onboarding steps': 'Đặt lại các bước hướng dẫn',
  'Reset all': 'Đặt lại tất cả',
  'Skip all': 'Bỏ qua tất cả',
  'Reset': 'Đặt lại',
  'Skip': 'Bỏ qua',
  'Start now': 'Bắt đầu ngay',
  'Continue': 'Tiếp tục',
  'You are all set': 'Bạn đã sẵn sàng',
  'All steps are completed successfully': 'Bạn đã hoàn thành tất cả các bước',
}

export function translateHelpText(text: string): string {
  const exact = phrases[text]
  if (exact) return exact
  let match = text.match(/^Welcome to (.+)$/)
  if (match) return `Chào mừng bạn đến với ${match[1]}`
  match = text.match(/^(\d+)\/(\d+) steps completed$/)
  if (match) return `Đã hoàn thành ${match[1]}/${match[2]} bước`
  match = text.match(/^(\d+)\/(\d+) steps$/)
  if (match) return `${match[1]}/${match[2]} bước`
  match = text.match(/^(\d+)% completed$/)
  if (match) return `Đã hoàn thành ${match[1]}%`
  match = text.match(/^You need to complete "(.+)" first\.$/)
  if (match) return `Bạn cần hoàn thành “${match[1]}” trước.`
  return text
}

// Framework onboarding currently renders English literals without translation hooks.
// Restrict translation to its UI and preserve the existing elements and handlers.
export function localizeHelp(root: Element) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT)
  let node: Node | null
  while ((node = walker.nextNode())) {
    const value = node.nodeValue || ''
    const text = value.trim()
    const translated = translateHelpText(text)
    if (text && translated !== text) node.nodeValue = value.replace(text, translated)
  }
  for (const element of [root, ...root.querySelectorAll('[aria-label], [placeholder], [title]')]) {
    for (const attribute of ['aria-label', 'placeholder', 'title']) {
      const value = element.getAttribute(attribute)
      if (!value) continue
      const translated = translateHelpText(value)
      if (translated !== value) element.setAttribute(attribute, translated)
    }
  }
}

const observers = new WeakMap<Element, MutationObserver>()
export const vVietnameseHelp = {
  mounted(element: Element) {
    const translate = () => {
      localizeHelp(element)
      // The framework teleports its options menu outside the help panel.
      if (element.classList.contains('getting-started')) {
        document.querySelectorAll('[role="menuitem"], [role="tooltip"]').forEach(item => localizeHelp(item))
      }
    }
    translate()
    const observer = new MutationObserver(translate)
    observer.observe(element, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ['aria-label', 'placeholder', 'title'] })
    // The menu is teleported to body only when the user opens it.
    if (element.classList.contains('getting-started')) observer.observe(document.body, { childList: true, subtree: true })
    observers.set(element, observer)
  },
  unmounted(element: Element) {
    observers.get(element)?.disconnect()
    observers.delete(element)
  },
}
