/**
 * Формирует правильный URL для изображений из Django.
 * Django может вернуть:
 *   - "/media/image_product/photo.jpg"
 *   - "image_product/photo.jpg"
 *   - "http://localhost:8000/media/..."
 */
const BASE = 'http://localhost:8000'

export function getImageUrl(path) {
  if (!path) return null
  if (path.startsWith('http')) return path
  if (path.startsWith('/media')) return `${BASE}${path}`
  return `${BASE}/media/${path}`
}
