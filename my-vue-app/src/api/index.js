/**
 * api/index.js - 后端API调用模块
 * 
 * 【模块用途】
 * 封装所有与后端Flask API的交互方法，提供统一的接口调用方式
 * 处理请求、响应、错误处理等通用逻辑
 * 
 * 【模块关系】
 * - 被 Home.vue、Products.vue、ProductDetail.vue 等页面组件引用
 * - 与后端 Flask API 进行 HTTP 请求交互
 * - 使用 fetch API 进行网络请求
 * 
 * 【API基础配置】
 * - BASE_URL: 后端API基础地址，默认 http://localhost:5000/api
 * - 所有接口返回统一格式：{ success: boolean, data: any, message?: string }
 * 
 * 【核心方法】
 * - request(method, url, data, options): 通用请求方法
 * - fetchProducts(params): 获取商品列表
 * - fetchProductDetail(id): 获取商品详情
 * - fetchCategories(): 获取分类列表
 * - fetchBrands(): 获取品牌列表
 * 
 * 【错误处理】
 * - 网络错误：返回 { success: false, message: '网络错误' }
 * - 服务器错误：返回 { success: false, message: '服务器错误' }
 * - 业务错误：返回 { success: false, message: 错误信息 }
 * - 连接超时：返回 { success: false, message: '连接超时' }
 */

/**
 * 后端API基础地址
 * 默认指向本地Flask开发服务器
 */
const BASE_URL = 'http://localhost:5000/api'

/**
 * 通用请求方法
 * @param {string} method - HTTP方法（GET, POST, PUT, DELETE）
 * @param {string} url - 请求路径（相对于BASE_URL）
 * @param {Object} data - 请求数据（POST/PUT时使用）
 * @param {Object} options - 额外选项（如headers、timeout等）
 * @returns {Promise<Object>} 响应数据
 */
const request = async (method, url, data = null, options = {}) => {
  // 设置默认超时时间（10秒）
  const timeout = options.timeout || 10000
  
  try {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('token')
    
    // 配置请求参数
    const config = {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }
    
    // 如果有 token，添加到 Authorization header
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    // 如果有请求数据，添加到请求体（POST/PUT）
    if (data && (method === 'POST' || method === 'PUT')) {
      config.body = JSON.stringify(data)
    }
    
    // 构建完整的请求URL（GET请求需要在URL中添加参数）
    let fullUrl = `${BASE_URL}${url}`
    if (data && method === 'GET') {
      const params = new URLSearchParams(data)
      fullUrl += `?${params.toString()}`
    }
    
    console.log(`[API请求] ${method} ${fullUrl}`, data ? JSON.stringify(data) : '')
    
    // 创建超时Promise
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('请求超时')), timeout)
    })
    
    // 创建请求Promise
    const requestPromise = fetch(fullUrl, config)
    
    // 发送请求（带超时控制）
    const response = await Promise.race([requestPromise, timeoutPromise])
    
    // 解析响应数据
    const result = await response.json()
    
    // 如果响应状态码不是2xx，视为错误
    if (!response.ok) {
      console.error(`[API错误] ${method} ${fullUrl} - 状态码: ${response.status}`, result)
      return { success: false, message: result.message || '请求失败' }
    }
    
    console.log(`[API成功] ${method} ${fullUrl} - 返回数据条数: ${Array.isArray(result.data) ? result.data.length : 'N/A'}`)
    return result
  } catch (error) {
    // 捕获网络错误、超时或其他异常
    console.error(`[API异常] ${method} ${BASE_URL}${url} - ${error.message}`, error)
    return { 
      success: false, 
      message: error.message === '请求超时' ? '连接超时，请稍后重试' : '网络错误，请稍后重试' 
    }
  }
}

/**
 * 获取商品列表
 * @param {Object} params - 请求参数
 * @param {string} params.search - 搜索关键词
 * @param {number} params.category_id - 分类ID
 * @param {number} params.brand_id - 品牌ID
 * @param {string} params.sort - 排序方式（price-asc, price-desc, sales, rating）
 * @param {number} params.page - 页码，默认1
 * @param {number} params.page_size - 每页数量，默认20
 * @returns {Promise<Object>} 商品列表数据
 */
export const fetchProducts = async (params = {}) => {
  return request('GET', '/products', params)
}

/**
 * 获取商品详情
 * @param {number} id - 商品ID
 * @returns {Promise<Object>} 商品详情数据
 */
export const fetchProductDetail = async (id) => {
  return request('GET', `/products/${id}`)
}

/**
 * 获取分类列表
 * @returns {Promise<Object>} 分类列表数据
 */
export const fetchCategories = async () => {
  return request('GET', '/categories')
}

/**
 * 获取品牌列表
 * @returns {Promise<Object>} 品牌列表数据
 */
export const fetchBrands = async () => {
  return request('GET', '/brands')
}

/**
 * 获取购物车列表
 * @returns {Promise<Object>} 购物车数据
 */
export const fetchCart = async () => {
  return request('GET', '/cart')
}

/**
 * 添加商品到购物车
 * @param {Object} data - 购物车数据
 * @param {number} data.product_id - 商品ID
 * @param {number} data.quantity - 数量
 * @returns {Promise<Object>} 操作结果
 */
export const addToCart = async (data) => {
  return request('POST', '/cart', data)
}

/**
 * 更新购物车商品数量
 * @param {number} id - 购物车项ID
 * @param {Object} data - 更新数据
 * @param {number} data.quantity - 新数量
 * @returns {Promise<Object>} 操作结果
 */
export const updateCartItem = async (id, data) => {
  return request('PUT', `/cart/${id}`, data)
}

/**
 * 删除购物车商品
 * @param {number} id - 购物车项ID
 * @returns {Promise<Object>} 操作结果
 */
export const removeFromCart = async (id) => {
  return request('DELETE', `/cart/${id}`)
}

/**
 * 用户登录
 * @param {Object} data - 登录凭证
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @returns {Promise<Object>} 登录结果
 */
export const login = async (data) => {
  return request('POST', '/auth/login', data)
}

/**
 * 用户注册
 * @param {Object} data - 用户注册数据
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @param {string} data.email - 邮箱
 * @returns {Promise<Object>} 注册结果
 */
export const register = async (data) => {
  return request('POST', '/auth/register', data)
}

/**
 * 获取订单列表
 * @returns {Promise<Object>} 订单列表数据
 */
export const fetchOrders = async () => {
  return request('GET', '/orders')
}

/**
 * 获取地址列表
 * @returns {Promise<Object>} 地址列表数据
 */
export const fetchAddresses = async () => {
  return request('GET', '/addresses')
}

/**
 * 添加收货地址
 * @param {Object} data - 地址数据
 * @param {string} data.consignee - 收货人
 * @param {string} data.phone - 手机号
 * @param {string} data.province - 省
 * @param {string} data.city - 市
 * @param {string} data.district - 区
 * @param {string} data.detail - 详细地址
 * @param {boolean} data.is_default - 是否默认地址
 * @returns {Promise<Object>} 操作结果
 */
export const addAddress = async (data) => {
  return request('POST', '/addresses', data)
}

/**
 * 创建订单
 * @param {Object} data - 订单数据
 * @param {number} data.address_id - 收货地址ID
 * @param {Array} data.items - 订单商品列表
 * @returns {Promise<Object>} 创建结果
 */
export const createOrder = async (data) => {
  return request('POST', '/orders', data)
}

/**
 * 提交商品评价
 * @param {Object} data - 评价数据
 * @param {number} data.product_id - 商品ID
 * @param {number} data.rating - 评分（1-5）
 * @param {string} data.content - 评价内容
 * @param {string} data.order_id - 订单ID
 * @param {boolean} data.is_anonymous - 是否匿名评价
 * @returns {Promise<Object>} 提交结果
 */
export const submitReview = async (data) => {
  return request('POST', '/reviews', data)
}

/**
 * 获取商品评价列表
 * @param {number} productId - 商品ID
 * @param {Object} params - 请求参数
 * @param {number} params.page - 页码，默认1
 * @param {number} params.page_size - 每页数量，默认10
 * @returns {Promise<Object>} 评价列表数据
 */
export const fetchReviews = async (productId, params = {}) => {
  return request('GET', `/reviews/${productId}`, params)
}

/**
 * 订单付款
 * @param {string} orderId - 订单ID
 * @returns {Promise<Object>} 操作结果
 */
export const payOrder = async (orderId) => {
  return request('POST', `/orders/${orderId}/pay`)
}

/**
 * 确认收货
 * @param {string} orderId - 订单ID
 * @returns {Promise<Object>} 操作结果
 */
export const receiveOrder = async (orderId) => {
  return request('POST', `/orders/${orderId}/receive`)
}

/**
 * 订单发货（管理员）
 * @param {string} orderId - 订单ID
 * @returns {Promise<Object>} 操作结果
 */
export const shipOrder = async (orderId) => {
  return request('POST', `/orders/${orderId}/ship`)
}

/**
 * 取消订单
 * @param {string} orderId - 订单ID
 * @returns {Promise<Object>} 操作结果
 */
export const cancelOrder = async (orderId) => {
  return request('POST', `/orders/${orderId}/cancel`)
}