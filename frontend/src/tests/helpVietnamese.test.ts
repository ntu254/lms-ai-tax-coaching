import { describe, expect, it, vi } from 'vitest'
import { localizeHelp, translateHelpText, vVietnameseHelp } from '@/utils/helpVietnamese'

describe('Vietnamese help interface', () => {
  it('translates framework labels and progress without changing unknown content', () => {
    expect(translateHelpText('Getting started')).toBe('Bắt đầu')
    expect(translateHelpText('2/8 steps completed')).toBe('Đã hoàn thành 2/8 bước')
    expect(translateHelpText('50% completed')).toBe('Đã hoàn thành 50%')
    expect(translateHelpText('You need to complete "Tạo khóa học đầu tiên" first.')).toBe('Bạn cần hoàn thành “Tạo khóa học đầu tiên” trước.')
    expect(translateHelpText('Nội dung khác')).toBe('Nội dung khác')
  })
  it('preserves controls and localizes text inserted after mounting', async () => {
    const root = document.createElement('div')
    root.innerHTML = '<button aria-label="Close"><span>Skip all</span></button><input placeholder="Search articles...">'
    document.body.append(root)
    vVietnameseHelp.mounted(root)
    expect(root.querySelector('button')?.getAttribute('aria-label')).toBe('Đóng')
    expect(root.querySelector('button span')?.textContent).toBe('Bỏ qua tất cả')
    expect(root.querySelector('input')?.getAttribute('placeholder')).toBe('Tìm bài viết...')
    root.querySelector('button span')!.textContent = 'Reset all'
    await vi.waitFor(() => expect(root.querySelector('button span')?.textContent).toBe('Đặt lại tất cả'))
    vVietnameseHelp.unmounted(root)
    root.remove()
  })
})
