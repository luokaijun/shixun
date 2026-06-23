/**
 * router/index.js - Vue Router 路由配置
 * 
 * 【模块用途】
 * 配置应用的路由规则，定义页面路径与组件的映射关系
 * 实现路由守卫，控制页面访问权限（如订单页面需要登录）
 * 使用 history 模式实现无 hash 的 URL
 * 
 * 【模块关系】
 * - 被 main.js 引用，作为 Vue 应用的路由配置
 * - 定义了所有页面组件的路由路径
 * - 通过路由守卫与 userStore 交互，实现登录验证
 * 
 * 【路由列表】
 * | 路径 | 名称 | 组件 | 说明 |
 * |------|------|------|------|
 * | / | Home | Home.vue | 首页 |
 * | /products | Products | Products.vue | 商品列表页 |
 * | /product/:id | ProductDetail | ProductDetail.vue | 商品详情页（动态路由） |
 * | /cart | Cart | Cart.vue | 购物车页面 |
 * | /login | Login | Login.vue | 登录页面 |
 * | /register | Register | Register.vue | 注册页面 |
 * | /orders | Orders | Orders.vue | 订单页面（需要登录） |
 * 
 * 【路由守卫】
 * - beforeEach: 全局前置守卫，检查需要登录的页面
 *   - 如果路由配置了 meta.requiresAuth 为 true
 *   - 且用户未登录，则重定向到登录页面
 *   - 登录成功后自动跳转到之前访问的页面
 */

// 导入Vue Router的核心方法
import { createRouter, createWebHistory } from 'vue-router'

/**
 * 路由配置数组
 * 每个路由对象定义了路径、名称、组件和元数据
 */
const routes = [
  /**
   * 首页路由
   * 路径：/
   * 组件：Home.vue
   */
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  
  /**
   * 商品列表页路由
   * 路径：/products
   * 组件：Products.vue
   */
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/Products.vue')
  },
  
  /**
   * 商品详情页路由（动态路由）
   * 路径：/product/:id（:id 是动态参数，表示商品ID）
   * 组件：ProductDetail.vue
   * 通过 useRoute().params.id 获取商品ID
   */
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('../views/ProductDetail.vue')
  },
  
  /**
   * 购物车页面路由
   * 路径：/cart
   * 组件：Cart.vue
   */
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('../views/Cart.vue')
  },
  
  /**
   * 登录页面路由
   * 路径：/login
   * 组件：Login.vue
   */
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  
  /**
   * 注册页面路由
   * 路径：/register
   * 组件：Register.vue
   */
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  
  /**
   * 订单页面路由（需要登录）
   * 路径：/orders
   * 组件：Orders.vue
   * meta.requiresAuth: true - 标记该路由需要登录才能访问
   */
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('../views/Orders.vue'),
    meta: { requiresAuth: true }
  }
]

/**
 * 创建路由实例
 * - history: 使用 createWebHistory() 创建 HTML5 history 模式
 *   - 特点：URL 没有 # 前缀，更美观
 *   - 注意：需要后端配置支持，否则刷新页面会404
 * - routes: 路由配置数组
 */
const router = createRouter({
  history: createWebHistory(),
  routes
})

/**
 * 路由守卫 - 全局前置守卫
 * 在每次路由跳转前执行
 * @param {Object} to - 目标路由
 * @param {Object} from - 来源路由
 * @param {Function} next - 下一步函数
 */
router.beforeEach((to, from, next) => {
  // 检查用户是否已登录（从 localStorage 获取用户数据）
  const isLoggedIn = localStorage.getItem('user')
  
  // 如果目标路由需要登录（meta.requiresAuth 为 true）
  // 且用户未登录，则重定向到登录页面
  if (to.meta.requiresAuth && !isLoggedIn) {
    // 保存用户原本要访问的页面路径，登录成功后自动跳转
    localStorage.setItem('redirect', to.fullPath)
    // 重定向到登录页面
    next('/login')
  } else {
    // 否则正常跳转
    next()
  }
})

/**
 * 导出路由实例
 * 在 main.js 中通过 app.use(router) 使用
 */
export default router