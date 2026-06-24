// 模拟商品数据
export const mockProducts = [
  { id: 1, name: 'iPhone 15 Pro', description: '强大的专业能力，钛金属设计', price: 7999, originalPrice: 8999, category: 'phone', image: 'https://via.placeholder.com/300x300/667eea/ffffff?text=iPhone+15', sales: 12580, rating: 4.9, stock: 99 },
  { id: 2, name: 'MacBook Pro M3', description: 'M3芯片，专业级性能', price: 14999, originalPrice: 16999, category: 'computer', image: 'https://via.placeholder.com/300x300/764ba2/ffffff?text=MacBook', sales: 8920, rating: 4.8, stock: 50 },
  { id: 3, name: 'AirPods Pro 2', description: '主动降噪，空间音频', price: 1899, originalPrice: 1999, category: 'audio', image: 'https://via.placeholder.com/300x300/ff6b6b/ffffff?text=AirPods', sales: 25680, rating: 4.7, stock: 200 },
  { id: 4, name: 'iPad Air', description: '轻薄便携，创作利器', price: 4799, originalPrice: 5299, category: 'computer', image: 'https://via.placeholder.com/300x300/4ecdc4/ffffff?text=iPad', sales: 15420, rating: 4.8, stock: 80 },
  { id: 5, name: 'Apple Watch S9', description: '健康监测，智能助手', price: 2999, originalPrice: 3299, category: 'watch', image: 'https://via.placeholder.com/300x300/45b7d1/ffffff?text=Watch', sales: 9870, rating: 4.6, stock: 120 },
  { id: 6, name: 'Sony WH-1000XM5', description: '顶级降噪，沉浸音质', price: 2499, originalPrice: 2999, category: 'audio', image: 'https://via.placeholder.com/300x300/96ceb4/ffffff?text=Sony', sales: 6540, rating: 4.9, stock: 60 },
  { id: 7, name: 'Nintendo Switch OLED', description: '随时随地，畅玩游戏', price: 2349, originalPrice: 2599, category: 'game', image: 'https://via.placeholder.com/300x300/ffeaa7/333333?text=Switch', sales: 18760, rating: 4.8, stock: 150 },
  { id: 8, name: 'Dyson V15', description: '强劲吸力，智能清洁', price: 4990, originalPrice: 5690, category: 'home', image: 'https://via.placeholder.com/300x300/dda0dd/ffffff?text=Dyson', sales: 7890, rating: 4.7, stock: 40 },
  { id: 9, name: 'Samsung Galaxy S24', description: 'AI手机，智能体验', price: 5999, originalPrice: 6999, category: 'phone', image: 'https://via.placeholder.com/300x300/74b9ff/ffffff?text=Samsung', sales: 10230, rating: 4.7, stock: 100 },
  { id: 10, name: 'ThinkPad X1 Carbon', description: '商务旗舰，轻薄本', price: 12999, originalPrice: 14999, category: 'computer', image: 'https://via.placeholder.com/300x300/a29bfe/ffffff?text=ThinkPad', sales: 5680, rating: 4.6, stock: 30 },
  { id: 11, name: 'Bose QC Ultra', description: '沉浸式音频体验', price: 2999, originalPrice: 3499, category: 'audio', image: 'https://via.placeholder.com/300x300/fd79a8/ffffff?text=Bose', sales: 4320, rating: 4.8, stock: 70 },
  { id: 12, name: 'PS5 Slim', description: '次世代游戏主机', price: 3499, originalPrice: 3899, category: 'game', image: 'https://via.placeholder.com/300x300/00b894/ffffff?text=PS5', sales: 22150, rating: 4.9, stock: 90 }
]

export const getProducts = () => {
  return mockProducts
}

export const getProductById = (id) => {
  return mockProducts.find(p => p.id === parseInt(id))
}

export const getCategories = () => {
  return [
    { id: 'all', name: '全部' },
    { id: 'phone', name: '手机' },
    { id: 'computer', name: '电脑' },
    { id: 'audio', name: '音频' },
    { id: 'watch', name: '手表' },
    { id: 'game', name: '游戏' },
    { id: 'home', name: '家电' }
  ]
}
