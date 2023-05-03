import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { config } from '@/configs'

interface LoadingItem {
  status: boolean
  key: string
}

export const useGlobalLoaderStore = defineStore('globalLoader', () => {
  // state
  const loadingItems = ref<LoadingItem[]>([])
  const loadingTimerId = ref<number>(0)

  // getter
  const isLoading = computed(() => loadingItems.value.length > 0)

  const resetLoading = (): void => {
    if (isLoading.value === false) return
    loadingItems.value.splice(0, loadingItems.value.length)
    clearTimeout(loadingTimerId.value)
    loadingTimerId.value = 0
  }

  const updateLoading = (status: boolean, key = 'item'): void => {
    const loadingItem = {
      status: status,
      key: key
    }

    const isStart = loadingItems.value.length === 0 && status === true
    if (status === true) {
      loadingItems.value.push(loadingItem)
    } else {
      const idx = loadingItems.value.findIndex((item) => item.key === key)
      if (idx !== -1) loadingItems.value.splice(idx, 1)
    }
    const isFinish = loadingItems.value.length === 0 && status === false

    if (isStart) {
      if (!loadingTimerId.value) {
        loadingTimerId.value = window.setTimeout(() => {
          resetLoading()
        }, config.common.loadingTimeoutThreshold)
      }
    } else if (isFinish) {
      // If loading items not exists, clear timer
      resetLoading()
    }
  }

  return { isLoading, updateLoading }
})
