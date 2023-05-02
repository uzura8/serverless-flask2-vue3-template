import type { MediaType } from '@/types/Media'
import config from '@/configs/config.json'
import media from '@/utils/media'

export default function useMedia() {
  const mediaUrl = (serviceId: string, type: MediaType, fileId: string, mimeType: string, size = 'raw'): string => {
    const ext = media.getExtensionByMimetype(mimeType)
    const pathItems = [config.media.url, serviceId]
    if (type === 'image') {
      const fileName = `${size}.${ext}`
      pathItems.push('images', fileId, fileName)
    } else {
      const fileName = `${fileId}.${ext}`
      pathItems.push('docs', fileName)
    }
    return pathItems.join('/')
  }

  const assetUrl = (path: string) => {
    const items = [path]
    items.unshift(config.media.url)
    return items.join('/')
  }

  return { mediaUrl, assetUrl }
}
