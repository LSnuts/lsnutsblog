<template>
  <div class="messages-page">
    <div class="messages-content">
      <el-card class="messages-card">
        <template #header>
          <div class="card-header">
            <h2>留言墙</h2>
            <p class="subtitle">留下你的足迹吧~</p>
          </div>
        </template>

        <!-- 留言表单 -->
        <div class="message-form">
          <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
            <el-form-item label="昵称" prop="author">
              <el-input v-model="form.author" placeholder="请输入昵称" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入邮箱（选填）" />
            </el-form-item>
            <el-form-item label="留言" prop="content">
              <el-input
                v-model="form.content"
                type="textarea"
                :rows="4"
                placeholder="请输入留言内容..."
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="submitting" @click="handleSubmit">
                提交留言
              </el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 留言列表 -->
        <div class="messages-list">
          <div v-if="loading" class="loading">
            <el-skeleton animated>
              <template #template>
                <div v-for="i in 3" :key="i" class="message-skeleton">
                  <el-skeleton-item variant="circle" style="width: 50px; height: 50px" />
                  <div style="flex: 1">
                    <el-skeleton-item variant="text" style="width: 30%; margin-bottom: 10px" />
                    <el-skeleton-item variant="text" style="width: 100%" />
                  </div>
                </div>
              </template>
            </el-skeleton>
          </div>

          <div v-else-if="messages.length === 0" class="empty">
            <el-empty description="暂无留言，来说点什么吧~" />
          </div>

          <transition-group v-else name="message-list" tag="div" class="messages">
            <div v-for="msg in messages" :key="msg.id" class="message-item">
              <el-avatar :size="50" class="message-avatar">
                {{ msg.author?.charAt(0).toUpperCase() || 'U' }}
              </el-avatar>
              <div class="message-body">
                <div class="message-header">
                  <span class="message-author">{{ msg.author }}</span>
                  <span class="message-date">{{ formatDate(msg.created_at) }}</span>
                </div>
                <div class="message-content">{{ msg.content }}</div>
                <div v-if="msg.email" class="message-email">
                  <el-icon><Message /></el-icon>
                  {{ msg.email }}
                </div>
              </div>
            </div>
          </transition-group>

          <div v-if="pagination.total > pagination.perPage" class="pagination">
            <el-pagination
              v-model:current-page="pagination.currentPage"
              :page-size="pagination.perPage"
              :total="pagination.total"
              layout="prev, pager, next"
              @current-change="fetchMessages"
            />
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { messagesAPI } from '@/api'

const messages = ref([])
const loading = ref(false)
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({
  author: '',
  email: '',
  content: ''
})

const rules = {
  author: [
    { required: true, message: '请输入昵称', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入留言内容', trigger: 'blur' },
    { min: 5, message: '留言内容至少5个字符', trigger: 'blur' }
  ]
}

const pagination = reactive({
  currentPage: 1,
  perPage: 10,
  total: 3
})

const fetchMessages = async () => {
  loading.value = true
  try {
    const response = await messagesAPI.getMessages({
      page: pagination.currentPage,
      per_page: pagination.perPage,
      approved: true
    })
    messages.value = response.messages
    pagination.total = response.total
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await messagesAPI.createMessage({
          author: form.author,
          email: form.email,
          content: form.content
        })
        ElMessage.success('留言提交成功，等待审核！')
        resetForm()
      } finally {
        submitting.value = false
      }
    }
  })
}

const resetForm = () => {
  form.author = ''
  form.email = ''
  form.content = ''
  formRef.value?.resetFields()
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date

  // 一天内
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    if (hours < 1) {
      const minutes = Math.floor(diff / 60000)
      return minutes < 1 ? '刚刚' : `${minutes}分钟前`
    }
    return `${hours}小时前`
  }

  // 七天内
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days}天前`
  }

  // 超过七天
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchMessages()
})
</script>

<style scoped>
.messages-page {
  padding: 40px 20px;
  min-height: calc(100vh - 200px);
}

.messages-content {
  max-width: 800px;
  margin: 0 auto;
}

.messages-card {
  background-color: var(--bg-card);
  backdrop-filter: blur(8px);
  transition: background-color 0.3s;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  font-size: 28px;
  color: var(--text-primary);
}

.subtitle {
  margin: 10px 0 0;
  color: #999;
  font-size: 14px;
}

.message-form {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 30px;
}

.messages-list {
  padding: 20px 0;
}

.loading {
  padding: 20px 0;
}

.message-skeleton {
  display: flex;
  gap: 15px;
  padding: 20px 0;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-item {
  display: flex;
  gap: 15px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.message-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.message-avatar {
  flex-shrink: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: bold;
}

.message-body {
  flex: 1;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.message-author {
  font-weight: bold;
  color: #333;
  font-size: 16px;
}

.message-date {
  color: #999;
  font-size: 12px;
}

.message-content {
  color: #666;
  line-height: 1.6;
  margin-bottom: 10px;
}

.message-email {
  color: #999;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

/* 动画 */
.message-list-enter-active,
.message-list-leave-active {
  transition: all 0.5s;
}

.message-list-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.message-list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

@media (max-width: 768px) {
  .message-item {
    padding: 15px;
  }

  .message-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}
</style>