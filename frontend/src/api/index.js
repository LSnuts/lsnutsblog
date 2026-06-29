import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000
})

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const errData = error.response?.data || {}
    const message = errData.error || errData.msg || '请求失败'
    const status = error.response?.status

    // 401 未授权 或 422 JWT令牌无效（subject格式错误/过期）
    if (status === 401 || (status === 422 && errData.msg?.toLowerCase().includes('subject'))) {
      const authStore = useAuthStore()
      authStore.logout()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  getCurrentUser: () => api.get('/auth/me'),
  changePassword: (data) => api.post('/auth/change-password', data),
  refreshToken: () => api.post('/auth/refresh')
}

export const postsAPI = {
  getPosts: (params) => api.get('/posts', { params }),
  getPost: (id) => api.get(`/posts/${id}`),
  createPost: (data) => api.post('/posts', data),
  updatePost: (id, data) => api.put(`/posts/${id}`, data),
  deletePost: (id) => api.delete(`/posts/${id}`)
}

export const configAPI = {
  getAllConfig: () => api.get('/config'),
  getConfig: (key) => api.get(`/config/${key}`),
  setConfig: (data) => api.post('/config', data),
  batchSetConfig: (data) => api.post('/config/batch', data),
  deleteConfig: (key) => api.delete(`/config/${key}`)
}

const createUploadRequest = (url) => (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post(url, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const uploadAPI = {
  uploadImage: createUploadRequest('/upload/image'),
  uploadAvatar: createUploadRequest('/upload/avatar')
}

export const messagesAPI = {
  getMessages: (params) => api.get('/messages', { params }),
  getMessage: (id) => api.get(`/messages/${id}`),
  createMessage: (data) => api.post('/messages', data),
  updateMessage: (id, data) => api.put(`/messages/${id}`, data),
  deleteMessage: (id) => api.delete(`/messages/${id}`)
}

export const pagesAPI = {
  getPages: (params) => api.get('/pages', { params }),
  getPage: (slug) => api.get(`/pages/${slug}`),
  createPage: (data) => api.post('/pages', data),
  updatePage: (id, data) => api.put(`/pages/${id}`, data),
  deletePage: (id) => api.delete(`/pages/${id}`)
}

export const uploadsBaseUrl = import.meta.env.VITE_UPLOADS_BASE_URL

export const resolveUploadUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http://localhost') || url.startsWith('http://127.0.0.1')) {
    return url.replace(/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?/, '')
  }
  if (url.startsWith('http://') || url.startsWith('https://')) return url
  if (url.startsWith('/uploads/')) return url
  return `${uploadsBaseUrl}${url.startsWith('/') ? '' : '/'}${url}`
}

export default api