<script setup>
/**
 * Home.vue - 首页
 * 
 * 【页面用途】
 * 电商系统的首页，展示热门商品、新品上架、分类导航等内容
 * 是用户进入系统后看到的第一个页面
 * 
 * 【页面关系】
 * - 路由路径：/（根路径）
 * - 引用 ProductCard.vue 组件展示商品卡片
 * - 通过 API 模块（api/index.js）从后端获取商品和分类数据
 * - 使用 vue-router 的 useRouter 进行页面跳转
 * 
 * 【数据流转】
 * 1. 页面挂载 → 调用 fetchProducts 获取商品列表
 * 2. 根据销量筛选热销商品 → hotProducts（计算属性）
 * 3. 根据创建时间筛选新品 → newProducts（计算属性）
 * 4. 渲染首页轮播图、分类导航、热销商品、新品区域
 * 5. 用户点击商品 → 跳转到商品详情页
 * 6. 用户点击分类 → 跳转到分类商品列表页
 * 
 * 【API接口】
 * - GET /api/products - 获取商品列表（用于筛选热销和新品）
 * - GET /api/categories - 获取分类列表（用于分类导航）
 * 
 * 【数据字段】
 * - products: 商品列表数据
 * - categories: 分类列表数据
 * - loading: 加载状态
 * - hotProducts: 热销商品（销量前8）
 * - newProducts: 新品（按创建时间排序前8）
 */

// 导入Vue响应式API
import { ref, computed, onMounted } from 'vue'
// 导入vue-router的路由钩子
import { useRouter } from 'vue-router'
// 导入后端API调用函数
import { fetchProducts, fetchCategories } from '../api/index'
// 导入商品卡片组件
import ProductCard from '../components/ProductCard.vue'

/**
 * 响应式数据定义
 */

// 商品列表数据
const products = ref([])
// 分类列表数据
const categories = ref([])
// 加载状态
const loading = ref(true)

// 创建路由实例，用于页面跳转
const router = useRouter()

/**
 * 从后端获取商品数据
 */
const loadProducts = async () => {
  loading.value = true
  try {
    // 调用后端API获取商品列表（获取更多商品用于筛选）
    const result = await fetchProducts({ page_size: 50 })
    if (result.success) {
      // 成功获取数据，更新商品列表
      products.value = result.data || []
    } else {
      // 获取失败，显示错误信息
      console.error('获取商品列表失败:', result.message)
      products.value = []
    }
  } catch (error) {
    // 网络错误或其他异常
    console.error('获取商品列表异常:', error)
    products.value = []
  } finally {
    // 无论成功与否，都结束加载状态
    loading.value = false
  }
}

/**
 * 从后端获取分类数据
 */
const loadCategories = async () => {
  try {
    // 调用后端API获取分类列表
    const result = await fetchCategories()
    if (result.success) {
      // 成功获取数据，更新分类列表
      categories.value = result.data || []
    } else {
      // 获取失败，显示错误信息
      console.error('获取分类列表失败:', result.message)
      categories.value = []
    }
  } catch (error) {
    // 网络错误或其他异常
    console.error('获取分类列表异常:', error)
    categories.value = []
  }
}

/**
 * 计算属性：热销商品
 * 根据销量排序，取前8个商品
 */
const hotProducts = computed(() => {
  return [...products.value]
    .sort((a, b) => (b.sales || 0) - (a.sales || 0))
    .slice(0, 8)
})

/**
 * 计算属性：新品
 * 根据创建时间排序，取前8个商品
 */
const newProducts = computed(() => {
  return [...products.value]
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    .slice(0, 8)
})

/**
 * 跳转到分类商品列表页
 * @param {number} categoryId - 分类ID
 */
const goToCategory = (categoryId) => {
  router.push(`/products?category_id=${categoryId}`)
}

/**
 * 跳转到全部商品页面
 */
const goToAllProducts = () => {
  router.push('/products')
}

/**
 * 页面挂载时初始化数据
 */
onMounted(() => {
  // 并行加载商品和分类数据
  loadProducts()
  loadCategories()
})
</script>

<template>
  <!-- 首页容器 -->
  <div class="home-page">
    <!-- Hero轮播区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1>欢迎来到红绿灯商城</h1>
        <p>发现优质商品，享受购物乐趣</p>
        <button class="hero-btn" @click="goToAllProducts">立即选购</button>
      </div>
    </section>
    
    <!-- 分类导航区域 -->
    <section class="categories-section">
      <div class="container">
        <h2 class="section-title">分类导航</h2>
        <div class="categories-grid">
          <!-- 
            遍历分类列表，生成分类按钮
            点击分类按钮跳转到对应分类的商品列表页
          -->
          <div 
            v-for="cat in categories" 
            :key="cat.id" 
            class="category-card"
            @click="goToCategory(cat.id)"
          >
            <div class="category-icon">📦</div>
            <span class="category-name">{{ cat.name }}</span>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 热销商品区域 -->
    <section class="hot-products-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">🔥 热销商品</h2>
          <button class="view-all-btn" @click="goToAllProducts">查看全部</button>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="loading">
          <p>加载中...</p>
        </div>
        
        <!-- 热销商品列表 -->
        <div v-else class="products-grid">
          <ProductCard 
            v-for="product in hotProducts" 
            :key="product.id" 
            :product="product" 
          />
        </div>
        
        <!-- 空状态 -->
        <div v-if="!loading && hotProducts.length === 0" class="empty">
          <p>暂无热销商品</p>
        </div>
      </div>
    </section>
    
    <!-- 新品上架区域 -->
    <section class="new-products-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">✨ 新品上架</h2>
          <button class="view-all-btn" @click="goToAllProducts">查看全部</button>
        </div>
        
        <!-- 新品列表 -->
        <div class="products-grid">
          <ProductCard 
            v-for="product in newProducts" 
            :key="product.id" 
            :product="product" 
          />
        </div>
        
        <!-- 空状态 -->
        <div v-if="!loading && newProducts.length === 0" class="empty">
          <p>暂无新品</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/**
 * 首页样式
 * 使用深色主题设计，配合紫色渐变风格
 */

/* 页面容器 */
.home-page {
  min-height: 100vh;
  background: #0a0a1a;
}

/* Hero轮播区域 */
.hero-section {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 5rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* Hero背景装饰 */
.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(139,92,246,0.1) 0%, transparent 50%);
  animation: pulse 8s ease-in-out infinite;
}

/* 脉冲动画 */
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

/* Hero内容 */
.hero-content {
  position: relative;
  z-index: 1;
}

/* Hero标题 */
.hero-content h1 {
  font-size: 3rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 1rem;
}

/* Hero描述 */
.hero-content p {
  font-size: 1.2rem;
  color: rgba(255,255,255,0.6);
  margin-bottom: 2rem;
}

/* Hero按钮 */
.hero-btn {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform .3s, box-shadow .3s;
}

/* Hero按钮悬停效果 */
.hero-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
}

/* 分类导航区域 */
.categories-section {
  padding: 3rem 0;
  background: rgba(255,255,255,0.02);
}

/* 内容容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* 区域标题 */
.section-title {
  font-size: 1.5rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 1.5rem;
}

/* 分类网格 */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
}

/* 分类卡片 */
.category-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all .3s;
}

/* 分类卡片悬停效果 */
.category-card:hover {
  background: rgba(139, 92, 246, 0.1);
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-3px);
}

/* 分类图标 */
.category-icon {
  font-size: 2.5rem;
  margin-bottom: .5rem;
}

/* 分类名称 */
.category-name {
  font-size: .95rem;
  color: rgba(255,255,255,0.7);
}

/* 热销和新品区域 */
.hot-products-section, .new-products-section {
  padding: 3rem 0;
}

/* 区域头部 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

/* 查看全部按钮 */
.view-all-btn {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.6);
  padding: .5rem 1.5rem;
  border-radius: 20px;
  font-size: .9rem;
  cursor: pointer;
  transition: all .3s;
}

/* 查看全部按钮悬停效果 */
.view-all-btn:hover {
  border-color: #8b5cf6;
  color: #a78bfa;
}

/* 加载状态 */
.loading {
  text-align: center;
  padding: 3rem;
  color: rgba(255,255,255,0.5);
}

/* 空状态 */
.empty {
  text-align: center;
  padding: 2rem;
  color: rgba(255,255,255,0.3);
}

/* 商品网格 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

/* 响应式布局 */
@media (max-width: 768px) {
  /* Hero标题 */
  .hero-content h1 {
    font-size: 2rem;
  }
  
  /* Hero描述 */
  .hero-content p {
    font-size: 1rem;
  }
  
  /* 分类网格 */
  .categories-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
  
  /* 商品网格 */
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
}
</style>