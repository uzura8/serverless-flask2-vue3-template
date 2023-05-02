import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useGlobalHeaderStore = defineStore('globalHeader', () => {
  const isMenuOpen = ref(false)

  const updateMenuOpenStatus = (status: boolean): void => {
    isMenuOpen.value = status
  }

  return { isMenuOpen, updateMenuOpenStatus }
})
