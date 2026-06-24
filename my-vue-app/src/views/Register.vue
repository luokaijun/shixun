<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userStore } from '../stores/user'

const router = useRouter()
const form = ref({ username: '', email: '', password: '', confirmPassword: '' })
const error = ref('')
const success = ref('')
const loading = ref(false)
const particles = ref([])

onMounted(() => {
  for (let i = 0; i < 30; i++) {
    particles.value.push({
      id: i, x: Math.random() * 100, y: Math.random() * 100,
      size: Math.random() * 4 + 2, duration: Math.random() * 20 + 15,
      delay: Math.random() * 10, opacity: Math.random() * 0.5 + 0.1
    })
  }
})

const handleRegister = async () => {
  error.value = ''
  success.value = ''
  if (!form.value.username) { error.value = '请输入用户名'; return }
  if (!form.value.email) { error.value = '请输入邮箱'; return }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) { error.value = '邮箱格式不正确'; return }
  if (!form.value.password) { error.value = '请输入密码'; return }
  if (form.value.password.length < 6) { error.value = '密码至少6位'; return }
  if (form.value.password !== form.value.confirmPassword) { error.value = '两次密码不一致'; return }
  loading.value = true
  try {
    const result = await userStore.register(form.value)
    if (result.success) {
      success.value = '注册成功！即将跳转...'
      setTimeout(() => router.push('/login'), 1500)
    } else {
      error.value = result.message || '注册失败'
    }
  } catch {
    error.value = '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <div class="particles">
      <span v-for="p in particles" :key="p.id" class="particle"
        :style="{ left: p.x + '%', top: p.y + '%', width: p.size + 'px', height: p.size + 'px', animationDuration: p.duration + 's', animationDelay: p.delay + 's', opacity: p.opacity }" />
    </div>
    <div class="glow glow-1" />
    <div class="glow glow-2" />
    <div class="glow glow-3" />

    <div class="register-card">
      <div class="card-header">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="8.5" cy="7" r="4" />
            <polyline points="17 11 19 13 23 9" />
          </svg>
        </div>
        <h1>创建账户</h1>
        <p class="subtitle">加入我们，开始购物之旅</p>
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名</label>
          <div class="input-wrapper">
            <input v-model="form.username" type="text" placeholder="请输入用户名" class="input" />
          </div>
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <div class="input-wrapper">
            <input v-model="form.email" type="email" placeholder="请输入邮箱" class="input" />
          </div>
        </div>
        <div class="form-group">
          <label>密码</label>
          <div class="input-wrapper">
            <input v-model="form.password" type="password" placeholder="至少6位" class="input" />
          </div>
        </div>
        <div class="form-group">
          <label>确认密码</label>
          <div class="input-wrapper">
            <input v-model="form.confirmPassword" type="password" placeholder="再次输入密码" class="input" />
          </div>
        </div>

        <Transition name="shake">
          <div v-if="error" class="error-msg">{{ error }}</div>
        </Transition>
        <Transition name="fade">
          <div v-if="success" class="success-msg">{{ success }}</div>
        </Transition>

        <button type="submit" :disabled="loading" class="btn-register">
          <span v-if="loading" class="spinner" />
          <span>{{ loading ? '注册中...' : '注 册' }}</span>
        </button>
      </form>

      <p class="footer-link">已有账户？<router-link to="/login">立即登录</router-link></p>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center; padding: 1rem;
  position: relative; overflow: hidden;
  background:
    linear-gradient(135deg, rgba(15, 12, 41, 0.85) 0%, rgba(48, 43, 99, 0.85) 30%, rgba(36, 36, 62, 0.85) 60%, rgba(15, 12, 41, 0.9) 100%),
    url('https://images.unsplash.com/photo-1607082349566-187342175e2f?w=1200&q=80') center/cover no-repeat;
}
.particles { position: absolute; inset: 0; pointer-events: none; }
.particle { position: absolute; background: rgba(139, 92, 246, 0.4); border-radius: 50%; animation: float linear infinite; }
@keyframes float {
  0% { transform: translateY(0) translateX(0) scale(1); }
  25% { transform: translateY(-30px) translateX(20px) scale(1.5); }
  50% { transform: translateY(-60px) translateX(-10px) scale(1); }
  75% { transform: translateY(-30px) translateX(-20px) scale(0.5); }
  100% { transform: translateY(0) translateX(0) scale(1); }
}
.glow { position: absolute; border-radius: 50%; filter: blur(120px); pointer-events: none; }
.glow-1 { width: 500px; height: 500px; background: rgba(139, 92, 246, 0.15); top: -200px; left: -100px; animation: pulse 8s ease-in-out infinite; }
.glow-2 { width: 400px; height: 400px; background: rgba(59, 130, 246, 0.12); bottom: -150px; right: -100px; animation: pulse 6s ease-in-out infinite reverse; }
.glow-3 { width: 350px; height: 350px; background: rgba(236, 72, 153, 0.1); top: 50%; left: 50%; animation: pulseCenter 10s ease-in-out infinite; }
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.3); opacity: 0.8; }
}
@keyframes pulseCenter {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.4; }
  50% { transform: translate(-50%, -50%) scale(1.4); opacity: 0.7; }
}
.register-card {
  background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px;
  padding: 2.5rem 2rem; width: 100%; max-width: 450px; position: relative; z-index: 1;
  animation: cardIn 0.6s ease-out;
}
@keyframes cardIn { from { opacity: 0; transform: translateY(30px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
.card-header { text-align: center; margin-bottom: 2rem; }
.logo-icon { width: 56px; height: 56px; margin: 0 auto 1rem; background: linear-gradient(135deg, #8b5cf6, #3b82f6); border-radius: 16px; display: flex; align-items: center; justify-content: center; color: #fff; }
.logo-icon svg { width: 28px; height: 28px; }
h1 { font-size: 1.6rem; color: #fff; margin-bottom: .5rem; font-weight: 700; }
.subtitle { color: rgba(255,255,255,0.5); font-size: .9rem; }
.form-group { margin-bottom: 1rem; }
label { display: flex; align-items: center; gap: .4rem; font-size: .85rem; color: rgba(255,255,255,0.7); font-weight: 500; margin-bottom: .5rem; }
.input-wrapper { background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; transition: all 0.3s; }
.input-wrapper:focus-within { border-color: #8b5cf6; box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15); background: rgba(255, 255, 255, 0.06); }
.input { width: 100%; padding: .875rem 1rem; background: transparent; border: none; color: #fff; font-size: .95rem; outline: none; box-sizing: border-box; }
.input::placeholder { color: rgba(255,255,255,0.25); }
.error-msg { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); color: #fca5a5; padding: .75rem 1rem; border-radius: 10px; font-size: .85rem; margin-bottom: .75rem; }
.success-msg { background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); color: #86efac; padding: .75rem 1rem; border-radius: 10px; font-size: .85rem; margin-bottom: .75rem; }
.shake-enter-active { animation: shake 0.4s ease; }
.fade-enter-active { transition: opacity 0.3s; }
.fade-enter-from { opacity: 0; }
@keyframes shake {
  0%, 100% { transform: translateX(0); } 20% { transform: translateX(-8px); }
  40% { transform: translateX(8px); } 60% { transform: translateX(-4px); } 80% { transform: translateX(4px); }
}
.btn-register {
  width: 100%; padding: .95rem; margin-top: .25rem;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6); border: none; border-radius: 12px;
  color: #fff; font-size: 1rem; font-weight: 600; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: .5rem;
  transition: all 0.3s; position: relative; overflow: hidden;
}
.btn-register::before { content: ''; position: absolute; inset: 0; background: linear-gradient(135deg, #a78bfa, #60a5fa); opacity: 0; transition: opacity 0.3s; }
.btn-register:hover:not(:disabled)::before { opacity: 1; }
.btn-register:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4); }
.btn-register:active:not(:disabled) { transform: translateY(0); }
.btn-register:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-register span { position: relative; z-index: 1; }
.spinner { width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.footer-link { text-align: center; margin-top: 1.5rem; color: rgba(255,255,255,0.5); font-size: .9rem; }
.footer-link a { color: #8b5cf6; text-decoration: none; font-weight: 600; transition: color 0.3s; }
.footer-link a:hover { color: #a78bfa; }
</style>