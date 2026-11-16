import { describe, expect, it } from 'vitest'
import { formatMoney } from '@/utils/money'

describe('money formatting', () => {
	it('formats Vietnamese đồng with Vietnamese digit grouping', () => {
		expect(formatMoney(1234567, 'VND').replace(/\s/g, ' ')).toBe('1.234.567 ₫')
	})

	it('formats numeric strings and zero instead of dropping them', () => {
		expect(formatMoney('1234567', 'VND').replace(/\s/g, ' ')).toBe('1.234.567 ₫')
		expect(formatMoney(0, 'VND').replace(/\s/g, ' ')).toBe('0 ₫')
	})

	it('keeps fractional amounts for currencies that use them', () => {
		expect(formatMoney(12.5, 'USD')).toBe(
			new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(12.5)
		)
	})

	it('handles missing or invalid currency information', () => {
		expect(formatMoney(null, 'VND')).toBe('')
		expect(formatMoney(123, null)).toBe('123')
		expect(formatMoney(123, 'invalid')).toBe('123 invalid')
	})
})
