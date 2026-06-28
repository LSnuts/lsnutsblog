<template>
  <div class="about-page">
    <div class="about-content">
      <el-card class="about-card">
        <template #header>
          <div class="card-header">
            <h2>关于我</h2>
          </div>
        </template>

        <div class="about-body">
          <div class="profile-section">
            <el-avatar :size="150" :src="configStore.getConfig('avatar') || undefined">
              <el-icon :size="80"><User /></el-icon>
            </el-avatar>
            <h1 class="name">{{ configStore.getConfig('author_name', '博主') }}</h1>
            <p class="signature">{{ configStore.getConfig('signature', '这个人很懒，什么都没写') }}</p>
          </div>

          <div class="info-section">
            <h3>基本信息</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">职业：</span>
                <span class="value">{{ configStore.getConfig('profession', '开发者') }}</span>
              </div>
              <div class="info-item">
                <span class="label">所在地：</span>
                <span class="value">{{ configStore.getConfig('location', '未知') }}</span>
              </div>
              <div class="info-item">
                <span class="label">邮箱：</span>
                <span class="value">{{ configStore.getConfig('email', '未设置') }}</span>
              </div>
              <div class="info-item">
                <span class="label">GitHub：</span>
                <span class="value">
                  <a v-if="configStore.getConfig('github')" :href="configStore.getConfig('github')" target="_blank">
                    {{ configStore.getConfig('github') }}
                  </a>
                  <span v-else>未设置</span>
                </span>
              </div>
            </div>
          </div>

          <div class="bio-section">
            <h3>个人简介</h3>
            <div class="bio-content" v-html="renderedBio"></div>
          </div>

          <div class="skills-section">
            <h3>技能标签</h3>
            <div class="skills-tags">
              <el-tag
                v-for="skill in skills"
                :key="skill"
                type="info"
                class="skill-tag"
              >
                {{ skill }}
              </el-tag>
            </div>
          </div>

          <div class="contact-section">
            <h3>联系方式</h3>
            <p>如果你有任何问题或合作意向，欢迎通过以下方式联系我：</p>
            <div class="contact-links">
              <a v-if="configStore.getConfig('email')" :href="'mailto:' + configStore.getConfig('email')">
                <el-button type="primary">
                  <el-icon><Message /></el-icon>
                  发送邮件
                </el-button>
              </a>
              <a v-if="configStore.getConfig('github')" :href="configStore.getConfig('github')" target="_blank">
                <el-button>
                  <el-icon><Link /></el-icon>
                  GitHub
                </el-button>
              </a>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import { marked } from 'marked'

const configStore = useConfigStore()

const skills = computed(() => {
  const skillsStr = configStore.getConfig('skills', 'Vue, Python, JavaScript')
  return skillsStr.split(',').map(s => s.trim()).filter(s => s)
})

const renderedBio = computed(() => {
  const bio = configStore.getConfig('bio', '这个人很懒，什么都没写。')
  return marked(bio)
})

onMounted(() => {
  configStore.fetchConfig()
})
</script>

<style scoped>
.about-page {
  padding: 40px 20px;
  min-height: calc(100vh - 200px);
}

.about-content {
  max-width: 800px;
  margin: 0 auto;
}

.about-card {
  margin-bottom: 20px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  font-size: 28px;
  color: #333;
}

.about-body {
  padding: 20px;
}

.profile-section {
  text-align: center;
  padding: 40px 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 40px;
}

.name {
  margin: 20px 0 10px;
  font-size: 32px;
  color: #333;
}

.signature {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.info-section,
.bio-section,
.skills-section,
.contact-section {
  margin-bottom: 40px;
}

h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
  display: inline-block;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.info-item {
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.label {
  font-weight: bold;
  color: #666;
}

.value {
  color: #333;
}

.value a {
  color: #409eff;
  text-decoration: none;
}

.value a:hover {
  text-decoration: underline;
}

.bio-content {
  line-height: 1.8;
  color: #333;
}

.bio-content :deep(p) {
  margin-bottom: 15px;
}

.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.skill-tag {
  padding: 8px 16px;
  font-size: 14px;
}

.contact-section p {
  color: #666;
  margin-bottom: 20px;
}

.contact-links {
  display: flex;
  gap: 15px;
}

.contact-links a {
  text-decoration: none;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .name {
    font-size: 24px;
  }

  .profile-section {
    padding: 20px 0;
  }
}
</style>