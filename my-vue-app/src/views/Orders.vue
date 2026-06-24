<script setup>import { ref, onMounted } from 'vue';
import { fetchOrders, submitReview, payOrder, receiveOrder, cancelOrder as cancelOrderApi } from '../api/index.js';
const orders = ref([]);
const loading = ref(false);
const reviewModal = ref(false);
const currentItem = ref(null);
const currentOrder = ref(null);
const reviewForm = ref({
 rating: 5,
 content: '',
 is_anonymous: false
});
const statusColor = {
 pending: '#ffa502',
 paid: '#f59e0b',
 shipped: '#3498db',
 completed: '#2ed573',
 canceled: '#666'
};
const loadOrders = async () => {
 loading.value = true;
 const result = await fetchOrders();
 if (result.success) {
 orders.value = result.data;
 }
 loading.value = false;
};
onMounted(() => {
 loadOrders();
});
const cancelOrder = async (id) => {
 if (!confirm('确定取消此订单？'))
 return;
 const result = await cancelOrderApi(id);
 if (result.success) {
 alert('订单已取消');
 loadOrders();
 } else {
 alert(result.message);
 }
};
const handlePayOrder = async (orderId) => {
 if (!confirm('确定付款？')) return;
 const result = await payOrder(orderId);
 if (result.success) {
 alert('付款成功');
 loadOrders();
 } else {
 alert(result.message);
 }
};
const handleReceiveOrder = async (orderId) => {
 if (!confirm('确认已收到商品？')) return;
 const result = await receiveOrder(orderId);
 if (result.success) {
 alert('确认收货成功');
 loadOrders();
 } else {
 alert(result.message);
 }
};
const openReviewModal = (order, item) => {
 currentOrder.value = order;
 currentItem.value = item;
 reviewForm.value = {
 rating: 5,
 content: '',
 is_anonymous: false
 };
 reviewModal.value = true;
};
const closeReviewModal = () => {
 reviewModal.value = false;
 currentItem.value = null;
 currentOrder.value = null;
};
const submitReviewHandler = async () => {
 if (!reviewForm.value.rating) {
 alert('请选择评分');
 return;
 }
 const result = await submitReview({
 product_id: currentItem.value.product_id,
 rating: reviewForm.value.rating,
 content: reviewForm.value.content,
 order_id: currentOrder.value.id,
 is_anonymous: reviewForm.value.is_anonymous ? 1 : 0
 });
 if (result.success) {
 alert('评价成功！');
 closeReviewModal();
 loadOrders();
 }
 else {
 alert(result.message);
 }
};
const hasUnreviewedItems = (order) => {
 return order.items.some(item => !item.reviewed);
};
const formatRating = (rating) => {
 return '★'.repeat(rating) + '☆'.repeat(5 - rating);
};

const openFirstUnreviewed = (order) => {
 const item = order.items.find(i => !i.reviewed);
 if (item) {
 openReviewModal(order, item);
 }
};
</script>

<template>
  <div class="orders-page">
    <div class="container">
      <h1 class="page-title">我的订单</h1>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="orders.length === 0" class="empty">
        <div class="empty-icon">📦</div>
        <p>暂无订单</p>
        <router-link to="/products" class="btn-primary">去购物 →</router-link>
      </div>

      <div v-else class="orders-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <div class="order-info">
              <span class="order-id">订单号：{{ order.id }}</span>
              <span class="order-date">{{ order.create_time }}</span>
            </div>
            <span :style="{ color: statusColor[order.status] || '#666' }" class="order-status">{{ order.status_text }}</span>
          </div>

          <div class="order-items">
            <div v-for="(item, i) in order.items" :key="item.id || i" class="order-item">
              <img :src="item.product_image || 'https://via.placeholder.com/100x100?text=No+Image'" :alt="item.product_name" />
              <div class="item-info">
                <span class="item-name">{{ item.product_name }}</span>
                <span class="item-price">¥{{ item.price }} × {{ item.quantity }}</span>
              </div>
              <div v-if="order.status === 'completed' && !item.reviewed" class="item-review">
                <button class="btn btn-review-item" @click="openReviewModal(order, item)">评价</button>
              </div>
              <div v-else-if="item.reviewed" class="item-reviewed">
                <span>已评价</span>
              </div>
            </div>
          </div>

          <div class="order-footer">
            <div class="order-total">合计：<span class="total-amount">¥{{ order.total_amount }}</span></div>
            <div class="order-actions">
              <button v-if="order.status === 'pending'" class="btn btn-cancel" @click="cancelOrder(order.id)">取消订单</button>
              <button v-if="order.status === 'pending'" class="btn btn-pay" @click="handlePayOrder(order.id)">立即付款</button>
              <button v-if="order.status === 'shipped'" class="btn btn-receive" @click="handleReceiveOrder(order.id)">确认收货</button>
              <button v-if="order.status === 'completed' && hasUnreviewedItems(order)" class="btn btn-review-all" @click="openFirstUnreviewed(order)">去评价</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="reviewModal" class="modal-overlay" @click.self="closeReviewModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>评价商品</h3>
          <button class="modal-close" @click="closeReviewModal">×</button>
        </div>
        <div class="modal-body">
          <div v-if="currentItem" class="review-product">
            <img :src="currentItem.product_image || 'https://via.placeholder.com/100x100?text=No+Image'" :alt="currentItem.product_name" />
            <span>{{ currentItem.product_name }}</span>
          </div>
          
          <div class="review-form">
            <div class="form-group">
              <label>评分</label>
              <div class="rating-stars">
                <span 
                  v-for="i in 5" 
                  :key="i" 
                  :class="{ active: reviewForm.rating >= i }"
                  @click="reviewForm.rating = i"
                >★</span>
                <span class="rating-text">{{ reviewForm.rating }}分</span>
              </div>
            </div>
            
            <div class="form-group">
              <label>评价内容</label>
              <textarea 
                v-model="reviewForm.content" 
                placeholder="请输入您的评价..." 
                rows="4"
              ></textarea>
            </div>
            
            <div class="form-group form-check">
              <input type="checkbox" v-model="reviewForm.is_anonymous" />
              <label>匿名评价</label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-cancel" @click="closeReviewModal">取消</button>
          <button class="btn btn-submit" @click="submitReviewHandler">提交评价</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.orders-page { min-height: 100vh; background: #0a0a1a; padding: 2rem 0; }
.container { max-width: 800px; margin: 0 auto; padding: 0 1rem; }
.page-title { font-size: 1.8rem; margin-bottom: 2rem; color: #fff; }
.loading { text-align: center; padding: 4rem; }
.spinner { width: 40px; height: 40px; border: 4px solid rgba(255,255,255,0.1); border-top-color: #8b5cf6; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
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
.order-item { display: flex; gap: 1rem; padding: .75rem 0; border-bottom: 1px solid rgba(255,255,255,0.04); align-items: center; }
.order-item:last-child { border-bottom: none; }
.order-item img { width: 60px; height: 60px; object-fit: cover; border-radius: 10px; }
.item-info { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: .25rem; }
.item-name { font-size: .95rem; color: rgba(255,255,255,0.85); }
.item-price { font-size: .85rem; color: rgba(255,255,255,0.4); }
.item-review { margin-left: auto; }
.btn-review-item { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; padding: .35rem .85rem; border: none; border-radius: 6px; font-size: .8rem; cursor: pointer; transition: transform .2s, box-shadow .2s; }
.btn-review-item:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); }
.item-reviewed { margin-left: auto; color: rgba(255,255,255,0.3); font-size: .8rem; }
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
.btn-review-all { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; }
.btn-review-all:hover { box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); }
.btn-submit { background: linear-gradient(135deg, #22c55e, #16a34a); color: #fff; }
.btn-submit:hover { box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4); }

.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: #1a1a2e; border-radius: 16px; width: 90%; max-width: 480px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
.modal-header h3 { color: #fff; margin: 0; font-size: 1.1rem; }
.modal-close { background: none; border: none; color: rgba(255,255,255,0.5); font-size: 1.5rem; cursor: pointer; padding: 0; line-height: 1; }
.modal-body { padding: 1.5rem; }
.review-product { display: flex; gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
.review-product img { width: 80px; height: 80px; object-fit: cover; border-radius: 10px; }
.review-product span { display: flex; align-items: center; color: rgba(255,255,255,0.85); font-size: .95rem; }
.review-form { display: flex; flex-direction: column; gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: .5rem; }
.form-group label { color: rgba(255,255,255,0.6); font-size: .9rem; }
.rating-stars { display: flex; align-items: center; gap: .5rem; }
.rating-stars span { font-size: 1.5rem; cursor: pointer; transition: color .2s; }
.rating-stars span:not(.rating-text) { color: rgba(255,255,255,0.2); }
.rating-stars span.active { color: #fbbf24; }
.rating-text { font-size: 1rem !important; color: rgba(255,255,255,0.6) !important; cursor: default !important; }
.form-group textarea { width: 100%; padding: .75rem; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #fff; font-size: .9rem; resize: vertical; box-sizing: border-box; }
.form-group textarea::placeholder { color: rgba(255,255,255,0.3); }
.form-group textarea:focus { outline: none; border-color: #8b5cf6; }
.form-check { flex-direction: row !important; align-items: center; gap: .5rem; }
.form-check input { width: 18px; height: 18px; }
.modal-footer { display: flex; gap: .75rem; padding: 1rem 1.5rem; border-top: 1px solid rgba(255,255,255,0.1); justify-content: flex-end; }
@media (max-width: 768px) {
  .order-header { flex-direction: column; gap: .75rem; align-items: flex-start; }
  .order-footer { flex-direction: column; gap: 1rem; align-items: stretch; }
  .order-actions { justify-content: stretch; }
  .btn { flex: 1; text-align: center; }
  .order-item { flex-wrap: wrap; }
  .item-review { width: 100%; margin-left: 0; margin-top: .5rem; }
  .btn-review-item { width: 100%; }
}
</style>