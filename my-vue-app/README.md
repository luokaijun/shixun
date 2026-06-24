<<<<<<< HEAD
# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).
=======
# shixun
>>>>>>> 2729f77565123ee24377f94a58b9ef3adb6d78b6


文件里的联系
┌─────────────────────────────────────────────────────────────────┐
│                        前端Vue应用                              │
├─────────────────────────────────────────────────────────────────┤
│  main.js ──────────── 入口文件                                  │
│     │                                                          │
│     ├── router/index.js ─── 路由配置（导航守卫、页面映射）       │
│     │         │                                                │
│     │         ├── Home.vue          ─── 首页                   │
│     │         ├── Products.vue      ─── 商品列表               │
│     │         ├── ProductDetail.vue ─── 商品详情               │
│     │         ├── Cart.vue          ─── 购物车                 │
│     │         ├── Login.vue         ─── 登录                   │
│     │         ├── Register.vue      ─── 注册                   │
│     │         └── Orders.vue        ─── 订单                   │
│     │                                                          │
│     ├── stores/ ──────── 状态管理                              │
│     │     ├── cart.js    ─── 购物车数据（增删改查、本地存储）   │
│     │     └── user.js    ─── 用户数据（登录、注册、状态）       │
│     │                                                          │
│     ├── components/ ──── 公共组件                              │
│     │     ├── Navbar.vue ─── 导航栏（路由链接、购物车数量）     │
│     │     └── ProductCard.vue ─── 商品卡片（复用组件）         │
│     │                                                          │
│     └── api/index.js ──── API调用（封装所有后端接口）           │
│                 │                                              │
│                 ▼                                              │
│           后端Flask API (http://localhost:5000/api)            │
└─────────────────────────────────────────────────────────────────┘