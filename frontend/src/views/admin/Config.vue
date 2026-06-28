<template>
  <div class="config-page">
    <h2 class="page-title">博客配置</h2>

    <el-card shadow="hover">
      <el-form
        ref="formRef"
        :model="form"
        label-width="100px"
        style="max-width: 600px"
      >
        <el-form-item label="博客标题">
          <el-input v-model="form.title" placeholder="请输入博客标题" />
        </el-form-item>

        <el-form-item label="个性签名">
          <el-input
            v-model="form.signature"
            type="textarea"
            :rows="3"
            placeholder="请输入个性签名"
          />
        </el-form-item>

        <el-form-item label="头像">
          <div class="avatar-upload">
            <el-avatar :size="100" :src="form.avatar || undefined">
              <el-icon :size="40"><User /></el-icon>
            </el-avatar>
            <el-upload
              class="avatar-uploader"
              :show-file-list="false"
              :before-upload="beforeAvatarUpload"
              :http-request="handleAvatarUpload"
            >
              <el-button type="primary">上传头像</el-button>
            </el-upload>
          </div>
          <div class="avatar-tip">支持 jpg/png/gif 格式，建议尺寸 200x200</div>
        </el-form-item>

        <el-form-item label="背景图片">
          <div class="background-upload">
            <div v-if="form.background" class="background-preview">
              <img :src="form.background" alt="背景预览" />
              <el-button type="danger" size="small" @click="form.background = ''">移除</el-button>
            </div>
            <el-upload
              v-else
              class="background-uploader"
              :show-file-list="false"
              :before-upload="beforeBackgroundUpload"
              :http-request="handleBackgroundUpload"
            >
              <el-button>
                <el-icon><Upload /></el-icon>
                上传背景图片
              </el-button>
            </el-upload>
          </div>
          <div class="background-tip">支持 jpg/png 格式，建议尺寸 1920x1080，文件大小不超过 5MB</div>
        </el-form-item>

        <el-form-item label="作者名称">
          <el-input v-model="form.author_name" placeholder="请输入作者名称" />
        </el-form-item>

        <el-form-item label="个人简介">
          <el-input
            v-model="form.bio"
            type="textarea"
            :rows="3"
            placeholder="请输入个人简介"
          />
        </el-form-item>

        <el-form-item label="技能标签">
          <el-input v-model="form.skills" placeholder="多个标签用逗号分隔，如：Vue,Python,Flask" />
        </el-form-item>

        <el-form-item label="职业">
          <el-input v-model="form.profession" placeholder="请输入职业" />
        </el-form-item>

        <el-form-item label="所在地">
          <el-input v-model="form.location" placeholder="请输入所在地" />
        </el-form-item>

        <el-form-item label="GitHub">
          <el-input v-model="form.github" placeholder="请输入 GitHub 地址" />
        </el-form-item>

        <el-form-item label="页脚信息">
          <el-input
            v-model="form.footer"
            type="textarea"
            :rows="2"
            placeholder="请输入页脚信息"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSave">
            保存配置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="hover" style="margin-top: 20px">
      <template #header>
        <span>修改密码</span>
      </template>
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
        style="max-width: 400px"
      >
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="passwordForm.old_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="passwordForm.new_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="passwordForm.confirm_password" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="passwordLoading" @click="handleChangePassword">
            修改密码
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useConfigStore } from '@/stores/config'
import { uploadAPI } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const configStore = useConfigStore()

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  title: '',
  signature: '',
  avatar: '',
  background: '',
  author_name: '',
  bio: '',
  skills: '',
  profession: '',
  location: '',
  github: '',
  footer: ''
})

const passwordFormRef = ref(null)
const passwordLoading = ref(false)
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

const beforeAvatarUpload = (file) => {
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

const handleAvatarUpload = async (options) => {
  try {
    const response = await uploadAPI.uploadAvatar(options.file)
    form.avatar = response.url
    ElMessage.success('头像上传成功')
  } catch (error) {
    // 错误已在拦截器中处理
  }
}

const beforeBackgroundUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

const handleBackgroundUpload = async (options) => {
  try {
    const response = await uploadAPI.uploadImage(options.file)
    form.background = response.url
    ElMessage.success('背景图片上传成功')
  } catch (error) {
    // 错误已在拦截器中处理
  }
}

const handleSave = async () => {
  loading.value = true
  try {
    await configStore.batchSetConfig(form)
    ElMessage.success('配置保存成功')
  } finally {
    loading.value = false
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
        authStore.logout()
        router.push('/login')
      } finally {
        passwordLoading.value = false
      }
    }
  })
}

onMounted(async () => {
  await configStore.fetchConfig()
  Object.keys(form).forEach(key => {
    form[key] = configStore.getConfig(key, '')
  })
})
</script>

<style scoped>
.config-page {
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #303133;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 10px;
}

.background-upload {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.background-preview {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.background-preview img {
  max-width: 400px;
  max-height: 200px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.background-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 10px;
}
</style>