<template>
  <div class="admin-menus">
    <h2 class="page-title">菜单管理</h2>
    <el-card shadow="hover">
      <div class="menu-tip">
        <el-icon><InfoFilled /></el-icon>
        <span>管理导航栏菜单项。支持显示/隐藏、拖拽排序、子菜单折叠。</span>
      </div>

      <div class="menu-list" v-loading="loading">
        <div v-for="(item, idx) in menuItems" :key="idx" class="menu-item">
          <el-icon class="drag-handle"><Rank /></el-icon>

          <el-switch v-model="item.visible" class="menu-switch" @change="item.visible = !!item.visible" />

          <div class="menu-fields">
            <div class="menu-row">
              <el-input v-model="item.label" placeholder="菜单名称" class="menu-label" />
              <el-input v-model="item.path" placeholder="/路径 或 https://..." class="menu-path" />
              <el-button type="danger" size="small" @click="removeItem(idx)">删除</el-button>
            </div>

            <!-- 子菜单折叠按钮 -->
            <div class="menu-children-area">
              <el-button v-if="!item.children" size="small" text type="primary" @click="addChild(idx)">
                <el-icon><Plus /></el-icon> 添加子菜单
              </el-button>
              <template v-if="item.children && item.children.length">
                <div class="child-items">
                  <div v-for="(child, ci) in item.children" :key="ci" class="child-item">
                    <el-icon class="child-dot"><CircleFilled /></el-icon>
                    <el-input v-model="child.label" placeholder="子菜单名称" class="child-label" />
                    <el-input v-model="child.path" placeholder="/路径" class="child-path" />
                    <el-button type="danger" size="small" circle @click="item.children.splice(ci, 1)">
                      <el-icon><Close /></el-icon>
                    </el-button>
                  </div>
                </div>
                <el-button size="small" text type="primary" @click="addChild(idx)">
                  <el-icon><Plus /></el-icon> 添加子菜单
                </el-button>
              </template>
            </div>
          </div>
        </div>
      </div>

      <el-button class="add-btn" @click="addItem">
        <el-icon><Plus /></el-icon> 添加菜单项
      </el-button>

      <div class="save-area">
        <el-button type="primary" :loading="saving" @click="handleSave">保存菜单</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { configAPI } from '@/api'
import { ElMessage } from 'element-plus'

const menuItems = ref([])
const loading = ref(false)
const saving = ref(false)

const defaultItems = [
  { label: '主页', path: '/', visible: true },
  { label: '关于我', path: '/about', visible: true },
  { label: '留言墙', path: '/messages', visible: true }
]

const fetchMenu = async () => {
  loading.value = true
  try {
    const res = await configAPI.getConfig('menu_items')
    if (res.config?.value) {
      try {
        menuItems.value = JSON.parse(res.config.value)
        // 确保每个项都有 visible 字段
        menuItems.value.forEach(item => { if (item.visible === undefined) item.visible = true })
      } catch {
        menuItems.value = defaultItems.map(i => ({...i}))
      }
    } else {
      menuItems.value = defaultItems.map(i => ({...i}))
    }
  } catch {
    menuItems.value = defaultItems.map(i => ({...i}))
  } finally { loading.value = false }
}

const addItem = () => {
  menuItems.value.push({ label: '', path: '', visible: true })
}

const addChild = (idx) => {
  if (!menuItems.value[idx].children) menuItems.value[idx].children = []
  menuItems.value[idx].children.push({ label: '', path: '' })
}

const removeItem = (idx) => {
  menuItems.value.splice(idx, 1)
}

const handleSave = async () => {
  saving.value = true
  try {
    const valid = menuItems.value.filter(m => m.label && m.path)
    // 清理空的子菜单
    valid.forEach(item => {
      if (item.children) {
        item.children = item.children.filter(c => c.label && c.path)
        if (!item.children.length) delete item.children
      }
    })
    await configAPI.setConfig({ key: 'menu_items', value: JSON.stringify(valid) })
    menuItems.value = valid
    ElMessage.success('菜单保存成功')
  } finally { saving.value = false }
}

onMounted(fetchMenu)
</script>

<style scoped>
.admin-menus { padding: 20px; max-width: 900px; }
.page-title { margin: 0 0 20px; font-size: 24px; }
.menu-tip {
  display: flex; align-items: center; gap: 8px;
  padding: 12px; background: #e6f7ff; border-radius: 4px;
  color: #1890ff; font-size: 13px; margin-bottom: 16px;
}
.menu-list { display: flex; flex-direction: column; gap: 10px; }
.menu-item {
  display: flex; align-items: flex-start; gap: 8px;
  padding: 12px; border: 1px solid #eee; border-radius: 8px;
  background: #fafafa; transition: all 0.2s;
}
.menu-item:hover { border-color: #409eff; }
.drag-handle { cursor: grab; color: #999; margin-top: 4px; }
.menu-switch { margin-top: 2px; }
.menu-fields { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.menu-row { display: flex; align-items: center; gap: 8px; }
.menu-label { flex: 0 0 140px; }
.menu-path { flex: 1; }
.menu-children-area { padding-left: 20px; }
.child-items { display: flex; flex-direction: column; gap: 6px; margin-bottom: 6px; }
.child-item { display: flex; align-items: center; gap: 6px; }
.child-dot { font-size: 6px; color: #409eff; flex-shrink: 0; }
.child-label { flex: 0 0 120px; }
.child-path { flex: 1; }
.child-item .el-button { flex-shrink: 0; }
.add-btn { margin-top: 12px; }
.save-area { margin-top: 20px; }

html.dark-mode .menu-item { border-color: #3a3a5c; background: #2a2a45; }
html.dark-mode .menu-tip { background: #1a3a4a; }
</style>