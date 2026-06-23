/**
 * stores/user.js - 用户状态管理
 * 
 * 【模块用途】
 * 管理用户的登录状态和认证信息，包括登录、注册、登出功能
 * 使用 Vue 的 reactive 响应式 API 创建全局状态，登录状态持久化到 localStorage
 * 
 * 【模块关系】
 * - 被 Login.vue、Register.vue、Navbar.vue 等组件引用
 * - 通过 localStorage 实现登录状态持久化（页面刷新后保持登录状态）
 * - 与后端 API 接口交互（后续可扩展）
 * 
 * 【数据结构】
 * userStore.user: 当前登录用户信息
 *   - id: 用户ID
 *   - username: 用户名
 *   - email: 邮箱
 * userStore.isLoggedIn: 是否登录（布尔值）
 * 
 * 【核心方法】
 * - login(credentials): 用户登录
 * - register(userData): 用户注册
 * - logout(): 用户登出
 * 
 * 【当前实现说明】
 * 当前使用模拟数据（mockUsers）进行登录验证
 * 后续可扩展为与后端 API 交互，实现真实的用户认证
 */

// 导入Vue的响应式API
import { reactive } from 'vue'

/**
 * 模拟用户数据（用于开发测试）
 * 实际项目中应从后端API获取用户数据
 */
const mockUsers = [
  { id: 1, username: 'admin', password: '123456', email: 'admin@example.com' },
  { id: 2, username: 'test', password: '123456', email: 'test@example.com' }
]

/**
 * 创建用户状态管理对象
 * 使用 reactive 创建响应式对象，所有组件共享同一个实例
 */
export const userStore = reactive({
  /**
   * 当前登录用户信息
   * 从 localStorage 加载初始化数据，如果没有则为 null
   */
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  
  /**
   * 是否已登录
   * 通过检查 localStorage 中是否存在用户数据来判断
   */
  isLoggedIn: !!localStorage.getItem('user'),

  /**
   * 用户登录
   * @param {Object} credentials - 登录凭证
   * @param {string} credentials.username - 用户名
   * @param {string} credentials.password - 密码
   * @returns {Object} 登录结果 { success: boolean, message?: string }
   */
  login(credentials) {
    // 在模拟用户数据中查找匹配的用户
    const user = mockUsers.find(
      u => u.username === credentials.username && u.password === credentials.password
    )
    
    if (user) {
      // 登录成功：更新用户信息和登录状态
      this.user = { id: user.id, username: user.username, email: user.email }
      this.isLoggedIn = true
      // 将用户信息保存到 localStorage，实现持久化
      localStorage.setItem('user', JSON.stringify(this.user))
      return { success: true }
    }
    
    // 登录失败：返回错误信息
    return { success: false, message: '用户名或密码错误' }
  },

  /**
   * 用户注册
   * @param {Object} userData - 用户注册数据
   * @param {string} userData.username - 用户名
   * @param {string} userData.password - 密码
   * @param {string} userData.email - 邮箱
   * @returns {Object} 注册结果 { success: boolean, message?: string }
   */
  register(userData) {
    // 检查用户名是否已存在
    const exists = mockUsers.find(u => u.username === userData.username)
    
    if (exists) {
      // 用户名已存在，返回错误信息
      return { success: false, message: '用户名已存在' }
    }
    
    // 创建新用户
    const newUser = {
      id: mockUsers.length + 1,
      username: userData.username,
      password: userData.password,
      email: userData.email
    }
    
    // 将新用户添加到模拟用户列表
    mockUsers.push(newUser)
    // 返回注册成功信息
    return { success: true, message: '注册成功' }
  },

  /**
   * 用户登出
   * 清除用户信息和登录状态，并重定向到首页
   */
  logout() {
    // 清除用户信息
    this.user = null
    // 更新登录状态为未登录
    this.isLoggedIn = false
    // 从 localStorage 中移除用户数据
    localStorage.removeItem('user')
  }
})