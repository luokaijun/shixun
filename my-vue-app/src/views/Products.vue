<script setup>
/**
 * Products.vue - 商品列表页面
 * 
 * 【页面用途】
 * 展示所有商品的列表，支持搜索、分类筛选、排序功能
 * 是用户浏览和查找商品的主要页面
 * 
 * 【页面关系】
 * - 路由路径：/products
 * - 引用 ProductCard.vue 组件展示商品卡片
 * - 通过 API 模块（api/index.js）从后端获取商品和分类数据
 * - 数据流向：后端API → fetchProducts/fetchCategories → products/categories → ProductCard组件
 * - 后端API不可用时，自动切换到本地mock数据作为备用方案
 * 
 * 【功能说明】
 * 1. 搜索功能：根据商品名称或描述搜索
 * 2. 分类筛选：按商品分类筛选
 * 3. 排序功能：支持价格升序/降序、销量优先、评分优先
 * 4. 商品展示：使用卡片形式展示商品列表
 * 5. 数据备用：后端API失败时自动使用本地mock数据
 * 
 * 【API接口】
 * - GET /api/products - 获取商品列表（支持搜索、分类、排序参数）
 * - GET /api/categories - 获取分类列表
 * 
 * 【数据字段】
 * - products: 商品列表数组，每个商品包含 main_image、name、price、sales、rating 等字段
 * - categories: 分类列表数组，每个分类包含 id、name 字段
 * - searchQuery: 搜索关键词
 * - selectedCategory: 当前选中的分类ID
 * - sortBy: 当前排序方式
 * - isUsingMock: 是否正在使用mock数据（API失败时为true）
 */

// 导入Vue响应式API
import { ref, computed, onMounted } from 'vue'
// 导入后端API调用函数
import { fetchProducts, fetchCategories } from '../api/index'
// 导入商品卡片组件
import ProductCard from '../components/ProductCard.vue'
// 导入mock数据作为备用方案
import { mockProducts, getCategories } from '../data/mock'

/**
 * 响应式数据定义
 */

// 商品列表数据
const products = ref([])
// 搜索关键词
const searchQuery = ref('')
// 当前选中的分类ID
const selectedCategory = ref('')
// 当前排序方式
const sortBy = ref('')
// 分类列表数据
const categories = ref([])
// 加载状态
const loading = ref(true)
// 总商品数
const total = ref(0)
// 是否正在使用mock数据（API失败时为true）
const isUsingMock = ref(false)

/**
 * 从后端获取商品数据
 * @param {Object} params - 请求参数（搜索、分类、排序）
 * @returns {void}
 */
const loadProducts = async (params = {}) => {
  loading.value = true
  isUsingMock.value = false
  
  try {
    // 调用后端API获取商品列表
    const result = await fetchProducts(params)
    
    if (result.success && result.data && result.data.length > 0) {
      // 成功获取数据，更新商品列表和总数
      products.value = result.data
      total.value = result.total || result.data.length
      console.log('成功从后端API获取商品数据:', products.value.length, '件商品')
    } else {
      // 获取失败或数据为空，使用mock数据作为备用方案
      console.warn('后端API返回数据为空或失败，切换到本地mock数据:', result.message)
      useMockProducts()
    }
  } catch (error) {
    // 网络错误或其他异常，使用mock数据作为备用方案
    console.error('获取商品列表异常，切换到本地mock数据:', error)
    useMockProducts()
  } finally {
    // 无论成功与否，都结束加载状态
    loading.value = false
  }
}

/**
 * 使用本地mock数据作为备用方案
 * 当后端API不可用时调用此方法
 * @returns {void}
 */
const useMockProducts = () => {
  isUsingMock.value = true
  // 转换mock数据格式，添加main_image字段以适配组件
  products.value = mockProducts.map(p => ({
    ...p,
    main_image: p.image,
    category_id: getCategoryIdByName(p.category),
    brand_id: 1,
    is_on_sale: 1
  }))
  total.value = products.value.length
  console.log('已切换到本地mock数据:', products.value.length, '件商品')
}

/**
 * 根据mock数据中的分类名称获取分类ID
 * @param {string} categoryName - 分类名称（如'phone', 'computer'）
 * @returns {number} 分类ID
 */
const getCategoryIdByName = (categoryName) => {
  const categoryMap = {
    'phone': 1,
    'computer': 1,
    'audio': 1,
    'watch': 1,
    'game': 1,
    'home': 3
  }
  return categoryMap[categoryName] || 1
}

/**
 * 从后端获取分类数据
 * 如果API失败，使用本地mock数据作为备用方案
 * @returns {void}
 */
const loadCategories = async () => {
  try {
    // 调用后端API获取分类列表
    const result = await fetchCategories()
    
    if (result.success && result.data && result.data.length > 0) {
      // 成功获取数据，更新分类列表
      categories.value = result.data
      console.log('成功从后端API获取分类数据:', categories.value.length, '个分类')
    } else {
      // 获取失败或数据为空，使用mock数据作为备用方案
      console.warn('后端API返回分类数据为空或失败，切换到本地mock数据:', result.message)
      useMockCategories()
    }
  } catch (error) {
    // 网络错误或其他异常，使用mock数据作为备用方案
    console.error('获取分类列表异常，切换到本地mock数据:', error)
    useMockCategories()
  }
}

/**
 * 使用本地mock分类数据作为备用方案
 * 当后端API不可用时调用此方法
 * @returns {void}
 */
const useMockCategories = () => {
  // 获取mock分类数据并转换格式（移除'all'选项，只保留实际分类）
  const mockCats = getCategories().filter(c => c.id !== 'all')
  categories.value = mockCats.map(c => ({
    ...c,
    id: parseInt(c.id) || getCategoryIdByName(c.id)
  }))
  console.log('已切换到本地mock分类数据:', categories.value.length, '个分类')
}

/**
 * 计算属性：过滤后的商品列表
 * 根据搜索关键词、分类、排序方式对商品进行筛选和排序
 */
const filteredProducts = computed(() => {
  // 开始时使用原始商品列表
  let result = [...products.value]
  
  // 搜索过滤：根据商品名称或描述匹配搜索关键词
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(p => 
      (p.name && p.name.toLowerCase().includes(query)) ||
      (p.description && p.description.toLowerCase().includes(query))
    )
  }
  
  // 分类过滤：根据选中的分类ID筛选
  if (selectedCategory.value) {
    result = result.filter(p => p.category_id === parseInt(selectedCategory.value))
  }
  
  // 排序：根据选中的排序方式进行排序
  switch (sortBy.value) {
    case 'price-asc':
      // 价格从低到高
      result = result.sort((a, b) => (a.price || 0) - (b.price || 0))
      break
    case 'price-desc':
      // 价格从高到低
      result = result.sort((a, b) => (b.price || 0) - (a.price || 0))
      break
    case 'sales':
      // 销量优先（从高到低）
      result = result.sort((a, b) => (b.sales || 0) - (a.sales || 0))
      break
    case 'rating':
      // 评分优先（从高到低）
      result = result.sort((a, b) => (b.rating || 0) - (a.rating || 0))
      break
  }
  
  return result
})

/**
 * 监听搜索关键词变化，重新加载商品
 */
const handleSearch = () => {
  loadProducts({
    search: searchQuery.value,
    category_id: selectedCategory.value,
    sort: sortBy.value
  })
}

/**
 * 监听分类选择变化，重新加载商品
 */
const handleCategoryChange = () => {
  loadProducts({
    search: searchQuery.value,
    category_id: selectedCategory.value,
    sort: sortBy.value
  })
}

/**
 * 监听排序方式变化，重新加载商品
 */
const handleSortChange = () => {
  loadProducts({
    search: searchQuery.value,
    category_id: selectedCategory.value,
    sort: sortBy.value
  })
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
  <!-- 商品列表页面容器 -->
  <div class="products-page">
    <div class="container">
      <!-- 筛选区域 -->
      <div class="filters">
        <!-- 搜索框 -->
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="搜索商品..." 
            class="search-input"
            @keyup.enter="handleSearch"
          />
        </div>
        
        <!-- 分类和排序 -->
        <div class="filter-group">
          <!-- 分类标签 -->
          <div class="categories">
            <!-- 全部按钮 -->
            <button 
              :class="['category-btn', { active: !selectedCategory }]"
              @click="selectedCategory = ''; handleCategoryChange()"
            >
              全部
            </button>
            <!-- 分类列表按钮 -->
            <button 
              v-for="cat in categories" 
              :key="cat.id"
              :class="['category-btn', { active: selectedCategory === cat.id.toString() }]"
              @click="selectedCategory = cat.id.toString(); handleCategoryChange()"
            >
              {{ cat.name }}
            </button>
          </div>
          
          <!-- 排序下拉框 -->
          <select v-model="sortBy" class="sort-select" @change="handleSortChange">
            <option value="">默认排序</option>
            <option value="price-asc">价格从低到高</option>
            <option value="price-desc">价格从高到低</option>
            <option value="sales">销量优先</option>
            <option value="rating">评分优先</option>
          </select>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="filteredProducts.length === 0" class="empty">
        <p>没有找到相关商品</p>
      </div>
      
      <!-- 商品网格 -->
      <div v-else class="products-grid">
        <ProductCard 
          v-for="product in filteredProducts" 
          :key="product.id" 
          :product="product" 
        />
      </div>
      
      <!-- 结果统计 -->
      <div class="results-count">
        共 {{ filteredProducts.length }} 件商品（总 {{ total }} 件）
      </div>
    </div>
  </div>
</template>

<style scoped>
/**
 * 商品列表页面样式
 * 使用深色主题设计，配合紫色渐变风格
 */

/* 页面容器 */
.products-page {
  min-height: 100vh;
  background: #0a0a1a;
  padding: 2rem 0;
}

/* 内容容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* 筛选区域 */
.filters {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  padding: 1.5rem;
  border-radius: 16px;
  margin-bottom: 2rem;
}

/* 搜索框区域 */
.search-box {
  margin-bottom: 1rem;
}

/* 搜索输入框 */
.search-input {
  width: 100%;
  padding: .75rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  font-size: 1rem;
  color: #fff;
  transition: border-color .3s;
  box-sizing: border-box;
}
/* 搜索框占位符样式 */
.search-input::placeholder { color: rgba(255,255,255,0.25); }
/* 搜索框聚焦样式 */
.search-input:focus { 
  outline: none; 
  border-color: #8b5cf6; 
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15); 
}

/* 筛选组（分类+排序） */
.filter-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

/* 分类标签容器 */
.categories {
  display: flex;
  gap: .5rem;
  flex-wrap: wrap;
}

/* 分类按钮 */
.category-btn {
  padding: .5rem 1rem;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  background: transparent;
  color: rgba(255,255,255,0.6);
  cursor: pointer;
  transition: all .3s;
  font-size: .9rem;
}
/* 分类按钮悬停效果 */
.category-btn:hover {
  border-color: #8b5cf6;
  color: #a78bfa;
}
/* 分类按钮激活状态 */
.category-btn.active {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  border-color: transparent;
  color: #fff;
}

/* 排序下拉框 */
.sort-select {
  padding: .5rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  font-size: .9rem;
  color: rgba(255,255,255,0.7);
  cursor: pointer;
}
/* 下拉框聚焦样式 */
.sort-select:focus { outline: none; border-color: #8b5cf6; }
/* 下拉框选项样式 */
.sort-select option { background: #1a1a2e; color: #fff; }

/* 加载和空状态 */
.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: rgba(255,255,255,0.5);
  font-size: 1.1rem;
}

/* 商品网格 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

/* 结果统计 */
.results-count {
  text-align: center;
  margin-top: 2rem;
  color: rgba(255,255,255,0.4);
}
</style>