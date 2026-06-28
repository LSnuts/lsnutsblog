<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="sidebar">
      <div class="sidebar-header">
        <h2>博客管理</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/admin">
          <el-icon><House /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/admin/posts">
          <el-icon><Document /></el-icon>
          <span>文章管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/messages">
          <el-icon><ChatDotSquare /></el-icon>
          <span>留言管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/pages">
          <el-icon><Notebook /></el-icon>
          <span>页面管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/menus">
          <el-icon><Menu /></el-icon>
          <span>菜单管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/config">
          <el-icon><Setting /></el-icon>
          <span>博客配置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <router-link to="/" class="view-site">
            <el-button type="primary" plain>
              <el-icon><View /></el-icon>
              查看网站
            </el-button>
          </router-link>
        </div>
        <div class="header-right">
          <el-tooltip :content="themeStore.isDark ? '切换日间模式' : '切换夜间模式'" placement="bottom">
            <el-button
              :icon="themeStore.isDark ? 'Sunny' : 'Moon'"
              circle
              @click="themeStore.toggle"
              class="theme-toggle"
            />
          </el-tooltip>
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              <el-icon><User /></el-icon>
              {{ authStore.user?.username }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="changePassword">修改密码</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="400px">
      <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="80px">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="passwordForm.old_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="passwordForm.new_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="passwordForm.confirm_password" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="passwordLoading" @click="handleChangePassword">
          确定
        </el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const activeMenu = computed(() => route.path)

const passwordDialogVisible = ref(false)
const passwordLoading = ref(false)
const passwordFormRef = ref(null)

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入旧密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      authStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
    })
  } else if (command === 'changePassword') {
    passwordDialogVisible.value = true
  }
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordLoading.value = true
      try {
        await authStore.changePassword({
          old_password: passwordForm.old_password,
          new_password: passwordForm.new_password
        })
        ElMessage.success('密码修改成功，请重新登录')
        passwordDialogVisible.value = false
        authStore.logout()
        router.push('/login')
      } finally {
        passwordLoading.value = false
      }
    }
  })
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 18px;
}

.el-menu {
  border-right: none;
}

.header {
  background-color: white;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.view-site {
  text-decoration: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 5px;
}

.main {
  background-color: #f0f2f5;
}
</style>

<style>
/* 管理后台暗色模式 */
html.dark-mode .admin-layout .sidebar {
  background-color: #1e1e38 !important;
}

html.dark-mode .admin-layout .header {
  background-color: #1a1a2e !important;
  border-bottom-color: #3a3a5c !important;
  color: #e0e0e0;
}

html.dark-mode .admin-layout .main {
  background-color: #16162a !important;
}

html.dark-mode .admin-layout .user-dropdown {
  color: #e0e0e0;
}

html.dark-mode .admin-layout .el-menu:not(.el-menu--horizontal) {
  background-color: #1e1e38 !important;
}

html.dark-mode .admin-layout .el-menu-item {
  color: #bfcbd9 !important;
}

html.dark-mode .admin-layout .el-menu-item.is-active {
  color: #409eff !important;
  background-color: rgba(64, 158, 255, 0.1) !important;
}

html.dark-mode .admin-layout .theme-toggle {
  color: #e0e0e0;
}

html.dark-mode .admin-layout .theme-toggle:hover {
  color: #409eff;
}

html.dark-mode .admin-layout .el-dialog {
  background-color: #1a1a2e !important;
}

html.dark-mode .admin-layout .el-dialog__title {
  color: #e0e0e0 !important;
}
</style>