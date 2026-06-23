<script setup>
/**
 * Navbar.vue - 导航栏组件
 * 
 * 【组件用途】
 * 页面顶部导航栏，提供页面跳转链接和用户操作入口
 * 包含 Logo、导航菜单、购物车、登录/注册、订单、退出等功能
 * 
 * 【组件关系】
 * - 被 App.vue 引用，作为全局导航栏
 * - 使用 vue-router 的 router-link 实现页面跳转
 * - 使用 userStore（用户状态管理）获取登录状态和用户信息
 * - 使用 cartStore（购物车状态管理）获取购物车数量
 * 
 * 【数据流转】
 * 1. 从 userStore 获取 isLoggedIn 和 user 数据
 * 2. 从 cartStore 获取 totalItems（购物车商品总数量）
 * 3. 根据登录状态显示不同的菜单项：
 *    - 已登录：显示订单、用户名、退出按钮
 *    - 未登录：显示登录、注册按钮
 * 4. 购物车图标显示商品数量徽章
 * 5. 用户点击退出 → 调用 userStore.logout() 和 cartStore.clearCart() → 跳转到首页
 * 
 * 【功能说明】
 * - Logo 点击跳转到首页
 * - 首页、商品、购物车链接
 * - 根据登录状态动态显示菜单
 * - 购物车数量徽章显示
 * - 退出登录功能
 */

// 导入vue-router的路由钩子
import { useRouter } from 'vue-router'
// 导入用户状态管理store
import { userStore } from '../stores/user'
// 导入购物车状态管理store
import { cartStore } from '../stores/cart'

// 创建路由实例，用于页面跳转
const router = useRouter()

/**
 * 处理退出登录
 * 清除用户状态和购物车数据，然后跳转到首页
 */
const handleLogout = () => {
  // 调用用户store的登出方法
  userStore.logout()
  // 清空购物车
  cartStore.clearCart()
  // 跳转到首页
  router.push('/')
}
</script>

<template>
  <!-- 导航栏容器 -->
  <nav class="navbar">
    <div class="container">
      <!-- Logo区域 -->
      <div class="navbar-brand">
        <!-- Logo链接，点击跳转到首页 -->
        <router-link to="/" class="logo">🛒 红绿灯商城</router-link>
      </div>
      
      <!-- 导航菜单 -->
      <div class="navbar-menu">
        <!-- 首页链接 -->
        <router-link to="/" class="nav-link">首页</router-link>
        <!-- 商品列表链接 -->
        <router-link to="/products" class="nav-link">商品</router-link>
        <!-- 购物车链接（带数量徽章） -->
        <router-link to="/cart" class="nav-link">
          购物车
          <!-- 购物车数量徽章，当购物车有商品时显示 -->
          <span v-if="cartStore.totalItems > 0" class="badge">{{ cartStore.totalItems }}</span>
        </router-link>
        
        <!-- 已登录状态菜单 -->
        <template v-if="userStore.isLoggedIn">
          <!-- 我的订单链接（需要登录） -->
          <router-link to="/orders" class="nav-link">我的订单</router-link>
          <!-- 当前用户名 -->
          <span class="nav-link username">{{ userStore.user?.username || '用户' }}</span>
          <!-- 退出登录按钮 -->
          <button @click="handleLogout" class="btn-logout">退出</button>
        </template>
        
        <!-- 未登录状态菜单 -->
        <template v-else>
          <!-- 登录链接 -->
          <router-link to="/login" class="nav-link">登录</router-link>
          <!-- 注册链接 -->
          <router-link to="/register" class="nav-link">注册</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/**
 * 导航栏样式
 * 使用深色主题设计，配合紫色渐变风格
 */

/* 导航栏容器 */
.navbar {
  /* 深色半透明背景 */
  background: rgba(15, 12, 41, 0.85);
  /* 背景模糊效果 */
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  /* 底部边框 */
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  /* 内边距 */
  padding: .875rem 0;
  /* 粘性定位，固定在顶部 */
  position: sticky;
  top: 0;
  /* 层级，确保在页面内容之上 */
  z-index: 100;
}

/* 内容容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  /* 弹性布局，两端对齐 */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Logo样式 */
.logo {
  font-size: 1.4rem;
  font-weight: bold;
  /* 紫色渐变文字 */
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  /* 移除下划线 */
  text-decoration: none;
}

/* 导航菜单 */
.navbar-menu {
  /* 弹性布局，居中对齐 */
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

/* 导航链接基础样式 */
.nav-link {
  color: rgba(255,255,255,0.7);
  text-decoration: none;
  font-size: .9rem;
  /* 颜色过渡动画 */
  transition: color 0.3s;
  position: relative;
  padding: .35rem 0;
}

/* 导航链接悬停效果 */
.nav-link:hover { color: #fff; }
/* 导航链接激活状态（当前页面） */
.nav-link.router-link-exact-active { color: #a78bfa; }

/* 购物车数量徽章 */
.badge {
  position: absolute;
  top: -8px;
  right: -14px;
  /* 红色渐变背景 */
  background: linear-gradient(135deg, #f43f5e, #e11d48);
  color: white;
  border-radius: 50%;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: bold;
  padding: 0 4px;
}

/* 用户名样式 */
.username {
  padding: .4rem 1rem;
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 20px;
  color: rgba(255,255,255,0.8);
  font-size: .85rem;
}

/* 退出按钮 */
.btn-logout {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.6);
  padding: .4rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-size: .85rem;
  transition: all 0.3s;
}

/* 退出按钮悬停效果 */
.btn-logout:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}
</style>