<template>
  <div class="layout-container" :style="backgroundStyle">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-content">
        <div class="nav-left">
          <h1 class="site-title" @click="$router.push('/')">{{ configStore.getConfig('title', '我的博客') }}</h1>
        </div>
        <div class="nav-center">
          <el-menu
            mode="horizontal"
            :default-active="activeMenu"
            router
            class="nav-menu"
          >
            <el-menu-item index="/">主页</el-menu-item>
            <el-menu-item index="/about">关于我</el-menu-item>
            <el-menu-item index="/messages">留言墙</el-menu-item>
          </el-menu>
        </div>
        <div class="nav-right">
          <el-input
            v-model="searchQuery"
            placeholder="全文搜索..."
            class="search-input"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <router-link v-if="authStore.isAuthenticated" to="/admin" class="admin-link">
            <el-button type="primary">管理后台</el-button>
          </router-link>
          <router-link v-else to="/login" class="login-link">
            <el-button type="primary">登录</el-button>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <p>{{ configStore.getConfig('footer', '© 2024 我的博客') }}</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useConfigStore } from '@/stores/config'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const configStore = useConfigStore()

const searchQuery = ref('')
const activeMenu = computed(() => route.path)

const backgroundStyle = computed(() => {
  const bg = configStore.getConfig('background')
  return bg ? {
    backgroundImage: `url(${bg})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundAttachment: 'fixed'
  } : {}
})

const handleSearch = () => {
  // 搜索功能在主页实现
  if (route.path !== '/') {
    router.push({ path: '/', query: { search: searchQuery.value } })
  }
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

/* 导航栏 */
.navbar {
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
}

.nav-left {
  flex: 0 0 200px;
}

.site-title {
  margin: 0;
  font-size: 20px;
  color: #333;
  cursor: pointer;
  transition: color 0.3s;
}

.site-title:hover {
  color: #409eff;
}

.nav-center {
  flex: 1;
}

.nav-menu {
  border-bottom: none;
}

.nav-right {
  flex: 0 0 400px;
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: flex-end;
}

.search-input {
  width: 200px;
}

.admin-link,
.login-link {
  text-decoration: none;
}

/* 主内容区 */
.main-content {
  flex: 1;
}

/* 页脚 */
.footer {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 20px;
  text-align: center;
  color: #666;
  margin-top: auto;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .nav-content {
    flex-wrap: wrap;
    height: auto;
    padding: 10px 20px;
  }

  .nav-center {
    order: 3;
    flex: 0 0 100%;
    margin-top: 10px;
  }

  .nav-right {
    flex: 0 0 auto;
  }

  .search-input {
    width: 150px;
  }
}
</style>