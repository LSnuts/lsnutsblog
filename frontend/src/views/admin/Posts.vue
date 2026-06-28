<template>
  <div class="posts-management">
    <div class="page-header">
      <h2 class="page-title">文章管理</h2>
      <router-link to="/admin/posts/new">
        <el-button type="primary">
          <el-icon><Plus /></el-icon>
          新建文章
        </el-button>
      </router-link>
    </div>

    <el-card shadow="hover">
      <el-table
        v-loading="loading"
        :data="posts"
        style="width: 100%"
      >
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_published ? 'success' : 'info'">
              {{ row.is_published ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="views" label="浏览量" width="100" />
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="更新时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <router-link :to="`/admin/posts/${row.id}/edit`">
              <el-button type="primary" text size="small">编辑</el-button>
            </router-link>
            <el-button
              type="danger"
              text
              size="small"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="pagination.total > pagination.perPage" class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          :page-size="pagination.perPage"
          :total="pagination.total"
          layout="total, prev, pager, next"
          @current-change="fetchPosts"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { postsAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const posts = ref([])
const pagination = reactive({
  currentPage: 1,
  perPage: 10,
  total: 0
})

const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await postsAPI.getPosts({
      page: pagination.currentPage,
      per_page: pagination.perPage,
      published: false
    })
    posts.value = response.posts
    pagination.total = response.total
  } finally {
    loading.value = false
  }
}

const handleDelete = (post) => {
  ElMessageBox.confirm(
    `确定要删除文章 "${post.title}" 吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await postsAPI.deletePost(post.id)
      ElMessage.success('文章已删除')
      fetchPosts()
    } catch (error) {
      // 错误已在拦截器中处理
    }
  })
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
  fetchPosts()
})
</script>

<style scoped>
.posts-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>