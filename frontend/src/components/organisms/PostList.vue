<script lang="ts">
import type { PostPublic, PagerKey } from '@/types/Post.d'
import type { PropType } from 'vue'
import { defineComponent, reactive, ref, computed, onBeforeMount } from 'vue'
import { PostApi } from '@/apis'
import { useGlobalLoaderStore } from '@/stores/globalLoader'
import PostListItem from '@/components/organisms/PostListItem.vue'

// Types
interface Params {
  pagerKey?: string
}

export default defineComponent({
  components: {
    PostListItem
  },

  props: {
    serviceId: {
      type: String as PropType<string>,
      default: ''
    }
  },

  setup(props) {
    // data
    let posts = ref([] as PostPublic[])
    let pagerKey = reactive({} as PagerKey)

    // store
    const globalLoader = useGlobalLoaderStore()

    // computed
    const hasNext = computed(() => Boolean(pagerKey))

    // methods
    const setPostList = async () => {
      globalLoader.updateLoading(true)
      try {
        let params: Params = {}
        if (Object.keys(pagerKey).length > 0) {
          params.pagerKey = JSON.stringify(pagerKey)
        }
        const res = await PostApi.getList(props.serviceId, params)
        res.items.map((item: PostPublic) => {
          posts.value.push(item)
        })
        pagerKey = res.pagerKey
        globalLoader.updateLoading(false)
      } catch (error) {
        console.log(error)
        globalLoader.updateLoading(false)
      }
    }

    onBeforeMount(async () => {
      await setPostList()
    })

    return {
      posts,
      pagerKey,
      setPostList,
      hasNext
    }
  }
})
</script>

<template>
  <div>
    <div
      v-if="posts.length"
      class="grid grid-cols-1 gap-6"
    >
      <PostListItem
        v-for="post in posts"
        :key="post.postId"
        :post="post"
      />
      <div
        v-if="hasNext"
        class="text-center"
      >
        <a
          @click="setPostList"
          class="cursor-pointer text-blue-600 hover:text-blue-800"
        >
          {{ $t('common.more') }}
        </a>
      </div>
    </div>

    <div v-else>
      <p class="text-gray-500 text-center">{{ $t('msg.noData') }}</p>
    </div>
  </div>
</template>
