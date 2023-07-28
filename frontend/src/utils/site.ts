import type { MediaType } from '@/types/Media'
import config from '@/configs/config.json'
import { getExtensionByMimetype } from '@/utils/media'

export function mediaUrl(
  prefix: string,
  type: MediaType,
  fileId: string,
  mimeType: string,
  size = 'raw'
): string {
  const ext = getExtensionByMimetype(mimeType)
  const pathItems = [config.media.url, prefix]
  if (type === 'image') {
    const fileName = `${size}.${ext}`
    pathItems.push('images', fileId, fileName)
  } else {
    const fileName = `${fileId}.${ext}`
    pathItems.push('docs', fileName)
  }
  return pathItems.join('/')
}

export function assetUrl(path: string): string {
  const items = [path]
  items.unshift(config.media.url)
  return items.join('/')
}
