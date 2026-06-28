<template>
  <div class="admin-pages">
    <div class="header-row">
      <h2 class="page-title">自定义页面管理</h2>
      <el-button type="primary" @click="openDialog()">新建页面</el-button>
    </div>

    <el-card shadow="hover">
      <el-table :data="pages" v-loading="loading" style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="150" />
        <el-table-column prop="slug" label="链接" min-width="150">
          <template #default="{ row }">
            <code>/page/{{ row.slug }}</code>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_published ? 'success' : 'info'">
              {{ row.is_published ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-popconfirm title="确定删除此页面？" @confirm="handleDelete(row)">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑页面' : '新建页面'" width="650px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="页面标题" />
        </el-form-item>
        <el-form-item label="链接" prop="slug">
          <el-input v-model="form.slug" placeholder="page-url (字母数字和横线)" />
          <div class="tip">访问地址: /page/{{ form.slug || '...' }}</div>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="12" placeholder="支持 Markdown 格式" />
        </el-form-item>
        <el-form-item label="发布">
          <el-switch v-model="form.is_published" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { pagesAPI } from '@/api'
import { ElMessage } from 'element-plus'

const pages = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const saving = ref(false)
const editing = ref(false)
const currentId = ref(null)
const form = ref({ title: '', slug: '', content: '', is_published: false })

const fetchPages = async () => {
  loading.value = true
  try {
    const res = await pagesAPI.getPages()
    pages.value = res.pages
  } finally { loading.value = false }
}

const openDialog = (page) => {
  if (page) {
    editing.value = true
    currentId.value = page.id
    form.value = { title: page.title, slug: page.slug, content: page.content, is_published: page.is_published }
  } else {
    editing.value = false
    currentId.value = null
    form.value = { title: '', slug: '', content: '', is_published: false }
  }
  dialogVisible.value = true
}

const handleSave = async () => {
  if (!form.value.title || !form.value.slug) {
    ElMessage.warning('标题和链接不能为空')
    return
  }
  saving.value = true
  try {
    if (editing.value && currentId.value) {
      await pagesAPI.updatePage(currentId.value, form.value)
      ElMessage.success('页面更新成功')
    } else {
      await pagesAPI.createPage(form.value)
      ElMessage.success('页面创建成功')
    }
    dialogVisible.value = false
    fetchPages()
  } finally { saving.value = false }
}

const handleDelete = async (page) => {
  await pagesAPI.deletePage(page.id)
  ElMessage.success('页面已删除')
  fetchPages()
}

const formatDate = (d) => new Date(d).toLocaleDateString('zh-CN')

onMounted(fetchPages)
</script>

<style scoped>
.admin-pages { padding: 20px; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { margin: 0; font-size: 24px; }
.tip { font-size: 12px; color: #999; margin-top: 4px; }
</style>