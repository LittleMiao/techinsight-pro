import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import StockDetail from './views/StockDetail.vue'
import Analyst from './views/Analyst.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/stock/:code',
    name: 'StockDetail',
    component: StockDetail
  },
  {
    path: '/analyst',
    name: 'Analyst',
    component: Analyst
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
