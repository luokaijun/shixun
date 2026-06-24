<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userStore } from '../stores/user'

const router = useRouter()
const formData = ref({ username: '', password: '' })
const error = ref('')
const loading = ref(false)
const particles = ref([])

onMounted(() => {
  for (let i = 0; i < 30; i++) {
    particles.value.push({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 2,
      duration: Math.random() * 20 + 15,
      delay: Math.random() * 10,
      opacity: Math.random() * 0.5 + 0.1
    })
  }
})

const handleLogin = async () => {
  error.value = ''
  if (!formData.value.username || !formData.value.password) {
    error.value = '请填写用户名和密码'
    return
  }
  loading.value = true
  try {
    const result = await userStore.login(formData.value)
    if (result.success) {
      const redirect = localStorage.getItem('redirect') || '/'
      localStorage.removeItem('redirect')
      router.push(redirect)
    } else {
      error.value = result.message || '登录失败'
    }
  } catch {
    error.value = '登录失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <!-- 粒子动画背景 -->
    <div class="particles">
      <span
        v-for="p in particles"
        :key="p.id"
        class="particle"
        :style="{
          left: p.x + '%',
          top: p.y + '%',
          width: p.size + 'px',
          height: p.size + 'px',
          animationDuration: p.duration + 's',
          animationDelay: p.delay + 's',
          opacity: p.opacity
        }"
      />
    </div>

    <!-- 光晕背景 -->
    <div class="glow glow-1" />
    <div class="glow glow-2" />
    <div class="glow glow-3" />

    <!-- 电商装饰元素 -->
    <div class="floating-shapes">
      <span class="shape shape-1">🛍️</span>
      <span class="shape shape-2">🏷️</span>
      <span class="shape shape-3">📦</span>
      <span class="shape shape-4">💎</span>
      <span class="shape shape-5">🛒</span>
      <span class="shape shape-6">⭐</span>
    </div>

    <!-- 玻璃拟态卡片 -->
    <div class="login-card">
      <div class="card-header">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </div>
        <h1>欢迎回来</h1>
        <p class="subtitle">登录您的账户继续购物</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            用户名
          </label>
          <div class="input-wrapper">
            <input
              v-model="formData.username"
              type="text"
              placeholder="请输入用户名"
              class="input"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
            密码
          </label>
          <div class="input-wrapper">
            <input
              v-model="formData.password"
              type="password"
              placeholder="请输入密码"
              class="input"
              required
            />
          </div>
        </div>

        <Transition name="shake">
          <div v-if="error" class="error-msg">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-icon">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            {{ error }}
          </div>
        </Transition>

        <button type="submit" :disabled="loading" class="btn-login">
          <span v-if="loading" class="spinner" />
          <span>{{ loading ? '登录中...' : '登 录' }}</span>
        </button>
      </form>

      <p class="footer-link">
        还没有账户？<router-link to="/register">立即注册</router-link>
      </p>

      <div class="demo-info">
        <p class="demo-title">演示账号</p>
        <div class="demo-accounts">
          <span class="demo-tag">admin / 123456</span>
          <span class="demo-tag">test / 123456</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(135deg, rgba(15, 12, 41, 0.85) 0%, rgba(48, 43, 99, 0.85) 30%, rgba(36, 36, 62, 0.85) 60%, rgba(15, 12, 41, 0.9) 100%),
    url('https://images.unsplash.com/photo-1607082349566-187342175e2f?w=1200&q=80') center/cover no-repeat;
  background-attachment: fixed;
}

/* 粒子动画 */
.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.particle {
  position: absolute;
  background: rgba(139, 92, 246, 0.4);
  border-radius: 50%;
  animation: float linear infinite;
}
@keyframes float {
  0% { transform: translateY(0) translateX(0) scale(1); }
  25% { transform: translateY(-30px) translateX(20px) scale(1.5); }
  50% { transform: translateY(-60px) translateX(-10px) scale(1); }
  75% { transform: translateY(-30px) translateX(-20px) scale(0.5); }
  100% { transform: translateY(0) translateX(0) scale(1); }
}

/* 光晕 */
.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
}
.glow-1 {
  width: 500px; height: 500px;
  background: rgba(139, 92, 246, 0.15);
  top: -200px; left: -100px;
  animation: pulse 8s ease-in-out infinite;
}
.glow-2 {
  width: 400px; height: 400px;
  background: rgba(59, 130, 246, 0.12);
  bottom: -150px; right: -100px;
  animation: pulse 6s ease-in-out infinite reverse;
}
.glow-3 {
  width: 350px; height: 350px;
  background: rgba(236, 72, 153, 0.1);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 10s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.3); opacity: 0.8; }
}
.glow-3 { animation: pulseCenter 10s ease-in-out infinite; }
@keyframes pulseCenter {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.4; }
  50% { transform: translate(-50%, -50%) scale(1.4); opacity: 0.7; }
}

/* 电商浮动装饰 */
.floating-shapes { position: absolute; inset: 0; pointer-events: none; }
.shape {
  position: absolute;
  font-size: 2rem;
  opacity: 0.15;
  animation: shapeFloat linear infinite;
}
.shape-1 { top: 10%; left: 5%; animation-duration: 18s; font-size: 2.5rem; }
.shape-2 { top: 20%; right: 8%; animation-duration: 22s; animation-delay: 2s; font-size: 2rem; }
.shape-3 { bottom: 25%; left: 10%; animation-duration: 20s; animation-delay: 5s; font-size: 3rem; }
.shape-4 { top: 60%; right: 5%; animation-duration: 16s; animation-delay: 3s; font-size: 2rem; }
.shape-5 { bottom: 15%; right: 15%; animation-duration: 24s; animation-delay: 7s; font-size: 2.8rem; }
.shape-6 { top: 40%; left: 15%; animation-duration: 19s; animation-delay: 1s; font-size: 1.8rem; }
@keyframes shapeFloat {
  0% { transform: translateY(0) rotate(0deg); }
  33% { transform: translateY(-30px) rotate(10deg); }
  66% { transform: translateY(15px) rotate(-5deg); }
  100% { transform: translateY(0) rotate(0deg); }
}

/* 玻璃拟态卡片 */
.login-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 2.5rem 2rem;
  width: 100%;
  max-width: 420px;
  position: relative;
  z-index: 1;
  animation: cardIn 0.6s ease-out;
}
@keyframes cardIn {
  from { opacity: 0; transform: translateY(30px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.card-header { text-align: center; margin-bottom: 2rem; }
.logo-icon {
  width: 56px; height: 56px;
  margin: 0 auto 1rem;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.logo-icon svg { width: 28px; height: 28px; }
h1 {
  font-size: 1.6rem;
  color: #fff;
  margin-bottom: .5rem;
  font-weight: 700;
}
.subtitle { color: rgba(255,255,255,0.5); font-size: .9rem; }

.form-group { margin-bottom: 1.25rem; }
label {
  display: flex;
  align-items: center;
  gap: .4rem;
  font-size: .85rem;
  color: rgba(255,255,255,0.7);
  font-weight: 500;
  margin-bottom: .5rem;
}
.label-icon { width: 16px; height: 16px; opacity: 0.6; }

.input-wrapper {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  transition: all 0.3s;
}
.input-wrapper:focus-within {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
  background: rgba(255, 255, 255, 0.06);
}
.input {
  width: 100%;
  padding: .875rem 1rem;
  background: transparent;
  border: none;
  color: #fff;
  font-size: .95rem;
  outline: none;
  box-sizing: border-box;
}
.input::placeholder { color: rgba(255,255,255,0.25); }

/* 错误消息 */
.error-msg {
  display: flex;
  align-items: center;
  gap: .5rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  padding: .75rem 1rem;
  border-radius: 10px;
  font-size: .85rem;
  margin-bottom: 1rem;
}
.error-icon { width: 18px; height: 18px; flex-shrink: 0; }
.shake-enter-active { animation: shake 0.4s ease; }
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-8px); }
  40% { transform: translateX(8px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}

/* 按钮 */
.btn-login {
  width: 100%;
  padding: .95rem;
  margin-top: .5rem;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}
.btn-login::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  opacity: 0;
  transition: opacity 0.3s;
}
.btn-login:hover:not(:disabled)::before { opacity: 1; }
.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
}
.btn-login:active:not(:disabled) { transform: translateY(0); }
.btn-login:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-login span { position: relative; z-index: 1; }

.spinner {
  width: 20px; height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.footer-link {
  text-align: center;
  margin-top: 1.5rem;
  color: rgba(255,255,255,0.5);
  font-size: .9rem;
}
.footer-link a {
  color: #8b5cf6;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}
.footer-link a:hover { color: #a78bfa; }

.demo-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  text-align: center;
}
.demo-title {
  color: rgba(255,255,255,0.4);
  font-size: .75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: .5rem;
}
.demo-accounts { display: flex; gap: .5rem; justify-content: center; flex-wrap: wrap; }
.demo-tag {
  background: rgba(139, 92, 246, 0.15);
  color: rgba(255,255,255,0.7);
  padding: .35rem .75rem;
  border-radius: 20px;
  font-size: .8rem;
  font-family: 'SF Mono', 'Cascadia Code', monospace;
}
</style>