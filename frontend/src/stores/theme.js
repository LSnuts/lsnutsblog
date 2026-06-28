import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(localStorage.getItem('theme-dark') === 'true')

  const themeClass = computed(() => isDark.value ? 'dark-mode' : '')

  const toggle = () => {
    isDark.value = !isDark.value
    localStorage.setItem('theme-dark', isDark.value.toString())
    applyTheme()
  }

  const applyTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark-mode')
    } else {
      document.documentElement.classList.remove('dark-mode')
    }
  }

  const init = () => {
    applyTheme()
  }

  return { isDark, themeClass, toggle, init }
})
