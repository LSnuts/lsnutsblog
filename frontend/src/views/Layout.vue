<template>
  <div class="layout-container" :class="{ 'has-hero': isHome }">
    <!-- 背景层 -->
    <div class="bg-layer" :style="backgroundStyle"></div>

    <!-- 紧凑导航栏 -->
    <nav class="navbar">
      <div class="nav-inner">
        <div class="nav-left">
          <h1 class="site-title" @click="$router.push('/')">{{ configStore.getConfig('title', '我的博客') }}</h1>
          <div class="nav-menu-wrapper">
            <el-menu mode="horizontal" :default-active="activeMenu" router class="nav-menu">
              <template v-for="item in visibleMenuItems" :key="item.path">
                <el-menu-item v-if="!item.children || !item.children.length" :index="item.path">
                  {{ item.label }}
                </el-menu-item>
                <el-sub-menu v-else :index="item.path">
                  <template #title>{{ item.label }}</template>
                  <el-menu-item v-for="child in item.children" :key="child.path" :index="child.path">
                    {{ child.label }}
                  </el-menu-item>
                </el-sub-menu>
              </template>
            </el-menu>
          </div>
        </div>
        <div class="nav-right">
          <el-input v-model="searchQuery" placeholder="搜索..." class="search-input" clearable @keyup.enter="handleSearch">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
          <el-tooltip :content="themeStore.isDark ? '日间模式' : '夜间模式'" placement="bottom">
            <el-button :icon="themeStore.isDark ? 'Sunny' : 'Moon'" circle @click="themeStore.toggle" class="icon-btn" />
          </el-tooltip>
          <router-link v-if="authStore.isAuthenticated" to="/admin">
            <el-button type="primary" size="small">管理</el-button>
          </router-link>
          <router-link v-else to="/login">
            <el-button size="small">登录</el-button>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 顶部大背景横幅 (仅在首页展示) -->
    <div v-if="isHome" class="hero-section" :style="heroStyle">
      <div class="hero-overlay">
        <h1 class="hero-title">{{ configStore.getConfig('title', '我的博客') }}</h1>
        <p class="hero-subtitle">{{ configStore.getConfig('signature', '分享知识，记录生活') }}</p>
      </div>
    </div>

    <!-- 主内容 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 页脚 (可在管理后台修改) -->
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
import { useThemeStore } from '@/stores/theme'
import { resolveUploadUrl } from '@/api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const configStore = useConfigStore()
const themeStore = useThemeStore()

const searchQuery = ref('')

const isHome = computed(() => route.path === '/')
const activeMenu = computed(() => route.path)

const menuItems = computed(() => {
  const raw = configStore.getConfig('menu_items', '')
  if (raw) {
    try { return JSON.parse(raw) }
    catch { return defaultMenu }
  }
  return defaultMenu
})

// 只显示 visible===true 或未设置 visible 的菜单项
const visibleMenuItems = computed(() => {
  return menuItems.value.filter(item => item.visible !== false)
})

const defaultMenu = [
  { label: '主页', path: '/' },
  { label: '关于我', path: '/about' },
  { label: '留言墙', path: '/messages' }
]

const backgroundStyle = computed(() => {
  const bg = resolveUploadUrl(configStore.getConfig('background'))
  return bg ? {
    backgroundImage: `url(${bg})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundAttachment: 'fixed',
    backgroundRepeat: 'no-repeat'
  } : {}
})

const heroStyle = computed(() => {
  // 优先使用独立横幅图片，没有则使用背景图片
  const hero = resolveUploadUrl(configStore.getConfig('hero_banner'))
  const bg = hero || resolveUploadUrl(configStore.getConfig('background'))
  return bg ? {
    backgroundImage: `url(${bg})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  } : {}
})

const handleSearch = () => {
  if (route.path !== '/') {
    router.push({ path: '/', query: { search: searchQuery.value } })
  } else {
    router.push({ query: { search: searchQuery.value } })
  }
}
</script>

<style>
/* ========== 全局 CSS 变量（含暗色） ========== */
:root {
  --bg-primary: #f0f2f5;
  --bg-card: rgba(255, 255, 255, 0.92);
  --bg-navbar: rgba(255, 255, 255, 0.95);
  --bg-overlay: rgba(255, 255, 255, 0.6);
  --text-primary: #333;
  --text-secondary: #666;
  --text-muted: #999;
  --border-color: #eee;
  --shadow-color: rgba(0, 0, 0, 0.1);
}
html.dark-mode {
  --bg-primary: #1a1a2e;
  --bg-card: rgba(30, 30, 50, 0.92);
  --bg-navbar: rgba(20, 20, 40, 0.95);
  --bg-overlay: rgba(0, 0, 0, 0.6);
  --text-primary: #e0e0e0;
  --text-secondary: #b0b0b0;
  --text-muted: #888;
  --border-color: #3a3a5c;
  --shadow-color: rgba(0, 0, 0, 0.3);
}
html.dark-mode, html.dark-mode body {
  background-color: #1a1a2e !important; color: #e0e0e0;
}
html.dark-mode .el-card {
  background-color: rgba(30, 30, 50, 0.92) !important;
  border-color: #3a3a5c !important; color: #e0e0e0;
}
html.dark-mode .el-menu--horizontal { background-color: transparent !important; }
html.dark-mode .el-menu--horizontal .el-menu-item { color: #b0b0b0 !important; }
html.dark-mode .el-menu--horizontal .el-menu-item.is-active { color: #409eff !important; border-bottom-color: #409eff !important; }
html.dark-mode .el-input__wrapper { background-color: rgba(30,30,50,0.8) !important; box-shadow: 0 0 0 1px #3a3a5c inset !important; }
html.dark-mode .el-input__inner { color: #e0e0e0 !important; }
html.dark-mode .el-pagination button, html.dark-mode .el-pager li {
  background-color: transparent !important; color: #b0b0b0 !important;
}
html.dark-mode .el-pager li.is-active { color: #409eff !important; }
html.dark-mode .el-skeleton__item { background: #3a3a5c !important; }
</style>

<style scoped>
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: background-color 0.3s;
}

/* 背景 */
.bg-layer {
  position: fixed; inset: 0;
  z-index: 0; pointer-events: none;
}
.layout-container::before {
  content: '';
  position: fixed; inset: 0;
  background-color: var(--bg-overlay);
  z-index: 0; pointer-events: none;
  transition: background-color 0.3s;
}

/* ====== 紧凑导航栏 ====== */
.navbar {
  position: sticky; top: 0; z-index: 100;
  background-color: var(--bg-navbar);
  backdrop-filter: blur(10px);
  box-shadow: 0 1px 8px var(--shadow-color);
  height: 46px; overflow: hidden;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
}
.nav-inner {
  max-width: 1400px; width: 100%;
  margin: 0 auto; padding: 0 16px;
  display: flex; align-items: center;
  justify-content: space-between;
}
.nav-left {
  display: flex; align-items: center;
  gap: 4px; flex: 1; min-width: 0; overflow: hidden;
}
.site-title {
  margin: 0; font-size: 15px; font-weight: 600;
  color: var(--text-primary);
  cursor: pointer; white-space: nowrap;
  transition: color 0.3s; flex-shrink: 0;
  padding-right: 8px;
  border-right: 1px solid var(--border-color);
}
.site-title:hover { color: #409eff; }
.nav-menu-wrapper {
  flex: 1; overflow-x: auto; overflow-y: hidden;
  margin-left: 4px; scrollbar-width: none; -ms-overflow-style: none;
  align-self: stretch; display: flex; align-items: stretch;
}
.nav-menu-wrapper::-webkit-scrollbar { display: none; height: 0; }
.nav-menu {
  border-bottom: none !important;
  display: flex; flex-wrap: nowrap; width: fit-content;
}
.nav-menu .el-menu-item, .nav-menu .el-sub-menu .el-sub-menu__title {
  padding: 0 10px; font-size: 13px; height: 46px !important; line-height: 46px !important;
  white-space: nowrap; flex-shrink: 0;
}
/* 活动指示器改用 box-shadow 避免撑大底部 */
.nav-menu .el-menu-item.is-active {
  box-shadow: inset 0 -2px 0 #409eff !important;
  border-bottom: none !important;
}
.nav-menu .el-menu-item:hover {
  background-color: transparent !important;
}
.nav-right {
  display: flex; align-items: center; gap: 8px;
  flex-shrink: 0;
}
.search-input { width: 160px; }
.search-input :deep(.el-input__wrapper) { height: 32px; }
.icon-btn { font-size: 16px; }
.icon-btn:hover { transform: scale(1.1); }

/* ====== 顶部大背景横幅 ====== */
.hero-section {
  position: relative;
  height: 340px;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
  z-index: 1;
}
.has-hero .hero-section {
  background-color: #2c3e50;
  background-size: cover; background-position: center;
}
.hero-overlay {
  text-align: center;
  padding: 40px;
  position: relative;
  z-index: 2;
}
.hero-title {
  font-size: 48px; font-weight: 700; margin: 0 0 12px;
  color: #fff;
  text-shadow: 0 2px 12px rgba(0,0,0,0.3);
  letter-spacing: 2px;
}
.hero-subtitle {
  font-size: 20px; margin: 0;
  color: rgba(255,255,255,0.85);
  text-shadow: 0 1px 6px rgba(0,0,0,0.2);
  font-weight: 300;
}
.has-hero .hero-section::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, transparent 50%, rgba(0,0,0,0.2) 100%);
  z-index: 1;
}

/* ====== 主内容 ====== */
.main-content {
  position: relative; z-index: 1; flex: 1;
}

/* ====== 页脚 ====== */
.footer {
  position: relative; z-index: 1;
  background-color: var(--bg-navbar);
  padding: 16px; text-align: center;
  color: var(--text-muted); font-size: 13px;
  transition: background-color 0.3s;
}

/* 响应式 */
@media (max-width: 768px) {
  .site-title { font-size: 14px; border: none; }
  .nav-menu .el-menu-item { padding: 0 8px; font-size: 12px; }
  .search-input { width: 120px; }
  .hero-title { font-size: 32px; }
  .hero-subtitle { font-size: 16px; }
  .hero-section { height: 240px; }
}
</style>