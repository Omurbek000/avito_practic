import axios from 'axios'

// Базовый URL нашего Django API
const api = axios.create({
  baseURL: 'http://localhost:8000',
})

// Перехватчик запросов — автоматически добавляет JWT токен в заголовок
// Это значит не нужно вручную добавлять токен в каждый запрос
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Перехватчик ответов — если токен протух (401), чистим localStorage
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
