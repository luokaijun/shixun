<script setup>
import { ref } from 'vue'

const orders = ref([
  {
    id: 'ORD20240115001', status: 'completed', statusText: '已完成',
    createdAt: '2024-01-15 14:30',
    items: [
      { name: 'iPhone 15 Pro', price: 7999, quantity: 1, image: 'https://via.placeholder.com/100x100?text=iPhone' },
      { name: 'AirPods Pro 2', price: 1899, quantity: 1, image: 'https://via.placeholder.com/100x100?text=AirPods' }
    ],
    total: 9898
  },
  {
    id: 'ORD20240110002', status: 'shipped', statusText: '已发货',
    createdAt: '2024-01-10 09:15',
    items: [
      { name: 'MacBook Pro M3', price: 14999, quantity: 1, image: 'https://via.placeholder.com/100x100?text=MacBook' }
    ],
    total: 14999
  },
  {
    id: 'ORD20240105003', status: 'pending', statusText: '待付款',
    createdAt: '2024-01-05 20:45',
    items: [
      { name: 'Sony WH-1000XM5', price: 2499, quantity: 1, image: 'https://via.placeholder.com/100x100?text=Sony' },
      { name: 'Apple Watch S9', price: 2999, quantity: 1, image: 'https://via.placeholder.com/100x100?text=Watch' },
      { name: 'iPad Air', price: 4799, quantity: 1, image: 'https://via.placeholder.com/100x100?text=iPad' }
    ],
    total: 10297
  }
])

const statusColor = { completed: '#2ed573', shipped: '#3498db', pending: '#ffa502' }

const cancelOrder = (id) => {
  if (confirm('确定取消此订单？')) {
    orders.value = orders.value.filter(o => o.id !== id)
    alert('订单已取消')
  }
}
</script>

<template>
  <div class="orders-page">
    <div class="container">
      <h1 class="page-title">我的订单</h1>

      <div v-if="orders.length === 0" class="empty">
        <div class="empty-icon">📦</div>
        <p>暂无订单</p>
        <router-link to="/products" class="btn-primary">去购物 →</router-link>
      </div>

      <div v-else class="orders-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <div class="order-info">
              <span class="order-id">订单号：{{ order.id }}</span>
              <span class="order-date">{{ order.createdAt }}</span>
            </div>
            <span :style="{ color: statusColor[order.status] || '#666' }" class="order-status">{{ order.statusText }}</span>
          </div>

          <div class="order-items">
            <div v-for="(item, i) in order.items" :key="i" class="order-item">
              <img :src="item.image" :alt="item.name" />
              <div class="item-info">
                <span class="item-name">{{ item.name }}</span>
                <span class="item-price">¥{{ item.price }} × {{ item.quantity }}</span>
              </div>
            </div>
          </div>

          <div class="order-footer">
            <div class="order-total">合计：<span class="total-amount">¥{{ order.total }}</span></div>
            <div class="order-actions">
              <button v-if="order.status === 'pending'" class="btn btn-cancel" @click="cancelOrder(order.id)">取消订单</button>
              <button v-if="order.status === 'pending'" class="btn btn-pay">立即付款</button>
              <button v-if="order.status === 'shipped'" class="btn btn-receive">确认收货</button>
              <button v-if="order.status === 'completed'" class="btn btn-review">评价</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.orders-page { min-height: 100vh; background: #0a0a1a; padding: 2rem 0; }
.container { max-width: 800px; margin: 0 auto; padding: 0 1rem; }
.page-title { font-size: 1.8rem; margin-bottom: 2rem; color: #fff; }
.empty { text-align: center; padding: 4rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; }
.empty-icon { font-size: 4rem; margin-bottom: 1rem; }
.empty p { color: rgba(255,255,255,0.5); font-size: 1.1rem; margin-bottom: 1.5rem; }
.btn-primary { display: inline-block; background: linear-gradient(135deg, #8b5cf6, #3b82f6); color: #fff; padding: .75rem 2rem; border-radius: 25px; text-decoration: none; font-weight: 500; transition: transform .2s, box-shadow .2s; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4); }
.orders-list { display: flex; flex-direction: column; gap: 1.5rem; }
.order-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; overflow: hidden; }
.order-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; background: rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.04); }
.order-info { display: flex; flex-direction: column; gap: .25rem; }
.order-id { font-size: .95rem; color: rgba(255,255,255,0.85); font-weight: 500; }
.order-date { font-size: .85rem; color: rgba(255,255,255,0.4); }
.order-status { font-size: .9rem; font-weight: 500; }
.order-items { padding: .5rem 1.5rem; }
.order-item { display: flex; gap: 1rem; padding: .75rem 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.order-item:last-child { border-bottom: none; }
.order-item img { width: 60px; height: 60px; object-fit: cover; border-radius: 10px; }
.item-info { display: flex; flex-direction: column; justify-content: center; gap: .25rem; }
.item-name { font-size: .95rem; color: rgba(255,255,255,0.85); }
.item-price { font-size: .85rem; color: rgba(255,255,255,0.4); }
.order-footer { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-top: 1px solid rgba(255,255,255,0.04); }
.order-total { font-size: .95rem; color: rgba(255,255,255,0.5); }
.total-amount { font-size: 1.25rem; font-weight: bold; color: #f87171; margin-left: .5rem; }
.order-actions { display: flex; gap: .75rem; }
.btn { padding: .5rem 1.25rem; border: none; border-radius: 8px; font-size: .85rem; cursor: pointer; transition: transform .2s, box-shadow .2s; }
.btn:hover { transform: translateY(-1px); }
.btn-cancel { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.08); }
.btn-cancel:hover { background: rgba(239, 68, 68, 0.1); color: #fca5a5; }
.btn-pay { background: linear-gradient(135deg, #8b5cf6, #3b82f6); color: #fff; }
.btn-pay:hover { box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); }
.btn-receive { background: linear-gradient(135deg, #22c55e, #16a34a); color: #fff; }
.btn-receive:hover { box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4); }
.btn-review { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; }
.btn-review:hover { box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); }
@media (max-width: 768px) {
  .order-header { flex-direction: column; gap: .75rem; align-items: flex-start; }
  .order-footer { flex-direction: column; gap: 1rem; align-items: stretch; }
  .order-actions { justify-content: stretch; }
  .btn { flex: 1; text-align: center; }
}
</style>