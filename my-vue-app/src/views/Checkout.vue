<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { fetchAddresses, addAddress, createOrder } from '../api/index.js'
import { cartStore } from '../stores/cart.js'

const router = useRouter()
const loading = ref(false)
const addresses = ref([])
const selectedAddressId = ref(null)
const showAddAddress = ref(false)
const addressForm = ref({
  consignee: '',
  phone: '',
  province: '',
  city: '',
  district: '',
  detail: '',
  is_default: false
})
const orderRemark = ref('')
const cartItems = ref([])

const totalPrice = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
})

const loadAddresses = async () => {
  loading.value = true
  const result = await fetchAddresses()
  if (result.success) {
    addresses.value = result.data
    if (addresses.value.length > 0) {
      const defaultAddr = addresses.value.find(a => a.is_default === 1)
      selectedAddressId.value = defaultAddr ? defaultAddr.id : addresses.value[0].id
    }
  }
  loading.value = false
}

const loadCartItems = () => {
  cartItems.value = cartStore.items.map(item => ({
    product_id: item.id,
    product_name: item.name,
    price: item.price,
    quantity: item.quantity,
    main_image: item.main_image
  }))
}

onMounted(() => {
  loadAddresses()
  loadCartItems()
  if (cartItems.value.length === 0) {
    alert('购物车为空')
    router.push('/cart')
  }
})

const submitAddress = async () => {
  const required = ['consignee', 'phone', 'province', 'city', 'detail']
  for (const field of required) {
    if (!addressForm.value[field]) {
      alert(`${field}不能为空`)
      return
    }
  }
  
  const result = await addAddress(addressForm.value)
  if (result.success) {
    alert('添加地址成功')
    showAddAddress.value = false
    addressForm.value = {
      consignee: '',
      phone: '',
      province: '',
      city: '',
      district: '',
      detail: '',
      is_default: false
    }
    loadAddresses()
  } else {
    alert(result.message)
  }
}

const handleSubmitOrder = async () => {
  if (!selectedAddressId.value) {
    alert('请选择收货地址')
    return
  }
  
  loading.value = true
  const items = cartItems.value.map(item => ({
    product_id: item.product_id,
    quantity: item.quantity
  }))
  
  const result = await createOrder({
    address_id: selectedAddressId.value,
    items,
    remark: orderRemark.value
  })
  
  loading.value = false
  
  if (result.success) {
    alert(`下单成功！订单号：${result.order_id}`)
    cartStore.clearCart()
    router.push('/orders')
  } else {
    alert(result.message)
  }
}
</script>

<template>
  <div class="checkout-page">
    <div class="container">
      <h1 class="page-title">结算</h1>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else class="checkout-content">
        <div class="checkout-left">
          <div class="section">
            <h2>收货地址</h2>
            <div v-if="addresses.length === 0" class="no-address">
              <p>暂无收货地址，请添加</p>
            </div>
            <div v-else class="address-list">
              <div 
                v-for="addr in addresses" 
                :key="addr.id"
                :class="['address-item', { selected: selectedAddressId === addr.id }]"
                @click="selectedAddressId = addr.id"
              >
                <div class="address-radio">
                  <span v-if="selectedAddressId === addr.id" class="checked">✓</span>
                </div>
                <div class="address-info">
                  <div class="address-header">
                    <span class="consignee">{{ addr.consignee }}</span>
                    <span class="phone">{{ addr.phone }}</span>
                    <span v-if="addr.is_default === 1" class="default-tag">默认</span>
                  </div>
                  <p class="address-detail">
                    {{ addr.province }} {{ addr.city }} {{ addr.district }} {{ addr.detail }}
                  </p>
                </div>
              </div>
            </div>
            <button class="btn-add-address" @click="showAddAddress = !showAddAddress">
              {{ showAddAddress ? '收起' : '添加收货地址' }}
            </button>
            
            <div v-if="showAddAddress" class="add-address-form">
              <div class="form-row">
                <div class="form-group">
                  <label>收货人</label>
                  <input v-model="addressForm.consignee" placeholder="请输入收货人姓名" />
                </div>
                <div class="form-group">
                  <label>手机号</label>
                  <input v-model="addressForm.phone" placeholder="请输入手机号" />
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>省</label>
                  <input v-model="addressForm.province" placeholder="省" />
                </div>
                <div class="form-group">
                  <label>市</label>
                  <input v-model="addressForm.city" placeholder="市" />
                </div>
                <div class="form-group">
                  <label>区</label>
                  <input v-model="addressForm.district" placeholder="区（选填）" />
                </div>
              </div>
              <div class="form-group">
                <label>详细地址</label>
                <textarea v-model="addressForm.detail" placeholder="请输入详细地址"></textarea>
              </div>
              <div class="form-check">
                <input type="checkbox" v-model="addressForm.is_default" />
                <label>设为默认地址</label>
              </div>
              <button class="btn-submit-address" @click="submitAddress">保存地址</button>
            </div>
          </div>
          
          <div class="section">
            <h2>订单备注</h2>
            <textarea v-model="orderRemark" placeholder="请输入订单备注（选填）"></textarea>
          </div>
        </div>
        
        <div class="checkout-right">
          <div class="order-summary">
            <h2>订单摘要</h2>
            <div class="summary-items">
              <div v-for="(item, i) in cartItems" :key="i" class="summary-item">
                <img :src="item.main_image || 'https://via.placeholder.com/60x60?text=Image'" :alt="item.product_name" />
                <div class="summary-info">
                  <span class="summary-name">{{ item.product_name }}</span>
                  <span class="summary-price">¥{{ item.price }} × {{ item.quantity }}</span>
                </div>
              </div>
            </div>
            <div class="summary-total">
              <span>商品总价</span>
              <span>¥{{ totalPrice.toFixed(2) }}</span>
            </div>
            <div class="summary-total">
              <span>运费</span>
              <span>¥0.00</span>
            </div>
            <div class="summary-final">
              <span>实付金额</span>
              <span>¥{{ totalPrice.toFixed(2) }}</span>
            </div>
            <button class="btn-submit-order" @click="handleSubmitOrder">提交订单</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.checkout-page { min-height: 100vh; background: #0a0a1a; padding: 2rem 0; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 1rem; }
.page-title { font-size: 1.8rem; margin-bottom: 2rem; color: #fff; }
.loading { text-align: center; padding: 4rem; }
.spinner { width: 40px; height: 40px; border: 4px solid rgba(255,255,255,0.1); border-top-color: #8b5cf6; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.checkout-content { display: flex; gap: 2rem; }
.checkout-left { flex: 1; }
.checkout-right { width: 380px; flex-shrink: 0; }

.section { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; }
.section h2 { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-bottom: 1rem; }

.no-address { color: rgba(255,255,255,0.4); text-align: center; padding: 2rem; }

.address-list { display: flex; flex-direction: column; gap: .75rem; }
.address-item { display: flex; gap: 1rem; padding: 1rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; cursor: pointer; transition: all .2s; }
.address-item:hover { background: rgba(255,255,255,0.05); }
.address-item.selected { border-color: #8b5cf6; background: rgba(139, 92, 246, 0.1); }
.address-radio { width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.address-item.selected .address-radio { border-color: #8b5cf6; background: #8b5cf6; }
.checked { color: #fff; font-size: .75rem; }
.address-info { flex: 1; min-width: 0; }
.address-header { display: flex; align-items: center; gap: 1rem; margin-bottom: .25rem; }
.consignee { color: rgba(255,255,255,0.85); font-weight: 500; }
.phone { color: rgba(255,255,255,0.5); font-size: .9rem; }
.default-tag { background: #8b5cf6; color: #fff; font-size: .7rem; padding: .15rem .5rem; border-radius: 4px; }
.address-detail { color: rgba(255,255,255,0.5); font-size: .9rem; margin: 0; }

.btn-add-address { width: 100%; margin-top: 1rem; padding: .75rem; background: transparent; border: 1px dashed rgba(255,255,255,0.2); color: rgba(255,255,255,0.5); border-radius: 8px; cursor: pointer; transition: all .2s; }
.btn-add-address:hover { border-color: #8b5cf6; color: #8b5cf6; }

.add-address-form { margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.06); }
.form-row { display: flex; gap: 1rem; }
.form-group { flex: 1; display: flex; flex-direction: column; gap: .25rem; }
.form-group label { color: rgba(255,255,255,0.5); font-size: .85rem; }
.form-group input, .form-group textarea { width: 100%; padding: .65rem; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #fff; font-size: .9rem; box-sizing: border-box; }
.form-group textarea { resize: vertical; min-height: 60px; }
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: #8b5cf6; }
.form-check { display: flex; align-items: center; gap: .5rem; margin: .5rem 0; }
.form-check label { color: rgba(255,255,255,0.5); font-size: .85rem; }
.btn-submit-address { width: 100%; margin-top: 1rem; padding: .75rem; background: linear-gradient(135deg, #8b5cf6, #3b82f6); color: #fff; border: none; border-radius: 8px; cursor: pointer; font-weight: 500; }

.section textarea { width: 100%; padding: .75rem; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #fff; font-size: .9rem; resize: vertical; min-height: 80px; box-sizing: border-box; }
.section textarea:focus { outline: none; border-color: #8b5cf6; }

.order-summary { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 1.5rem; position: sticky; top: 2rem; }
.order-summary h2 { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-bottom: 1rem; }
.summary-items { max-height: 300px; overflow-y: auto; margin-bottom: 1rem; }
.summary-item { display: flex; gap: .75rem; padding: .5rem 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.summary-item:last-child { border-bottom: none; }
.summary-item img { width: 50px; height: 50px; object-fit: cover; border-radius: 8px; }
.summary-info { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: .25rem; }
.summary-name { color: rgba(255,255,255,0.7); font-size: .85rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.summary-price { color: rgba(255,255,255,0.4); font-size: .8rem; }
.summary-total { display: flex; justify-content: space-between; padding: .5rem 0; color: rgba(255,255,255,0.5); font-size: .9rem; }
.summary-final { display: flex; justify-content: space-between; padding: .75rem 0; border-top: 1px solid rgba(255,255,255,0.1); margin-top: .5rem; }
.summary-final span:first-child { color: rgba(255,255,255,0.7); font-size: 1rem; }
.summary-final span:last-child { color: #f87171; font-size: 1.5rem; font-weight: bold; }
.btn-submit-order { width: 100%; margin-top: 1rem; padding: .85rem; background: linear-gradient(135deg, #22c55e, #16a34a); color: #fff; border: none; border-radius: 10px; cursor: pointer; font-size: 1rem; font-weight: 500; transition: transform .2s, box-shadow .2s; }
.btn-submit-order:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4); }

@media (max-width: 768px) {
  .checkout-content { flex-direction: column; }
  .checkout-right { width: 100%; }
  .form-row { flex-direction: column; }
}
</style>