<script setup>
/**
 * ProductCard.vue - 商品卡片组件
 * 
 * 【组件用途】
 * 用于展示单个商品的卡片，包含商品图片、名称、价格、销量、评分等信息
 * 提供点击跳转详情页和加入购物车的功能
 * 
 * 【组件关系】
 * - 被 Home.vue（首页）、Products.vue（商品列表页）引用
 * - 通过 props 接收 product 对象数据
 * - 使用 cartStore（购物车状态管理）处理加入购物车逻辑
 * - 使用 vue-router 的 useRouter 进行页面跳转
 * 
 * 【数据流转】
 * 1. 父组件传入 product 对象（包含商品的所有信息）
 * 2. 组件渲染商品图片、名称、价格等信息
 * 3. 用户点击卡片 → 调用 goToDetail() → 路由跳转到商品详情页
 * 4. 用户点击"加入购物车"按钮 → 调用 addToCart() → 调用 cartStore.addToCart() → 更新购物车状态
 * 
 * 【字段说明】
 * - product.main_image: 商品主图URL（后端返回的字段名，替代原来的 image）
 * - product.name: 商品名称
 * - product.description: 商品描述
 * - product.price: 商品价格
 * - product.original_price: 商品原价（划线价）
 * - product.sales: 销量
 * - product.rating: 评分
 */

// 导入 vue-router 的路由跳转钩子
import { useRouter } from 'vue-router'
// 导入购物车状态管理 store，用于处理购物车操作
import { cartStore } from '../stores/cart'

/**
 * 定义组件的 props（外部传入的数据）
 * @prop {Object} product - 商品对象，必填
 */
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

// 创建路由实例，用于页面跳转
const router = useRouter()

/**
 * 跳转到商品详情页
 * 当用户点击商品卡片时触发
 */
const goToDetail = () => {
  // 跳转到 /product/:id 路由，传入商品ID
  router.push(`/product/${props.product.id}`)
}

/**
 * 将商品加入购物车
 * @param {Event} e - 点击事件对象
 */
const addToCart = async (e) => {
  // 阻止事件冒泡，避免同时触发 goToDetail()
  e.stopPropagation()
  try {
    // 调用购物车 store 的添加方法
    await cartStore.addToCart(props.product)
    // 添加成功后显示提示
    alert('已添加到购物车')
  } catch (error) {
    // 添加失败时显示错误提示
    alert('添加失败，请重试')
  }
}
</script>

<template>
  <!-- 商品卡片容器，点击时跳转到详情页 -->
  <div class="product-card" @click="goToDetail">
    <!-- 商品图片区域 -->
    <div class="product-image">
      <!-- 
        使用后端返回的 main_image 字段作为商品主图
        如果没有主图，则显示占位图
      -->
      <img 
        :src="product.main_image || 'https://via.placeholder.com/300x300?text=商品图片'" 
        :alt="product.name" 
      />
      <!-- 折扣标签（如果有折扣） -->
      <span v-if="product.discount" class="discount-tag">{{ product.discount }}折</span>
    </div>
    
    <!-- 商品信息区域 -->
    <div class="product-info">
      <!-- 商品名称 -->
      <h3 class="product-name">{{ product.name }}</h3>
      <!-- 商品描述 -->
      <p class="product-desc">{{ product.description }}</p>
      
      <!-- 商品底部：价格和购物车按钮 -->
      <div class="product-footer">
        <!-- 价格区域 -->
        <div class="price-wrapper">
          <!-- 当前价格（红色高亮） -->
          <span class="price">¥{{ product.price }}</span>
          <!-- 原价（划线价，灰色显示） -->
          <span v-if="product.original_price" class="original-price">¥{{ product.original_price }}</span>
        </div>
        
        <!-- 加入购物车按钮 -->
        <button class="add-cart-btn" @click="addToCart">
          🛒 加入购物车
        </button>
      </div>
      
      <!-- 销量和评分信息 -->
      <div class="product-sales">
        <span>已售 {{ product.sales || 0 }}</span>
        <span>⭐ {{ product.rating || 5.0 }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/**
 * 商品卡片样式
 * 使用深色主题设计，配合紫色渐变风格
 */

/* 卡片容器 */
.product-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

/* 卡片悬停效果 */
.product-card:hover {
  transform: translateY(-6px);
  border-color: rgba(139, 92, 246, 0.3);
  box-shadow: 0 12px 35px rgba(139, 92, 246, 0.15);
}

/* 商品图片区域 */
.product-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: rgba(255,255,255,0.02);
}

/* 商品图片 */
.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

/* 图片悬停放大效果 */
.product-card:hover .product-image img {
  transform: scale(1.05);
}

/* 折扣标签 */
.discount-tag {
  position: absolute;
  top: 10px;
  right: 10px;
  background: linear-gradient(135deg, #f43f5e, #e11d48);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: .75rem;
  font-weight: bold;
}

/* 商品信息区域 */
.product-info {
  padding: 1rem;
}

/* 商品名称 */
.product-name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: .5rem;
  color: rgba(255,255,255,0.85);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 商品描述 */
.product-desc {
  font-size: .85rem;
  color: rgba(255,255,255,0.4);
  margin-bottom: .75rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 商品底部区域 */
.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: .5rem;
}

/* 价格包装器 */
.price-wrapper {
  display: flex;
  align-items: baseline;
  gap: .5rem;
}

/* 当前价格 */
.price {
  font-size: 1.25rem;
  font-weight: bold;
  color: #f87171;
}

/* 原价 */
.original-price {
  font-size: .85rem;
  color: rgba(255,255,255,0.25);
  text-decoration: line-through;
}

/* 加入购物车按钮 */
.add-cart-btn {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
  border: none;
  padding: .5rem 1rem;
  border-radius: 20px;
  font-size: .85rem;
  cursor: pointer;
  transition: transform .2s, box-shadow .2s;
}

/* 按钮悬停效果 */
.add-cart-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
}

/* 销量和评分信息 */
.product-sales {
  display: flex;
  justify-content: space-between;
  font-size: .75rem;
  color: rgba(255,255,255,0.3);
}
</style>