<template>
  <div class="edit-post">
    <div class="page-header">
      <h2 class="page-title">{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
      <el-button @click="router.back()">返回</el-button>
    </div>

    <el-card shadow="hover">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
        style="max-width: 800px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文章标题" />
        </el-form-item>

        <el-form-item label="摘要">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要（可选）"
          />
        </el-form-item>

        <el-form-item label="封面图">
          <el-upload
            class="cover-uploader"
            :show-file-list="false"
            :before-upload="beforeCoverUpload"
            :http-request="handleCoverUpload"
          >
            <img v-if="form.cover_image" :src="form.cover_image" class="cover-image" />
            <el-icon v-else class="cover-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="cover-tip">建议尺寸：800x450，支持 jpg/png/gif 格式</div>
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="15"
            placeholder="请输入文章内容（支持 Markdown 格式）"
          />
        </el-form-item>

        <el-form-item label="发布状态">
          <el-switch
            v-model="form.is_published"
            active-text="发布"
            inactive-text="草稿"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            {{ isEdit ? '保存' : '创建' }}
          </el-button>
          <el-button @click="handleSaveDraft" v-if="!isEdit">
            保存为草稿
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postsAPI, uploadAPI } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  title: '',
  content: '',
  summary: '',
  cover_image: '',
  is_published: false
})

const rules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' }
  ]
}

const beforeCoverUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

const handleCoverUpload = async (options) => {
  try {
    const response = await uploadAPI.uploadImage(options.file)
    form.cover_image = response.url
    ElMessage.success('封面图上传成功')
  } catch (error) {
    // 错误已在拦截器中处理
  }
}

const fetchPost = async () => {
  if (!isEdit.value) return

  loading.value = true
  try {
    const response = await postsAPI.getPost(route.params.id)
    Object.assign(form, response.post)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (isEdit.value) {
          await postsAPI.updatePost(route.params.id, form)
          ElMessage.success('文章已更新')
        } else {
          await postsAPI.createPost(form)
          ElMessage.success('文章已创建')
        }
        router.push('/admin/posts')
      } finally {
        loading.value = false
      }
    }
  })
}

const handleSaveDraft = async () => {
  form.is_published = false
  await handleSubmit()
}

onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.edit-post {
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

.cover-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 300px;
  height: 169px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-uploader:hover {
  border-color: #409eff;
}

.cover-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 10px;
}
</style>