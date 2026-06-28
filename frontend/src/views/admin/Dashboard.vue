<template>
  <div class="dashboard">
    <h2 class="page-title">仪表盘</h2>

    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #409EFF">
            <el-icon :size="30"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.posts }}</div>
            <div class="stat-label">文章总数</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #67C23A">
            <el-icon :size="30"><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.published }}</div>
            <div class="stat-label">已发布</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #E6A23C">
            <el-icon :size="30"><Edit /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.drafts }}</div>
            <div class="stat-label">草稿</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #F56C6C">
            <el-icon :size="30"><View /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.views }}</div>
            <div class="stat-label">总浏览</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>最新文章</span>
              <router-link to="/admin/posts">
                <el-button type="primary" text>查看全部</el-button>
              </router-link>
            </div>
          </template>

          <el-table :data="recentPosts" style="width: 100%">
            <el-table-column prop="title" label="标题" min-width="200" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_published ? 'success' : 'info'">
                  {{ row.is_published ? '已发布' : '草稿' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="views" label="浏览量" width="100" />
            <el-table-column label="发布时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <router-link :to="`/admin/posts/${row.id}/edit`">
                  <el-button type="primary" text size="small">编辑</el-button>
                </router-link>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { postsAPI } from '@/api'

const stats = reactive({
  posts: 0,
  published: 0,
  drafts: 0,
  views: 0
})

const recentPosts = ref([])

const fetchStats = async () => {
  try {
    const response = await postsAPI.getPosts({ page: 1, per_page: 100, published: false })
    const posts = response.posts

    stats.posts = response.total
    stats.published = posts.filter(p => p.is_published).length
    stats.drafts = posts.filter(p => !p.is_published).length
    stats.views = posts.reduce((sum, p) => sum + p.views, 0)

    recentPosts.value = posts.slice(0, 5)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #303133;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  width: 100%;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>