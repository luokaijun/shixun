<script setup>
/**
 * ProductDetail.vue - 商品详情页面
 * 
 * 【页面用途】
 * 展示单个商品的详细信息，包括多图展示、商品参数、价格、库存等
 * 提供加入购物车和立即购买功能
 * 
 * 【页面关系】
 * - 路由路径：/product/:id（动态路由，接收商品ID参数）
 * - 通过 API 模块（api/index.js）从后端获取商品详情数据
 * - 使用 cartStore（购物车状态管理）处理加入购物车逻辑
 * - 使用 vue-router 的 useRoute 获取路由参数
 * - 使用 vue-router 的 useRouter 进行页面跳转
 * 
 * 【数据流转】
 * 1. 路由参数获取商品ID → useRoute().params.id
 * 2. 调用 fetchProductDetail(id) → 获取商品详情数据
 * 3. 渲染商品图片（多图轮播）、名称、价格、描述等信息
 * 4. 用户点击"加入购物车" → 调用 cartStore.addToCart() → 更新购物车状态
 * 5. 用户点击"立即购买" → 跳转到订单页面或直接下单
 * 
 * 【API接口】
 * - GET /api/products/:id - 获取商品详情（包含多图、分类、品牌信息）
 * 
 * 【数据字段】
 * - product: 商品详情对象
 *   - main_image: 商品主图
 *   - images: 商品图片列表（数组，包含所有商品图片）
 *   - name: 商品名称
 *   - description: 商品描述
 *   - price: 商品价格
 *   - original_price: 商品原价
 *   - stock: 库存数量
 *   - sales: 销量
 *   - rating: 评分
 *   - category: 分类信息（嵌套对象）
 *   - brand: 品牌信息（嵌套对象）
 * - selectedImageIndex: 当前选中的图片索引（用于图片切换）
 * - quantity: 购买数量
 */

// 导入Vue响应式API
import { ref, onMounted } from 'vue'
// 导入vue-router的路由钩子
import { useRoute, useRouter } from 'vue-router'
// 导入后端API调用函数
import { fetchProductDetail } from '../api/index'
// 导入购物车状态管理store
import { cartStore } from '../stores/cart'

/**
 * 响应式数据定义
 */

// 商品详情数据
const product = ref(null)
// 当前选中的图片索引
const selectedImageIndex = ref(0)
// 购买数量
const quantity = ref(1)
// 加载状态
const loading = ref(true)

// 创建路由实例，用于获取路由参数
const route = useRoute()
// 创建路由实例，用于页面跳转
const router = useRouter()

/**
 * 从后端获取商品详情数据
 */
const loadProduct = async () => {
  // 从路由参数中获取商品ID
  const id = route.params.id
  if (!id) {
    console.error('商品ID不存在')
    return
  }
  
  loading.value = true
  try {
    // 调用后端API获取商品详情
    const result = await fetchProductDetail(id)
    if (result.success) {
      // 成功获取数据，更新商品详情
      product.value = result.data || null
      // 初始化图片索引为0
      selectedImageIndex.value = 0
    } else {
      // 获取失败，显示错误信息
      console.error('获取商品详情失败:', result.message)
      product.value = null
    }
  } catch (error) {
    // 网络错误或其他异常
    console.error('获取商品详情异常:', error)
    product.value = null
  } finally {
    // 无论成功与否，都结束加载状态
    loading.value = false
  }
}

/**
 * 切换选中的图片
 * @param {number} index - 图片索引
 */
const selectImage = (index) => {
  selectedImageIndex.value = index
}

/**
 * 将商品加入购物车
 */
const addToCart = async () => {
  if (!product.value) return
  
  try {
    // 调用购物车store的添加方法，传入商品和数量
    await cartStore.addToCart(product.value, quantity.value)
    // 添加成功后显示提示
    alert(`已添加 ${quantity.value} 件商品到购物车`)
  } catch (error) {
    // 添加失败时显示错误提示
    alert('添加失败，请重试')
  }
}

/**
 * 立即购买
 */
const buyNow = async () => {
  if (!product.value) return
  
  try {
    // 先添加到购物车
    await cartStore.addToCart(product.value, quantity.value)
    // 然后跳转到购物车页面
    router.push('/cart')
  } catch (error) {
    // 操作失败时显示错误提示
    alert('购买失败，请重试')
  }
}

/**
 * 页面挂载时初始化数据
 */
onMounted(() => {
  loadProduct()
})
</script>

<template>
  <!-- 商品详情页面容器 -->
  <div class="product-detail-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <!-- 商品不存在状态 -->
    <div v-else-if="!product" class="not-found">
      <p>商品不存在或已下架</p>
    </div>
    
    <!-- 商品详情内容 -->
    <div v-else class="container">
      <!-- 商品图片区域 -->
      <div class="product-images">
        <!-- 主图展示 -->
        <div class="main-image">
          <!-- 
            使用商品图片列表中的当前选中图片
            如果没有图片，显示占位图
          -->
          <img 
            :src="(product.images && product.images[selectedImageIndex]) || product.main_image || 'https://via.placeholder.com/600x600?text=商品图片'" 
            :alt="product.name" 
          />
        </div>
        
        <!-- 缩略图列表 -->
        <div class="thumbnails">
          <!-- 
            遍历商品图片列表，生成缩略图
            如果有主图，将主图放在第一位
          -->
          <div 
            v-for="(img, index) in (product.images || [product.main_image]).filter(Boolean)" 
            :key="index"
            :class="['thumbnail', { active: index === selectedImageIndex }]"
            @click="selectImage(index)"
          >
            <img :src="img" :alt="`${product.name} - ${index + 1}`" />
          </div>
        </div>
      </div>
      
      <!-- 商品信息区域 -->
      <div class="product-info">
        <!-- 商品名称 -->
        <h1 class="product-name">{{ product.name }}</h1>
        
        <!-- 商品描述 -->
        <p class="product-desc">{{ product.description }}</p>
        
        <!-- 价格区域 -->
        <div class="price-section">
          <span class="current-price">¥{{ product.price }}</span>
          <span v-if="product.original_price" class="original-price">¥{{ product.original_price }}</span>
          <span v-if="product.discount" class="discount-badge">{{ product.discount }}折</span>
        </div>
        
        <!-- 商品参数 -->
        <div class="product-specs">
          <div class="spec-item">
            <span class="label">分类</span>
            <span class="value">{{ product.category?.name || '-' }}</span>
          </div>
          <div class="spec-item">
            <span class="label">品牌</span>
            <span class="value">{{ product.brand?.name || '-' }}</span>
          </div>
          <div class="spec-item">
            <span class="label">销量</span>
            <span class="value">{{ product.sales || 0 }}件</span>
          </div>
          <div class="spec-item">
            <span class="label">评分</span>
            <span class="value">⭐ {{ product.rating || 5.0 }}</span>
          </div>
          <div class="spec-item">
            <span class="label">库存</span>
            <span :class="['value', { low: (product.stock || 0) < 10 }]">
              {{ product.stock || 0 }}件
            </span>
          </div>
        </div>
        
        <!-- 数量选择 -->
        <div class="quantity-section">
          <span class="label">数量</span>
          <div class="quantity-control">
            <button 
              class="qty-btn" 
              :disabled="quantity <= 1" 
              @click="quantity = Math.max(1, quantity - 1)"
            >
              -
            </button>
            <input 
              type="number" 
              v-model.number="quantity" 
              min="1" 
              :max="product.stock || 999"
              class="qty-input"
            />
            <button 
              class="qty-btn" 
              :disabled="(product.stock || 0) <= quantity" 
              @click="quantity = Math.min(product.stock || 999, quantity + 1)"
            >
              +
            </button>
          </div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button class="btn btn-cart" @click="addToCart">
            🛒 加入购物车
          </button>
          <button class="btn btn-buy" @click="buyNow">
            立即购买
          </button>
        </div>
      </div>
      
      <!-- 商品详情描述 -->
      <div class="product-details">
        <h2>商品详情</h2>
        <div class="detail-content">
          <!-- 渲染商品详情内容（支持HTML） -->
          <div v-html="product.detail || product.description"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/**
 * 商品详情页面样式
 * 使用深色主题设计，配合紫色渐变风格
 */

/* 页面容器 */
.product-detail-page {
  min-height: 100vh;
  background: #0a0a1a;
  padding: 2rem 0;
}

/* 加载和不存在状态 */
.loading, .not-found {
  text-align: center;
  padding: 5rem;
  color: rgba(255,255,255,0.5);
  font-size: 1.2rem;
}

/* 内容容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* 商品图片和信息区域 */
.product-images, .product-info {
  display: inline-block;
  vertical-align: top;
}

/* 商品图片区域 */
.product-images {
  width: 45%;
  margin-right: 5%;
}

/* 主图展示 */
.main-image {
  width: 100%;
  height: 500px;
  background: rgba(255,255,255,0.03);
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 1rem;
}

/* 主图图片 */
.main-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* 缩略图列表 */
.thumbnails {
  display: flex;
  gap: .5rem;
  overflow-x: auto;
  padding-bottom: .5rem;
}

/* 缩略图 */
.thumbnail {
  width: 80px;
  height: 80px;
  border: 2px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  flex-shrink: 0;
  transition: border-color .3s;
}

/* 缩略图图片 */
.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 缩略图激活状态 */
.thumbnail.active {
  border-color: #8b5cf6;
}

/* 商品信息区域 */
.product-info {
  width: 50%;
}

/* 商品名称 */
.product-name {
  font-size: 1.75rem;
  font-weight: bold;
  color: rgba(255,255,255,0.9);
  margin-bottom: 1rem;
}

/* 商品描述 */
.product-desc {
  font-size: 1rem;
  color: rgba(255,255,255,0.5);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

/* 价格区域 */
.price-section {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  margin-bottom: 2rem;
}

/* 当前价格 */
.current-price {
  font-size: 2.25rem;
  font-weight: bold;
  color: #f87171;
}

/* 原价 */
.original-price {
  font-size: 1.1rem;
  color: rgba(255,255,255,0.3);
  text-decoration: line-through;
}

/* 折扣标签 */
.discount-badge {
  background: linear-gradient(135deg, #f43f5e, #e11d48);
  color: white;
  padding: .25rem .75rem;
  border-radius: 6px;
  font-size: .9rem;
  font-weight: bold;
}

/* 商品参数区域 */
.product-specs {
  background: rgba(255,255,255,0.03);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

/* 参数项 */
.spec-item {
  display: flex;
  justify-content: space-between;
  padding: .75rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

/* 参数项最后一项移除底部边框 */
.spec-item:last-child {
  border-bottom: none;
}

/* 参数标签 */
.spec-item .label {
  color: rgba(255,255,255,0.4);
}

/* 参数值 */
.spec-item .value {
  color: rgba(255,255,255,0.8);
}

/* 库存不足样式 */
.spec-item .value.low {
  color: #f87171;
}

/* 数量选择区域 */
.quantity-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

/* 标签 */
.quantity-section .label {
  color: rgba(255,255,255,0.7);
  font-size: 1rem;
}

/* 数量控制 */
.quantity-control {
  display: flex;
  align-items: center;
  background: rgba(255,255,255,0.04);
  border-radius: 10px;
  overflow: hidden;
}

/* 数量按钮 */
.qty-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.7);
  font-size: 1.2rem;
  cursor: pointer;
  transition: background .3s;
}

/* 数量按钮悬停效果 */
.qty-btn:hover:not(:disabled) {
  background: rgba(255,255,255,0.1);
}

/* 数量按钮禁用状态 */
.qty-btn:disabled {
  opacity: .4;
  cursor: not-allowed;
}

/* 数量输入框 */
.qty-input {
  width: 60px;
  height: 40px;
  border: none;
  background: transparent;
  color: rgba(255,255,255,0.9);
  text-align: center;
  font-size: 1rem;
}

/* 数量输入框聚焦样式 */
.qty-input:focus {
  outline: none;
}

/* 操作按钮区域 */
.action-buttons {
  display: flex;
  gap: 1rem;
}

/* 按钮基础样式 */
.btn {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform .2s, box-shadow .2s;
}

/* 加入购物车按钮 */
.btn-cart {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

/* 加入购物车按钮悬停效果 */
.btn-cart:hover {
  background: rgba(139, 92, 246, 0.3);
  transform: translateY(-2px);
}

/* 立即购买按钮 */
.btn-buy {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
}

/* 立即购买按钮悬停效果 */
.btn-buy:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
}

/* 商品详情描述区域 */
.product-details {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255,255,255,0.06);
}

/* 详情标题 */
.product-details h2 {
  font-size: 1.5rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 1.5rem;
}

/* 详情内容 */
.detail-content {
  color: rgba(255,255,255,0.6);
  line-height: 1.8;
}

/* 详情内容中的图片 */
.detail-content img {
  max-width: 100%;
  border-radius: 8px;
  margin: 1rem 0;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .product-images, .product-info {
    width: 100%;
    margin-right: 0;
  }
  
  .product-images {
    margin-bottom: 2rem;
  }
  
  .main-image {
    height: 350px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>