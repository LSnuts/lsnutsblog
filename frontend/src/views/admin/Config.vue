 <template>
  <div class="config-page">
    <h2 class="page-title">博客配置</h2>

    <!-- 实时预览区域 -->
    <el-card shadow="hover" class="preview-card">
      <template #header>
        <span>博客预览</span>
      </template>
      <div class="preview-area" :style="previewStyle">
        <div class="preview-overlay">
          <div class="preview-nav">导航栏</div>
          <div class="preview-body">
            <div class="preview-sidebar">个人资料</div>
            <div class="preview-main">文章列表</div>
            <div class="preview-sidebar">日历</div>
          </div>
        </div>
      </div>
    </el-card>

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
            <el-avatar :size="100" :src="resolveUploadUrl(form.avatar) || undefined">
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
          <div class="tip">支持 jpg/png/gif 格式，建议尺寸 200x200</div>
        </el-form-item>

        <el-form-item label="背景图片">
          <div class="bg-upload-area">
            <div class="bg-preview" v-if="form.background">
              <div class="bg-preview-img" :style="{backgroundImage: 'url('+resolveUploadUrl(form.background)+')'}"></div>
              <div class="bg-actions">
                <el-button type="primary" @click="openCropDialog('background')">裁剪</el-button>
                <el-button type="danger" @click="form.background = ''">移除</el-button>
              </div>
            </div>
            <div class="bg-upload-zone" v-else @click="triggerBgUpload('background')">
              <el-icon :size="40"><Plus /></el-icon>
              <span>上传背景图片</span>
            </div>
            <input
              ref="bgFileInput"
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              style="display:none"
              @change="handleBgFileSelect($event, 'background')"
            />
          </div>
          <div class="tip">支持 jpg/png 格式，建议尺寸 1920x1080，文件大小不超过 5MB</div>
        </el-form-item>

        <el-form-item label="首页横幅图">
          <div class="bg-upload-area">
            <div class="bg-preview" v-if="form.hero_banner">
              <div class="bg-preview-img" :style="{backgroundImage: 'url('+resolveUploadUrl(form.hero_banner)+')'}"></div>
              <div class="bg-actions">
                <el-button type="primary" @click="openCropDialog('hero_banner')">裁剪</el-button>
                <el-button type="danger" @click="form.hero_banner = ''">移除</el-button>
              </div>
            </div>
            <div class="bg-upload-zone" v-else @click="triggerBgUpload('hero_banner')">
              <el-icon :size="40"><PictureFilled /></el-icon>
              <span>上传横幅图片</span>
            </div>
            <input
              ref="heroFileInput"
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              style="display:none"
              @change="handleBgFileSelect($event, 'hero_banner')"
            />
          </div>
          <div class="tip">首页顶部大图，建议尺寸 1920x600，不设置则使用背景图片</div>
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
      <template #header><span>修改密码</span></template>
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

    <!-- 裁剪对话框 -->
    <el-dialog v-model="cropDialogVisible" title="裁剪背景图片" width="700px" @opened="initCropper">
      <div class="crop-container" v-loading="cropLoading">
        <div class="crop-area">
          <canvas ref="cropCanvas" class="crop-canvas"></canvas>
        </div>
        <div class="crop-preview">
          <h4>预览效果</h4>
          <div class="crop-preview-box" :style="{backgroundImage: 'url('+cropPreviewUrl+')'}"></div>
        </div>
      </div>
      <div class="crop-controls">
        <el-slider v-model="cropZoom" :min="50" :max="200" :step="5" show-input @change="renderCropper" />
        <span class="crop-zoom-label">缩放: {{ cropZoom }}%</span>
      </div>
      <template #footer>
        <el-button @click="cropDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="cropSaving" @click="saveCropped">应用裁剪</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useConfigStore } from '@/stores/config'
import { uploadAPI, resolveUploadUrl } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const configStore = useConfigStore()

const formRef = ref(null)
const loading = ref(false)
const bgFileInput = ref(null)
const heroFileInput = ref(null)
const uploadTarget = ref('')

const form = reactive({
  title: '',
  signature: '',
  avatar: '',
  background: '',
  hero_banner: '',
  author_name: '',
  bio: '',
  skills: '',
  profession: '',
  location: '',
  github: '',
  footer: ''
})

const previewStyle = computed(() => {
  const bg = resolveUploadUrl(form.background)
  return bg ? {
    backgroundImage: `url(${bg})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  } : {
    backgroundColor: '#e8e8e8'
  }
})

const passwordFormRef = ref(null)
const passwordLoading = ref(false)
const passwordForm = reactive({ old_password: '', new_password: '', confirm_password: '' })
const passwordRules = {
  old_password: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  new_password: [{ required: true, message: '请输入新密码', trigger: 'blur' }, { min: 6, message: '密码长度至少6位', trigger: 'blur' }],
  confirm_password: [{ required: true, message: '请确认新密码', trigger: 'blur' }, { validator: (rule, val, cb) => val === passwordForm.new_password ? cb() : cb(new Error('两次输入的密码不一致')), trigger: 'blur' }]
}

// 裁剪相关
const cropDialogVisible = ref(false)
const cropLoading = ref(false)
const cropSaving = ref(false)
const cropCanvas = ref(null)
const cropZoom = ref(100)
const cropPreviewUrl = ref('')
let cropImage = null

const triggerBgUpload = (target) => {
  uploadTarget.value = target
  if (target === 'hero_banner') heroFileInput.value?.click()
  else bgFileInput.value?.click()
}

const handleBgFileSelect = (e, target) => {
  const file = e.target.files?.[0]
  if (!file) return

  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isImage) { ElMessage.error('只能上传图片文件!'); return }
  if (!isLt5M) { ElMessage.error('图片大小不能超过 5MB!'); return }

  cropLoading.value = true
  const reader = new FileReader()
  reader.onload = (ev) => {
    const img = new Image()
    img.onload = async () => {
      cropImage = img
      cropZoom.value = 100
      uploadTarget.value = target
      cropDialogVisible.value = true
      cropLoading.value = false
    }
    img.src = ev.target.result
  }
  reader.readAsDataURL(file)
  e.target.value = ''
}

const openCropDialog = (target) => {
  uploadTarget.value = target
  const url = target === 'hero_banner' ? form.hero_banner : form.background
  if (!url) { ElMessage.warning('请先上传图片'); return }

  cropLoading.value = true
  const img = new Image()
  img.crossOrigin = 'anonymous'
  img.onload = () => {
    cropImage = img
    cropZoom.value = 100
    cropDialogVisible.value = true
    cropLoading.value = false
  }
  img.onerror = () => {
    ElMessage.error('无法加载图片进行裁剪')
    cropLoading.value = false
  }
  img.src = resolveUploadUrl(url)
}

const initCropper = async () => {
  await nextTick()
  renderCropper()
}

const renderCropper = () => {
  if (!cropImage || !cropCanvas.value) return

  const canvas = cropCanvas.value
  const ctx = canvas.getContext('2d')

  // 容器尺寸
  const containerWidth = 520
  const containerHeight = 290

  // 缩放
  const scale = cropZoom.value / 100
  const imgW = cropImage.width * scale
  const imgH = cropImage.height * scale

  // 裁剪区域（居中）
  const cropW = Math.min(imgW, containerWidth)
  const cropH = Math.min(imgH, containerHeight)

  canvas.width = containerWidth
  canvas.height = containerHeight

  // 清空
  ctx.fillStyle = '#f0f0f0'
  ctx.fillRect(0, 0, containerWidth, containerHeight)

  // 绘制图片（居中）
  const sx = (imgW - cropW) / 2
  const sy = (imgH - cropH) / 2

  ctx.drawImage(cropImage, 0, 0, imgW, imgH, 0, 0, containerWidth, containerHeight)

  // 保存裁剪后的数据
  cropPreviewUrl.value = canvas.toDataURL('image/jpeg', 0.9)

  // 绘制遮罩
  ctx.fillStyle = 'rgba(0,0,0,0.3)'
  ctx.fillRect(0, 0, containerWidth, containerHeight)

  // 裁切区域（留白，让用户看到选择区域）
  const cutX = 20
  const cutY = 20
  const cutW = containerWidth - 40
  const cutH = containerHeight - 40
  ctx.clearRect(cutX, cutY, cutW, cutH)
  ctx.strokeStyle = '#409eff'
  ctx.lineWidth = 2
  ctx.setLineDash([5, 5])
  ctx.strokeRect(cutX, cutY, cutW, cutH)
  ctx.setLineDash([])
}

const saveCropped = async () => {
  if (!cropImage) return
  cropSaving.value = true

  try {
    // 从canvas获取裁剪后图片
    const canvas = cropCanvas.value
    const cutX = 20
    const cutY = 20
    const cutW = canvas.width - 40
    const cutH = canvas.height - 40

    // 创建临时canvas进行精确裁剪
    const tempCanvas = document.createElement('canvas')
    tempCanvas.width = cutW
    tempCanvas.height = cutH
    const tempCtx = tempCanvas.getContext('2d')

    const scale = cropZoom.value / 100
    const imgW = cropImage.width * scale
    const imgH = cropImage.height * scale

    // 计算源偏移（居中）
    const sx = (imgW - canvas.width) / 2 / scale + cutX / scale
    const sy = (imgH - canvas.height) / 2 / scale + cutY / scale
    const sw = cutW / scale
    const sh = cutH / scale

    tempCtx.drawImage(cropImage, sx, sy, sw, sh, 0, 0, cutW, cutH)

    // 转为Blob上传
    const blob = await new Promise(resolve => tempCanvas.toBlob(resolve, 'image/jpeg', 0.92))

    // 使用 FormData 上传
    const fd = new FormData()
    fd.append('file', blob, 'background.jpg')
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
    const uploadUrl = `${apiBaseUrl}/upload/image`
    const res = await fetch(uploadUrl, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}` },
      body: fd
    })
    const json = await res.json()
    if (json.url) {
      const targetKey = uploadTarget.value === 'hero_banner' ? 'hero_banner' : 'background'
      form[targetKey] = json.url
      ElMessage.success('图片裁剪上传成功')
      cropDialogVisible.value = false
    } else {
      ElMessage.error(json.error || '上传失败')
    }
  } finally {
    cropSaving.value = false
  }
}

const beforeAvatarUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isImage) { ElMessage.error('只能上传图片文件!'); return false }
  if (!isLt2M) { ElMessage.error('图片大小不能超过 2MB!'); return false }
  return true
}

const handleAvatarUpload = async (options) => {
  try {
    const response = await uploadAPI.uploadAvatar(options.file)
    form.avatar = response.url
    ElMessage.success('头像上传成功')
  } catch { /* 错误已在拦截器中处理 */ }
}

const handleSave = async () => {
  loading.value = true
  try {
    await configStore.batchSetConfig(form)
    ElMessage.success('配置保存成功')
  } finally { loading.value = false }
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordLoading.value = true
      try {
        await authStore.changePassword({ old_password: passwordForm.old_password, new_password: passwordForm.new_password })
        ElMessage.success('密码修改成功，请重新登录')
        authStore.logout()
        router.push('/login')
      } finally { passwordLoading.value = false }
    }
  })
}

onMounted(async () => {
  await configStore.fetchConfig()
  Object.keys(form).forEach(key => { form[key] = configStore.getConfig(key, '') })
})
</script>

<style scoped>
.config-page { padding: 20px; }
.page-title { margin-bottom: 20px; font-size: 24px; color: #303133; }

/* 预览 */
.preview-card { margin-bottom: 20px; }
.preview-area {
  height: 180px;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}
.preview-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.5);
  display: flex;
  flex-direction: column;
}
.preview-nav {
  height: 36px;
  background: rgba(255,255,255,0.85);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; color: #666; margin: 6px 8px; border-radius: 4px;
}
.preview-body {
  flex: 1;
  display: grid;
  grid-template-columns: 80px 1fr 80px;
  gap: 6px;
  padding: 0 8px 8px;
}
.preview-sidebar,
.preview-main {
  background: rgba(255,255,255,0.8);
  border-radius: 4px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: #999;
}

/* 背景上传 */
.bg-upload-area {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.bg-preview {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.bg-preview-img {
  width: 400px;
  height: 200px;
  border-radius: 8px;
  background-size: cover;
  background-position: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.bg-actions {
  display: flex;
  gap: 10px;
}
.bg-upload-zone {
  width: 400px;
  height: 150px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #909399;
  cursor: pointer;
  transition: all 0.3s;
}
.bg-upload-zone:hover {
  border-color: #409eff;
  color: #409eff;
}
.tip { color: #909399; font-size: 12px; margin-top: 8px; }

/* 裁剪 */
.crop-container {
  display: flex;
  gap: 20px;
}
.crop-area {
  flex: 1;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}
.crop-canvas { display: block; width: 100%; }
.crop-preview { width: 150px; }
.crop-preview h4 { margin: 0 0 8px; font-size: 13px; color: #666; }
.crop-preview-box {
  width: 150px;
  height: 84px;
  border-radius: 4px;
  background-size: cover;
  background-position: center;
  border: 1px solid #dcdfe6;
}
.crop-controls {
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.crop-controls .el-slider { flex: 1; }
.crop-zoom-label { font-size: 13px; color: #666; white-space: nowrap; }

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 20px;
}
</style>