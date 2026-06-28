<template>
  <div class="custom-page">
    <div v-if="loading" class="loading"><el-skeleton animated><el-skeleton-item variant="p" style="width:100%;height:300px" /></el-skeleton></div>
    <el-alert v-else-if="error" :title="error" type="error" center />
    <div v-else-if="page" class="page-content">
      <h1 class="page-title">{{ page.title }}</h1>
      <div class="page-body markdown-body" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { pagesAPI } from '@/api'

const route = useRoute()
const page = ref(null)
const loading = ref(true)
const error = ref('')

const renderedContent = computed(() => {
  if (!page.value?.content) return ''
  // Simple markdown-like rendering
  let html = page.value.content
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/### (.+)/g, '<h3>$1</h3>')
    .replace(/## (.+)/g, '<h2>$1</h2>')
    .replace(/# (.+)/g, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/- (.+)/g, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br/>')
  return '<p>' + html + '</p>'
})

onMounted(async () => {
  try {
    const res = await pagesAPI.getPage(route.params.slug)
    if (!res.page.is_published) {
      error.value = '该页面未发布'
    } else {
      page.value = res.page
    }
  } catch (e) {
    error.value = '页面不存在'
  } finally { loading.value = false }
})
</script>

<style scoped>
.custom-page { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
.page-title { font-size: 28px; color: var(--text-primary); margin-bottom: 30px; }
.page-body { font-size: 15px; line-height: 1.8; color: var(--text-secondary); }
.loading { padding: 40px; }
</style>