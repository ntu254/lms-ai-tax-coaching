/** Format VND in the familiar Vietnamese grouping, independent of browser language. */
export function formatMoney(
	amount: number | string | null | undefined,
	currency: string | null | undefined
): string {
	if (amount === null || amount === undefined || amount === '') return ''
	if (!currency) return String(amount)

	const value = Number(amount)
	if (!Number.isFinite(value)) return `${amount} ${currency}`

	try {
		return new Intl.NumberFormat(currency === 'VND' ? 'vi-VN' : undefined, {
			style: 'currency',
			currency,
		}).format(value)
	} catch {
		return `${amount} ${currency}`
	}
}
