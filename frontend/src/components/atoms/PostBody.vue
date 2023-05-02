<template>
  <div
    v-html="body"
    class="post-body"
  ></div>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import { defineComponent, onMounted } from 'vue'

import 'highlight.js/styles/atom-one-dark.css'
import hljs from 'highlight.js'

export default defineComponent({
  components: {},

  props: {
    body: {
      type: String as PropType<String>,
      required: true
    }
  },

  setup() {
    onMounted(() => {
      hljs.highlightAll()
    })

    return {}
  }
})
</script>
<style lang="scss">
.post-body {
  @import '@/styles/browser-default.scss';
  pre {
    padding: 0 0;
  }
}
</style>
