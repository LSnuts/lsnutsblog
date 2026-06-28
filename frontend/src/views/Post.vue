<template>
  <div class="post-container">
    <el-skeleton v-if="loading" animated>
      <template #template>
        <el-skeleton-item variant="h1" style="width: 80%" />
        <el-skeleton-item variant="text" style="width: 40%; margin-top: 20px" />
        <div style="margin-top: 30px">
          <el-skeleton-item variant="text" style="width: 100%" />
          <el-skeleton-item variant="text" style="width: 100%; margin-top: 16px" />
          <el-skeleton-item variant="text" style="width: 80%; margin-top: 16px" />
        </div>
      </template>
    </el-skeleton>

    <article v-else-if="post" class="post">
      <header class="post-header">
        <router-link to="/" class="back-link">
          <el-icon><ArrowLeft /></el-icon>
          返回首页
        </router-link>
        <h1 class="post-title">{{ post.title }}</h1>
        <div class="post-meta">
          <span><el-icon><User /></el-icon> {{ post.author }}</span>
          <span><el-icon><Calendar /></el-icon> {{ formatDate(post.created_at) }}</span>
          <span><el-icon><View /></el-icon> {{ post.views }} 阅读</span>
        </div>
      </header>

      <div v-if="post.cover_image" class="post-cover">
        <img :src="post.cover_image" :alt="post.title" />
      </div>

      <div class="post-content" v-html="renderedContent"></div>
    </article>

    <el-empty v-else description="文章不存在" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { postsAPI } from '@/api'
import { marked } from 'marked'
import 'highlight.js/styles/github.css'

const route = useRoute()
const post = ref(null)
const loading = ref(true)

const renderedContent = computed(() => {
  if (!post.value?.content) return ''

  marked.setOptions({
    highlight: function(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(code, { language: lang }).value
        } catch (err) {}
      }
      return hljs.highlightAuto(code).value
    },
    breaks: true,
    gfm: true
  })

  return marked(post.value.content)
})

const fetchPost = async () => {
  loading.value = true
  try {
    const response = await postsAPI.getPost(route.params.id)
    post.value = response.post
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.post-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.post-header {
  margin-bottom: 40px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #409eff;
  text-decoration: none;
  margin-bottom: 20px;
  transition: opacity 0.3s;
}

.back-link:hover {
  opacity: 0.8;
}

.post-title {
  font-size: 36px;
  color: #303133;
  margin-bottom: 20px;
}

.post-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.post-cover {
  width: 100%;
  margin-bottom: 40px;
  border-radius: 8px;
  overflow: hidden;
}

.post-cover img {
  width: 100%;
  display: block;
}

.post-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
}

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4),
.post-content :deep(h5),
.post-content :deep(h6) {
  margin-top: 30px;
  margin-bottom: 15px;
  color: #303133;
}

.post-content :deep(p) {
  margin-bottom: 20px;
}

.post-content :deep(code) {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
}

.post-content :deep(pre) {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 20px;
}

.post-content :deep(pre code) {
  background: none;
  padding: 0;
}

.post-content :deep(ul),
.post-content :deep(ol) {
  margin-bottom: 20px;
  padding-left: 30px;
}

.post-content :deep(li) {
  margin-bottom: 10px;
}

.post-content :deep(blockquote) {
  border-left: 4px solid #409eff;
  padding-left: 20px;
  margin: 20px 0;
  color: #606266;
}

.post-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 20px 0;
}

.post-content :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.post-content :deep(a:hover) {
  text-decoration: underline;
}
</style>