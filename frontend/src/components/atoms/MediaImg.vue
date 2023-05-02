<template>
  <figure class="">
    <img
      :src="imageUrl"
      @error="noImageUrl"
      :class="{ 'rounded-lg': isRounded, 'cursor-pointer': isClickable }"
      class="h-auto max-w-full"
      :alt="caption ? caption : ''"
    >
    <figcaption
      v-if="caption && isDisplayCaption"
      class="mt-2 text-sm text-center text-gray-500 dark:text-gray-400"
    >{{ caption }}</figcaption>
  </figure>
</template>

<script lang="ts">
//import type { MimeTypeImage } from '@/types/Media.d'
import type { PropType } from 'vue'
import { defineComponent, computed } from 'vue'
import useMedia from '@/commons/useMedia'

//interface Props {
//  fileId: string
//  mimeType: MimeTypeImage
//  size: string
//  src: string
//  caption: string
//  sizeClass: string
//  isClickable: boolean
//  isRounded: boolean
//  isDisplayCaption: boolean
//}

export default defineComponent({
  props: {
    serviceId: {
      type: String as PropType<string>,
      default: '',
    },
    fileId: {
      type: String as PropType<string>,
      default: '',
    },
    mimeType: {
      type: String as PropType<string>,
      default: '',
    },
    size: {
      type: String as PropType<string>,
      default: 'raw',
    },
    src: {
      type: String as PropType<string>,
      default: '',
    },
    sizeClass: {
      type: String as PropType<string>,
      default: '',
    },
    caption: {
      type: String as PropType<string>,
      default: '',
    },
    isClickable: {
      type: Boolean as PropType<boolean>,
      default: false,
    },
    isRounded: {
      type: Boolean as PropType<boolean>,
      default: false,
    },
    isDisplayCaption: {
      type: Boolean as PropType<boolean>,
      default: false,
    },
  },

  setup(props) {
    const { mediaUrl, assetUrl } = useMedia()

    const imageUrl = computed((): string => {
      if (props.src) return props.src
      return mediaUrl(props.serviceId, 'image', props.fileId, props.mimeType, props.size)
    })

    const noImageUrl = (event: any): void => {
      // TODO: 型定義を追加する
      if ((event.target instanceof HTMLImageElement) === false) return
      if (event.target == null) return
      event.target.src = assetUrl('assets/img/noimage.jpg')
    }

    //const activate = () => {
    //  if (props.isClickable === false) return
    //  contexst.emit('activate', imageUrl.value)
    //}

    return {
      imageUrl,
      noImageUrl,
      //activate,
    }
  },
})
</script>

