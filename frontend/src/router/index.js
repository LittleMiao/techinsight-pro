import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AnalystView from '../views/AnalystView.vue'
import StockDetail from '../views/StockDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/analysts',
    name: 'AnalystView',
    component: AnalystView
  },
  {
    path: '/stock/:symbol',
    name: 'StockDetail',
    component: StockDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
