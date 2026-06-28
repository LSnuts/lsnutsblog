<template>
  <div class="home-page">
    <div class="container">
      <!-- 左侧边栏 - 个人信息 -->
      <aside class="sidebar-left">
        <el-card class="profile-card">
          <div class="profile-header">
            <el-avatar :size="100" :src="configStore.getConfig('avatar') || undefined">
              <el-icon :size="50"><User /></el-icon>
            </el-avatar>
            <h2 class="profile-name">{{ configStore.getConfig('author_name', '博主') }}</h2>
            <p class="profile-signature">{{ configStore.getConfig('signature', '这个人很懒，什么都没写') }}</p>
          </div>
          <div class="profile-stats">
            <div class="stat-item">
              <span class="stat-value">{{ stats.posts }}</span>
              <span class="stat-label">文章</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ stats.views }}</span>
              <span class="stat-label">阅读</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ stats.messages }}</span>
              <span class="stat-label">留言</span>
            </div>
          </div>
          <div class="profile-links">
            <a v-if="configStore.getConfig('github')" :href="configStore.getConfig('github')" target="_blank">
              <el-icon><Link /></el-icon> GitHub
            </a>
            <a v-if="configStore.getConfig('email')" :href="'mailto:' + configStore.getConfig('email')">
              <el-icon><Message /></el-icon> 邮箱
            </a>
          </div>
        </el-card>
      </aside>

      <!-- 中间主内容区 - 文章列表 -->
      <section class="main-area">
        <div v-if="searchQuery" class="search-results-header">
          <h3>搜索结果: "{{ searchQuery }}"</h3>
          <el-button @click="clearSearch">清除搜索</el-button>
        </div>

        <div v-if="loading" class="loading">
          <el-skeleton animated>
            <template #template>
              <div v-for="i in 3" :key="i" class="post-item-skeleton">
                <el-skeleton-item variant="h3" style="width: 80%" />
                <el-skeleton-item variant="text" style="width: 100%; margin-top: 10px" />
                <el-skeleton-item variant="text" style="width: 60%; margin-top: 10px" />
              </div>
            </template>
          </el-skeleton>
        </div>

        <div v-else-if="posts.length === 0" class="empty">
          <el-empty :description="searchQuery ? '没有找到相关文章' : '暂无文章'" />
        </div>

        <transition-group v-else name="post-list" tag="div" class="posts-list">
          <el-card
            v-for="post in posts"
            :key="post.id"
            class="post-card"
            shadow="hover"
            @click="viewPost(post.id)"
          >
            <div class="post-header">
              <h3 class="post-title">{{ post.title }}</h3>
              <el-tag v-if="post.is_published" type="success" size="small">已发布</el-tag>
              <el-tag v-else type="info" size="small">草稿</el-tag>
            </div>
            <p class="post-summary">{{ post.summary || truncateContent(post.content) }}</p>
            <div class="post-meta">
              <span><el-icon><Calendar /></el-icon> {{ formatDate(post.created_at) }}</span>
              <span><el-icon><View /></el-icon> {{ post.views }} 阅读</span>
              <span><el-icon><User /></el-icon> {{ post.author }}</span>
            </div>
          </el-card>
        </transition-group>

        <div v-if="pagination.total > pagination.perPage" class="pagination">
          <el-pagination
            v-model:current-page="pagination.currentPage"
            :page-size="pagination.perPage"
            :total="pagination.total"
            layout="prev, pager, next"
            @current-change="fetchPosts"
          />
        </div>
      </section>

      <!-- 右侧边栏 - 日历 -->
      <aside class="sidebar-right">
        <el-card class="calendar-card">
          <template #header>
            <div class="calendar-header">
              <span>{{ currentMonth }}</span>
              <div class="calendar-nav">
                <el-button text @click="prevMonth">
                  <el-icon><ArrowLeft /></el-icon>
                </el-button>
                <el-button text @click="nextMonth">
                  <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
            </div>
          </template>
          <div class="calendar-grid">
            <div class="calendar-weekday">
              <span v-for="day in weekDays" :key="day">{{ day }}</span>
            </div>
            <div class="calendar-days">
              <span
                v-for="(day, index) in calendarDays"
                :key="index"
                :class="{
                  'other-month': day.otherMonth,
                  'has-post': hasPostOnDate(day.date)
                }"
              >
                {{ day.day }}
              </span>
            </div>
          </div>
        </el-card>

        <el-card class="tags-card">
          <template #header>
            <span>标签云</span>
          </template>
          <div class="tags-list">
            <el-tag
              v-for="tag in tags"
              :key="tag"
              class="tag-item"
              type="info"
            >
              {{ tag }}
            </el-tag>
          </div>
        </el-card>

        <el-card class="recent-posts-card">
          <template #header>
            <span>最新文章</span>
          </template>
          <div class="recent-posts-list">
            <div
              v-for="post in recentPosts"
              :key="post.id"
              class="recent-post-item"
              @click="viewPost(post.id)"
            >
              {{ post.title }}
            </div>
          </div>
        </el-card>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useConfigStore } from '@/stores/config'
import { postsAPI } from '@/api'

const router = useRouter()
const route = useRoute()
const configStore = useConfigStore()

const posts = ref([])
const recentPosts = ref([])
const loading = ref(false)
const searchQuery = ref('')
const currentDate = ref(new Date())

const pagination = reactive({
  currentPage: 1,
  perPage: 10,
  total: 0
})

const stats = reactive({
  posts: 0,
  views: 0,
  messages: 0
})

const tags = ref(['Vue', 'Python', 'Flask', 'PostgreSQL', 'JavaScript'])

const weekDays = ['日', '一', '二', '三', '四', '五', '六']

const currentMonth = computed(() => {
  const date = currentDate.value
  return `${date.getFullYear()}年${date.getMonth() + 1}月`
})

const calendarDays = computed(() => {
  const date = currentDate.value
  const year = date.getFullYear()
  const month = date.getMonth()

  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startWeekday = firstDay.getDay()
  const daysInMonth = lastDay.getDate()

  const days = []

  // 上个月的天数
  for (let i = startWeekday - 1; i >= 0; i--) {
    const d = new Date(year, month, -i)
    days.push({
      day: d.getDate(),
      date: d.toISOString().split('T')[0],
      otherMonth: true
    })
  }

  // 当前月的天数
  for (let i = 1; i <= daysInMonth; i++) {
    const d = new Date(year, month, i)
    days.push({
      day: i,
      date: d.toISOString().split('T')[0],
      otherMonth: false
    })
  }

  // 下个月的天数
  const remaining = 42 - days.length
  for (let i = 1; i <= remaining; i++) {
    const d = new Date(year, month + 1, i)
    days.push({
      day: i,
      date: d.toISOString().split('T')[0],
      otherMonth: true
    })
  }

  return days
})

const fetchPosts = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      per_page: pagination.perPage,
      published: true
    }

    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    const response = await postsAPI.getPosts(params)
    posts.value = response.posts
    pagination.total = response.total

    // 更新统计数据
    stats.posts = response.total
    stats.views = response.posts.reduce((sum, p) => sum + p.views, 0)

    // 获取最新文章
    if (!searchQuery.value) {
      const recentResponse = await postsAPI.getPosts({ page: 1, per_page: 5, published: true })
      recentPosts.value = recentResponse.posts
    }
  } finally {
    loading.value = false
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  pagination.currentPage = 1
  fetchPosts()
}

const viewPost = (id) => {
  router.push({ name: 'Post', params: { id } })
}

const truncateContent = (content) => {
  if (!content) return ''
  const text = content.replace(/[#*`>\-\n]/g, '').trim()
  return text.length > 150 ? text.substring(0, 150) + '...' : text
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const prevMonth = () => {
  const date = currentDate.value
  date.setMonth(date.getMonth() - 1)
  currentDate.value = new Date(date)
}

const nextMonth = () => {
  const date = currentDate.value
  date.setMonth(date.getMonth() + 1)
  currentDate.value = new Date(date)
}

const hasPostOnDate = (dateString) => {
  return posts.value.some(post => {
    const postDate = new Date(post.created_at).toISOString().split('T')[0]
    return postDate === dateString
  })
}

// 监听路由查询参数变化
watch(() => route.query.search, (newSearch) => {
  if (newSearch) {
    searchQuery.value = newSearch
    pagination.currentPage = 1
    fetchPosts()
  }
}, { immediate: true })

onMounted(() => {
  if (!route.query.search) {
    fetchPosts()
  }
  configStore.fetchConfig()
})
</script>

<style scoped>
.home-page {
  padding: 30px 20px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 30px;
}

/* 左侧边栏 */
.sidebar-left {
  position: sticky;
  top: 90px;
  height: fit-content;
}

.profile-card {
  text-align: center;
}

.profile-header {
  padding: 20px 0;
}

.profile-name {
  margin: 15px 0 5px;
  font-size: 20px;
}

.profile-signature {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  margin: 20px 0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

.profile-links {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.profile-links a {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.profile-links a:hover {
  color: #409eff;
}

/* 中间主内容区 */
.main-area {
  min-height: 500px;
}

.search-results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background-color: white;
  border-radius: 8px;
}

.search-results-header h3 {
  margin: 0;
}

.loading {
  padding: 20px;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-card {
  cursor: pointer;
  transition: all 0.3s;
}

.post-card:hover {
  transform: translateX(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.post-title {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.post-summary {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
}

.post-meta {
  display: flex;
  gap: 20px;
  color: #999;
  font-size: 12px;
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

/* 右侧边栏 */
.sidebar-right {
  position: sticky;
  top: 90px;
  height: fit-content;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.calendar-card {
  overflow: hidden;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.calendar-nav {
  display: flex;
  gap: 5px;
}

.calendar-grid {
  padding: 10px 0;
}

.calendar-weekday {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-size: 12px;
  color: #999;
  margin-bottom: 10px;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.calendar-days span {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  font-size: 12px;
  border-radius: 50%;
}

.calendar-days span.other-month {
  color: #ccc;
}

.calendar-days span.has-post {
  background-color: #409eff;
  color: white;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: pointer;
}

.tag-item:hover {
  transform: scale(1.1);
}

.recent-posts-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.recent-post-item {
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.recent-post-item:hover {
  background-color: #f5f5f5;
  border-left-color: #409eff;
  color: #409eff;
  padding-left: 12px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .container {
    grid-template-columns: 250px 1fr 250px;
    gap: 20px;
  }
}

@media (max-width: 992px) {
  .container {
    grid-template-columns: 1fr;
  }

  .sidebar-left,
  .sidebar-right {
    position: static;
  }
}

/* 动画 */
.post-list-enter-active,
.post-list-leave-active {
  transition: all 0.5s;
}

.post-list-enter-from,
.post-list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>