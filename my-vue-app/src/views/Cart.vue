<script setup>
/**
 * Cart.vue - 购物车页面
 * 
 * 【页面用途】
 * 展示用户购物车中的商品列表，支持修改数量、删除商品、清空购物车、结算功能
 * 是用户下单前的关键页面
 * 
 * 【页面关系】
 * - 路由路径：/cart
 * - 使用 cartStore（购物车状态管理）获取和操作购物车数据
 * - 使用 vue-router 的 useRouter 进行页面跳转
 * 
 * 【数据流转】
 * 1. 页面挂载 → 从 cartStore 获取购物车数据（cartItems）
 * 2. 渲染购物车商品列表（包含商品图片、名称、价格、数量）
 * 3. 用户修改数量 → 调用 cartStore.updateQuantity() → 更新购物车状态
 * 4. 用户删除商品 → 调用 cartStore.removeFromCart() → 更新购物车状态
 * 5. 用户清空购物车 → 调用 cartStore.clearCart() → 更新购物车状态
 * 6. 用户结算 → 跳转到订单页面（预留功能）
 * 
 * 【API接口】
 * - 通过 cartStore 调用后端API（详见 stores/cart.js）
 *   - GET /api/cart - 获取购物车列表
 *   - POST /api/cart - 添加商品到购物车
 *   - PUT /api/cart/:id - 更新购物车商品数量
 *   - DELETE /api/cart/:id - 删除购物车商品
 * 
 * 【数据字段】
 * - cartItems: 购物车商品列表（从 cartStore 获取）
 *   - id: 购物车项ID
 *   - product_id: 商品ID
 *   - product: 商品对象（包含 main_image、name、price 等）
 *   - quantity: 购买数量
 * - cartStore.totalItems: 购物车商品总数量
 * - cartStore.totalPrice: 购物车商品总价格
 */

// 导入vue-router的路由钩子
import { useRouter } from 'vue-router'
// 导入购物车状态管理store
import { cartStore } from '../stores/cart'

// 创建路由实例，用于页面跳转
const router = useRouter()

/**
 * 更新购物车商品数量
 * @param {number} cartItemId - 购物车项ID
 * @param {number} quantity - 新的数量
 */
const updateQuantity = async (cartItemId, quantity) => {
  // 数量不能小于1
  if (quantity < 1) return
  
  try {
    // 调用购物车store的更新数量方法
    await cartStore.updateQuantity(cartItemId, quantity)
  } catch (error) {
    // 更新失败时显示错误提示
    alert('更新数量失败，请重试')
  }
}

/**
 * 删除购物车商品
 * @param {number} cartItemId - 购物车项ID
 */
const removeItem = async (cartItemId) => {
  // 确认删除操作
  if (!confirm('确定要删除该商品吗？')) return
  
  try {
    // 调用购物车store的删除方法
    await cartStore.removeItem(cartItemId)
  } catch (error) {
    // 删除失败时显示错误提示
    alert('删除失败，请重试')
  }
}

/**
 * 清空购物车
 */
const clearCart = async () => {
  // 确认清空操作
  if (!confirm('确定要清空购物车吗？')) return
  
  try {
    // 调用购物车store的清空方法
    await cartStore.clearCart()
  } catch (error) {
    // 清空失败时显示错误提示
    alert('清空失败，请重试')
  }
}

const checkout = () => {
  if (cartStore.totalItems === 0) {
    alert('购物车为空，请先添加商品')
    return
  }
  router.push('/checkout')
}
</script>

<template>
  <!-- 购物车页面容器 -->
  <div class="cart-page">
    <div class="container">
      <!-- 页面标题 -->
      <h1 class="page-title">🛒 购物车</h1>
      
      <!-- 购物车为空状态 -->
      <div v-if="cartStore.totalItems === 0" class="empty-cart">
        <div class="empty-icon">🛒</div>
        <p>购物车是空的</p>
        <button class="empty-btn" @click="router.push('/products')">去选购商品</button>
      </div>
      
      <!-- 购物车内容 -->
      <div v-else class="cart-content">
        <!-- 购物车列表 -->
        <div class="cart-list">
          <!-- 购物车商品项 -->
          <div v-for="item in cartStore.cartItems" :key="item.id" class="cart-item">
            <!-- 商品图片 -->
            <div class="cart-item-image">
              <!-- 
                使用商品的 main_image 字段作为图片
                如果没有主图，显示占位图
              -->
              <img 
                :src="item.product?.main_image || 'https://via.placeholder.com/150x150?text=商品图片'" 
                :alt="item.product?.name || '商品'" 
              />
            </div>
            
            <!-- 商品信息 -->
            <div class="cart-item-info">
              <!-- 商品名称 -->
              <h3 class="cart-item-name">{{ item.product?.name || '未知商品' }}</h3>
              <!-- 商品描述 -->
              <p class="cart-item-desc">{{ item.product?.description || '' }}</p>
              <!-- 商品价格 -->
              <span class="cart-item-price">¥{{ item.product?.price || 0 }}</span>
            </div>
            
            <!-- 数量控制 -->
            <div class="cart-item-quantity">
              <button 
                class="qty-btn" 
                :disabled="item.quantity <= 1" 
                @click="updateQuantity(item.id, item.quantity - 1)"
              >
                -
              </button>
              <span class="qty-value">{{ item.quantity }}</span>
              <button 
                class="qty-btn" 
                @click="updateQuantity(item.id, item.quantity + 1)"
              >
                +
              </button>
            </div>
            
            <!-- 小计价格 -->
            <div class="cart-item-subtotal">
              ¥{{ (item.product?.price || 0) * item.quantity }}
            </div>
            
            <!-- 删除按钮 -->
            <div class="cart-item-delete">
              <button class="delete-btn" @click="removeItem(item.id)">删除</button>
            </div>
          </div>
        </div>
        
        <!-- 购物车底部 -->
        <div class="cart-footer">
          <!-- 清空购物车按钮 -->
          <button class="clear-btn" @click="clearCart">清空购物车</button>
          
          <!-- 结算区域 -->
          <div class="checkout-section">
            <!-- 商品总数 -->
            <span class="total-items">共 {{ cartStore.totalItems }} 件商品</span>
            <!-- 总价 -->
            <div class="total-price">
              <span class="label">合计：</span>
              <span class="value">¥{{ cartStore.total }}</span>
            </div>
            <!-- 结算按钮 -->
            <button class="checkout-btn" @click="checkout">结算</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/**
 * 购物车页面样式
 * 使用深色主题设计，配合紫色渐变风格
 */

/* 页面容器 */
.cart-page {
  min-height: 100vh;
  background: #0a0a1a;
  padding: 2rem 0;
}

/* 内容容器 */
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* 页面标题 */
.page-title {
  font-size: 2rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 2rem;
}

/* 空购物车状态 */
.empty-cart {
  text-align: center;
  padding: 5rem 0;
}

/* 空购物车图标 */
.empty-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
}

/* 空购物车提示文字 */
.empty-cart p {
  color: rgba(255,255,255,0.4);
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

/* 空购物车按钮 */
.empty-btn {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform .2s, box-shadow .2s;
}

/* 空购物车按钮悬停效果 */
.empty-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
}

/* 购物车内容 */
.cart-content {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  overflow: hidden;
}

/* 购物车列表 */
.cart-list {
  padding: 1rem;
}

/* 购物车商品项 */
.cart-item {
  display: flex;
  align-items: center;
  padding: 1.5rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  transition: background .3s;
}

/* 购物车商品项悬停效果 */
.cart-item:hover {
  background: rgba(255,255,255,0.02);
}

/* 商品项最后一项移除底部边框 */
.cart-item:last-child {
  border-bottom: none;
}

/* 商品图片 */
.cart-item-image {
  width: 100px;
  height: 100px;
  background: rgba(255,255,255,0.04);
  border-radius: 10px;
  overflow: hidden;
  margin-right: 1.5rem;
}

/* 商品图片内容 */
.cart-item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 商品信息 */
.cart-item-info {
  flex: 1;
  min-width: 0;
}

/* 商品名称 */
.cart-item-name {
  font-size: 1rem;
  font-weight: 600;
  color: rgba(255,255,255,0.85);
  margin-bottom: .25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 商品描述 */
.cart-item-desc {
  font-size: .85rem;
  color: rgba(255,255,255,0.3);
  margin-bottom: .5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 商品价格 */
.cart-item-price {
  font-size: 1.1rem;
  font-weight: bold;
  color: #f87171;
}

/* 数量控制 */
.cart-item-quantity {
  display: flex;
  align-items: center;
  gap: .75rem;
  margin: 0 1.5rem;
}

/* 数量按钮 */
.qty-btn {
  width: 32px;
  height: 32px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.04);
  color: rgba(255,255,255,0.7);
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all .3s;
}

/* 数量按钮悬停效果 */
.qty-btn:hover:not(:disabled) {
  border-color: #8b5cf6;
  color: #a78bfa;
}

/* 数量按钮禁用状态 */
.qty-btn:disabled {
  opacity: .4;
  cursor: not-allowed;
}

/* 数量值 */
.qty-value {
  min-width: 30px;
  text-align: center;
  color: rgba(255,255,255,0.8);
  font-size: 1rem;
}

/* 小计价格 */
.cart-item-subtotal {
  min-width: 80px;
  text-align: right;
  font-size: 1.1rem;
  font-weight: bold;
  color: rgba(255,255,255,0.9);
  margin-right: 1.5rem;
}

/* 删除按钮区域 */
.cart-item-delete {
  min-width: 60px;
}

/* 删除按钮 */
.delete-btn {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.4);
  padding: .5rem 1rem;
  border-radius: 8px;
  font-size: .85rem;
  cursor: pointer;
  transition: all .3s;
}

/* 删除按钮悬停效果 */
.delete-btn:hover {
  border-color: #ef4444;
  color: #f87171;
}

/* 购物车底部 */
.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1rem;
  background: rgba(255,255,255,0.02);
  border-top: 1px solid rgba(255,255,255,0.06);
}

/* 清空购物车按钮 */
.clear-btn {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.4);
  padding: .75rem 1.5rem;
  border-radius: 10px;
  font-size: .9rem;
  cursor: pointer;
  transition: all .3s;
}

/* 清空购物车按钮悬停效果 */
.clear-btn:hover {
  border-color: #ef4444;
  color: #f87171;
}

/* 结算区域 */
.checkout-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

/* 商品总数 */
.total-items {
  color: rgba(255,255,255,0.4);
  font-size: .9rem;
}

/* 总价 */
.total-price {
  display: flex;
  align-items: baseline;
  gap: .25rem;
}

/* 总价标签 */
.total-price .label {
  color: rgba(255,255,255,0.5);
  font-size: .9rem;
}

/* 总价数值 */
.total-price .value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #f87171;
}

/* 结算按钮 */
.checkout-btn {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
  border: none;
  padding: .75rem 2rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform .2s, box-shadow .2s;
}

/* 结算按钮悬停效果 */
.checkout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
}

/* 响应式布局 */
@media (max-width: 768px) {
  /* 购物车商品项 */
  .cart-item {
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;
  }
  
  /* 商品信息 */
  .cart-item-info {
    width: calc(100% - 115px);
  }
  
  /* 数量控制 */
  .cart-item-quantity {
    margin: 0;
    order: 4;
  }
  
  /* 小计价格 */
  .cart-item-subtotal {
    margin: 0;
    order: 3;
  }
  
  /* 删除按钮 */
  .cart-item-delete {
    order: 5;
  }
  
  /* 购物车底部 */
  .cart-footer {
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  /* 结算区域 */
  .checkout-section {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>