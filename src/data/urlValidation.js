function webUrl(value, base = 'https://site.invalid') {
  if (!value) return ''
  try {
    const url = new URL(value, base)
    return ['https:', 'http:'].includes(url.protocol) ? url : null
  } catch {
    return null
  }
}

export function safeDownloadUrl(value, base) {
  return webUrl(value, base)?.href || ''
}

export function safeWebPlayerUrl(value, base) {
  const url = webUrl(value, base)
  if (!url || /\.(exe|apk|zip|7z|rar|tar|gz|dmg|appimage)$/i.test(url.pathname)) return ''
  return url.href
}

export function isSameOrigin(value, origin) {
  const url = webUrl(value, origin)
  return Boolean(url && url.origin === origin)
}
