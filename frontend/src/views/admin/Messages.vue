<template>
  <div class="admin-messages">
    <div class="header-row">
      <h2 class="page-title">留言管理</h2>
    </div>

    <el-card shadow="hover">
      <div v-if="loading" class="loading">
        <el-skeleton animated>
          <template #template>
            <el-skeleton-item variant="p" style="width: 100%; height: 200px" />
          </template>
        </el-skeleton>
      </div>

      <div v-else-if="messages.length === 0" class="empty">
        <el-empty description="暂无留言" />
      </div>

      <div v-else class="messages-list">
        <div v-for="msg in messages" :key="msg.id" class="message-item">
          <div class="message-header">
            <div class="message-user">
              <el-avatar :size="40" class="msg-avatar">
                {{ msg.author?.charAt(0).toUpperCase() || 'U' }}
              </el-avatar>
              <div class="user-info">
                <span class="author-name">{{ msg.author }}</span>
                <span class="message-date">{{ formatDate(msg.created_at) }}</span>
              </div>
            </div>
            <div class="message-actions">
              <el-switch
                v-model="msg.is_approved"
                active-text="已审核"
                inactive-text="待审核"
                @change="handleToggleApproved(msg)"
              />
              <el-button type="primary" size="small" @click="openReplyDialog(msg)">
                {{ msg.reply ? '编辑回复' : '回复' }}
              </el-button>
              <el-popconfirm title="确定删除这条留言？" @confirm="handleDelete(msg)">
                <template #reference>
                  <el-button type="danger" size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>

          <div class="message-content">
            {{ msg.content }}
          </div>

          <div v-if="msg.email" class="message-email">
            <el-icon><Message /></el-icon> {{ msg.email }}
          </div>

          <div v-if="msg.reply" class="message-reply">
            <div class="reply-label">
              <el-icon><ChatDotSquare /></el-icon>
              <span>管理员回复：</span>
            </div>
            <div class="reply-content">{{ msg.reply }}</div>
          </div>
        </div>
      </div>

      <div v-if="total > pageSize" class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="fetchMessages"
        />
      </div>
    </el-card>

    <!-- 回复对话框 -->
    <el-dialog v-model="replyDialogVisible" :title="'回复 - ' + (replyTarget?.author || '')" width="500px">
      <el-input
        v-model="replyContent"
        type="textarea"
        :rows="4"
        placeholder="请输入回复内容..."
      />
      <template #footer>
        <el-button @click="replyDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="replyLoading" @click="handleReply">
          确定回复
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { messagesAPI } from '@/api'
import { ElMessage } from 'element-plus'

const messages = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const replyDialogVisible = ref(false)
const replyContent = ref('')
const replyTarget = ref(null)
const replyLoading = ref(false)

const fetchMessages = async () => {
  loading.value = true
  try {
    const response = await messagesAPI.getMessages({
      page: currentPage.value,
      per_page: pageSize.value
    })
    messages.value = response.messages
    total.value = response.total
  } finally {
    loading.value = false
  }
}

const handleToggleApproved = async (msg) => {
  try {
    await messagesAPI.updateMessage(msg.id, { is_approved: msg.is_approved })
    ElMessage.success(msg.is_approved ? '留言已审核通过' : '留言已取消审核')
  } catch {
    msg.is_approved = !msg.is_approved
  }
}

const openReplyDialog = (msg) => {
  replyTarget.value = msg
  replyContent.value = msg.reply || ''
  replyDialogVisible.value = true
}

const handleReply = async () => {
  if (!replyTarget.value || !replyContent.value.trim()) return

  replyLoading.value = true
  try {
    const response = await messagesAPI.updateMessage(replyTarget.value.id, {
      reply: replyContent.value,
      is_approved: true
    })
    replyTarget.value.reply = response.data.reply
    replyTarget.value.is_approved = true
    replyDialogVisible.value = false
    ElMessage.success('回复成功')
  } finally {
    replyLoading.value = false
  }
}

const handleDelete = async (msg) => {
  try {
    await messagesAPI.deleteMessage(msg.id)
    messages.value = messages.value.filter(m => m.id !== msg.id)
    total.value--
    ElMessage.success('留言已删除')
  } catch {
    // 错误已在拦截器处理
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchMessages()
})
</script>

<style scoped>
.admin-messages {
  padding: 20px;
}

.page-title {
  margin: 0 0 20px;
  font-size: 24px;
  color: #303133;
}

.loading {
  padding: 40px;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  transition: all 0.3s;
}

.message-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  flex-wrap: wrap;
  gap: 10px;
}

.message-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author-name {
  font-weight: bold;
  color: #333;
}

.message-date {
  font-size: 12px;
  color: #999;
}

.message-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.message-content {
  font-size: 15px;
  line-height: 1.6;
  color: #444;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.message-email {
  font-size: 12px;
  color: #999;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 10px;
}

.message-reply {
  margin-top: 12px;
  padding: 12px;
  background-color: #f0f9ff;
  border-left: 3px solid #409eff;
  border-radius: 4px;
}

.reply-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: #409eff;
  font-weight: bold;
  margin-bottom: 6px;
}

.reply-content {
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.msg-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
</style>