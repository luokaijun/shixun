/**
 * stores/cart.js - 购物车状态管理
 * 
 * 【模块用途】
 * 管理购物车的状态和操作，包括添加商品、修改数量、删除商品、清空购物车等功能
 * 使用 Vue 的 reactive 响应式 API 创建全局状态，数据持久化到 localStorage
 * 
 * 【模块关系】
 * - 被 ProductCard.vue、ProductDetail.vue、Cart.vue 等组件引用
 * - 通过 localStorage 实现数据持久化（页面刷新后购物车数据不丢失）
 * - 与后端 API 接口交互（后续可扩展）
 * 
 * 【数据结构】
 * cartStore.items: 购物车商品列表数组
 *   - id: 商品ID（唯一标识）
 *   - name: 商品名称
 *   - price: 商品价格
 *   - main_image: 商品主图URL（适配后端返回的字段名）
 *   - description: 商品描述
 *   - quantity: 购买数量
 * 
 * 【核心方法】
 * - addToCart(product, quantity): 添加商品到购物车
 * - updateQuantity(itemId, quantity): 更新购物车商品数量
 * - removeItem(itemId): 从购物车删除商品
 * - clearCart(): 清空购物车
 * - total: 计算属性，返回购物车商品总价
 * - saveToStorage(): 将购物车数据保存到 localStorage
 */

// 导入Vue的响应式API
import { reactive } from 'vue'

/**
 * 从 localStorage 初始化购物车数据
 * 如果 localStorage 中没有数据，则初始化为空数组
 */
const savedCart = JSON.parse(localStorage.getItem('cart') || '[]')

/**
 * 创建购物车状态管理对象
 * 使用 reactive 创建响应式对象，所有组件共享同一个实例
 */
export const cartStore = reactive({
  /**
   * 购物车商品列表
   * 从 localStorage 加载初始化数据
   */
  items: savedCart,

  /**
   * 添加商品到购物车
   * @param {Object} product - 商品对象
   * @param {number} quantity - 添加数量，默认为1
   */
  addToCart(product, quantity = 1) {
    // 查找购物车中是否已存在该商品
    const existingItem = this.items.find(item => item.id === product.id)
    
    if (existingItem) {
      // 如果已存在，增加数量
      existingItem.quantity += quantity
    } else {
      // 如果不存在，添加新商品到购物车
      this.items.push({
        id: product.id,
        name: product.name,
        price: product.price,
        // 使用后端返回的 main_image 字段（替代原来的 image 字段）
        main_image: product.main_image,
        description: product.description,
        quantity: quantity
      })
    }
    
    // 将更新后的购物车数据保存到 localStorage
    this.saveToStorage()
  },

  /**
   * 更新购物车商品数量
   * @param {number} itemId - 商品ID
   * @param {number} quantity - 新的数量
   */
  updateQuantity(itemId, quantity) {
    // 查找对应的商品
    const item = this.items.find(item => item.id === itemId)
    if (item) {
      // 更新数量
      item.quantity = quantity
      // 将更新后的购物车数据保存到 localStorage
      this.saveToStorage()
    }
  },

  /**
   * 从购物车删除商品
   * @param {number} itemId - 商品ID
   */
  removeItem(itemId) {
    // 过滤掉指定ID的商品
    this.items = this.items.filter(item => item.id !== itemId)
    // 将更新后的购物车数据保存到 localStorage
    this.saveToStorage()
  },

  /**
   * 计算属性：购物车商品总价
   * @returns {number} 总价
   */
  get total() {
    // 使用 reduce 计算所有商品的价格总和
    return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  },

  /**
   * 计算属性：购物车商品总数量
   * @returns {number} 总数量
   */
  get totalItems() {
    // 使用 reduce 计算所有商品的数量总和
    return this.items.reduce((sum, item) => sum + item.quantity, 0)
  },

  /**
   * 获取购物车商品列表（用于模板渲染）
   * @returns {Array} 购物车商品列表，每个商品包含完整信息
   */
  get cartItems() {
    // 返回包含完整商品信息的购物车列表
    return this.items.map(item => ({
      id: item.id,
      product_id: item.id,
      quantity: item.quantity,
      // 将商品信息封装到 product 对象中，保持与后端API返回格式一致
      product: {
        id: item.id,
        name: item.name,
        price: item.price,
        main_image: item.main_image,
        description: item.description
      }
    }))
  },

  /**
   * 清空购物车
   */
  clearCart() {
    // 清空商品列表
    this.items = []
    // 将更新后的购物车数据保存到 localStorage
    this.saveToStorage()
  },

  /**
   * 将购物车数据保存到 localStorage
   * 实现数据持久化，页面刷新后购物车数据不丢失
   */
  saveToStorage() {
    localStorage.setItem('cart', JSON.stringify(this.items))
  }
})