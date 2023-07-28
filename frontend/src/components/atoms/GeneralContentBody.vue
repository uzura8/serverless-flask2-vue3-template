<script lang="ts">
import type { PropType } from 'vue'
import { defineComponent, computed } from 'vue'
import { nl2br, link2url } from '@/utils/str'

export default defineComponent({
  components: {},

  props: {
    body: {
      type: String as PropType<string>,
      required: true
    },
    isNl2br: {
      type: Boolean as PropType<boolean>,
      default: true
    },
    isLink2url: {
      type: Boolean as PropType<boolean>,
      default: true
    }
  },

  setup(props) {
    const covertedBody = computed(() => {
      let body = props.body
      if (props.isNl2br) {
        body = nl2br(body)
      }
      if (props.isLink2url) {
        body = link2url(body, true, 'text-blue-600 dark:text-blue-500 hover:underline')
      }
      return body
    })

    return {
      covertedBody
    }
  }
})
</script>

<template>
  <div v-html="$sanitize(covertedBody)"></div>
</template>
