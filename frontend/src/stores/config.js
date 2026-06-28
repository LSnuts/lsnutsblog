import { defineStore } from 'pinia'
import { ref } from 'vue'
import { configAPI } from '@/api'

export const useConfigStore = defineStore('config', () => {
  const config = ref({})
  const loading = ref(false)

  // 获取所有配置
  const fetchConfig = async () => {
    loading.value = true
    try {
      const response = await configAPI.getAllConfig()
      config.value = response.config
    } finally {
      loading.value = false
    }
  }

  // 设置单个配置
  const setConfig = async (key, value) => {
    await configAPI.setConfig({ key, value })
    config.value[key] = value
  }

  // 批量设置配置
  const batchSetConfig = async (data) => {
    await configAPI.batchSetConfig(data)
    Object.assign(config.value, data)
  }

  // 获取单个配置值
  const getConfig = (key, defaultValue = '') => {
    return config.value[key] || defaultValue
  }

  return {
    config,
    loading,
    fetchConfig,
    setConfig,
    batchSetConfig,
    getConfig
  }
})