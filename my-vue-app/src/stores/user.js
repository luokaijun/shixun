import { reactive } from 'vue'
import { login as apiLogin, register as apiRegister } from '../api/index'

export const userStore = reactive({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  isLoggedIn: !!localStorage.getItem('user'),

  async login(credentials) {
    const result = await apiLogin(credentials)
    if (result.success) {
      this.user = result.user
      this.isLoggedIn = true
      localStorage.setItem('user', JSON.stringify(this.user))
      return { success: true }
    }
    return { success: false, message: result.message || '用户名或密码错误' }
  },

  async register(userData) {
    const result = await apiRegister(userData)
    if (result.success) {
      return { success: true, message: '注册成功' }
    }
    return { success: false, message: result.message || '注册失败' }
  },

  logout() {
    this.user = null
    this.isLoggedIn = false
    localStorage.removeItem('user')
  }
})