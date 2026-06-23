<script setup>
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="app-container">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2024 红绿灯商城. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-container { min-height: 100vh; display: flex; flex-direction: column; background: #0a0a1a; }
.main-content { flex: 1; }
.app-footer { background: rgba(255,255,255,0.03); border-top: 1px solid rgba(255,255,255,0.06); color: rgba(255,255,255,0.4); text-align: center; padding: 1.5rem; margin-top: auto; }
.app-footer p { margin: 0; font-size: .85rem; }
</style>