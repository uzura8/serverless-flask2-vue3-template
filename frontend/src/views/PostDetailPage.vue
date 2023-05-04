<script lang="ts">
import type { PostPublic } from '@/types/Post.d'
import { defineComponent, computed, ref, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import { config } from '@/configs'
import { obj, date } from '@/utils'
import { PostApi } from '@/apis'
import PostBody from '@/components/atoms/PostBody.vue'

export default defineComponent({
  components: {
    PostBody
  },

  setup() {
    const route = useRoute()

    const serviceId = config.post.serviceId
    const globalLoader = useGlobalLoaderStore()

    const slug = computed(() => {
      return route.params.slug ? (route.params.slug as string) : ''
    })

    const previewToken = computed(() => {
      return route.query.previewToken ? (route.query.previewToken as string) : ''
    })

    let post = ref({} as PostPublic)
    const setPost = async () => {
      globalLoader.updateLoading(true)
      try {
        const params = previewToken.value ? { token: previewToken.value } : ''
        post.value = await PostApi.getOne(serviceId, slug.value, params)
        globalLoader.updateLoading(false)
      } catch (error) {
        console.log(error)
        globalLoader.updateLoading(false)
      }
    }

    onBeforeMount(async () => {
      await setPost()
    })

    return {
      post,
      serviceId,
      dateFomat: date.formatDate,
      hasKey: obj.hasKey,
      setPost
    }
  }
})
</script>

<template>
  <div v-if="post">
    <div class="block">
      <RouterLink to="/posts/">
        <i class="fas fa-chevron-left"></i>
        <span>{{ $t('common.posts') }}</span>
      </RouterLink>
    </div>

    <h1 class="text-4xl font-extrabold dark:text-white">{{ post.title }}</h1>
    <div class="container mx-auto py-8">
      <PostBody
        v-if="post.bodyHtml"
        :body="post.bodyHtml"
      />
      <div class="">
        <time
          itemprop="datepublished"
          :datetime="dateFomat(post.publishAt)"
          >{{ dateFomat(post.publishAt) }}</time
        >
      </div>

      <ul v-if="hasKey(post, 'tags', true)">
        <li
          v-for="tag in post.tags"
          :key="tag.tagId"
          class="is-inline-block"
        >
          <RouterLink
            :to="`/posts/tags/${tag.label}`"
            class=""
            >{{ tag.label }}</RouterLink
          >
        </li>
      </ul>
    </div>
  </div>
</template>
