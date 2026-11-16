import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { afterEach, describe, expect, it, vi } from 'vitest'

describe('auth page translation', () => {
  afterEach(() => { document.body.innerHTML = ''; document.body.removeAttribute('data-path') })
  it('translates asynchronously inserted login errors without removing their markup', async () => {
    document.body.dataset.path = 'login'
    document.body.innerHTML = '<div class="login-content"><div class="login-error-banner"><span class="es-alert__title"></span><i aria-hidden="true"></i></div></div>'
    const source = readFileSync(resolve(process.cwd(), '../lms/public/js/auth.js'), 'utf8')
    new Function(source)()
    const title = document.querySelector('.es-alert__title')!
    title.textContent = 'Invalid credentials, try again.'
    await vi.waitFor(() => expect(title.textContent).toBe('Email hoặc mật khẩu không chính xác. Vui lòng thử lại.'))
    expect(document.querySelector('.login-error-banner i')).not.toBeNull()
    title.textContent = 'Too many requests. Please try again later.'
    await vi.waitFor(() => expect(title.textContent).toBe('Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau.'))
  })
})
