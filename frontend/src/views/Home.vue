<template>
  <div class="home">
    <div class="page-header">
      <h1 class="page-title">TechInsight Pro</h1>
      <p class="page-subtitle">科技板块股票深度研究平台</p>
    </div>

    <div class="quick-actions">
      <div class="action-card" @click="$router.push('/analysts')">
        <el-icon size="32" color="#1e40af"><UserFilled /></el-icon>
        <div class="action-title">分析师视角</div>
        <div class="action-desc">用博主框架模拟分析股票</div>
      </div>
    </div>

    <div class="card">
      <h3 class="card-title">热门股票</h3>
      <div class="stock-grid">
        <div 
          v-for="stock in stocks" 
          :key="stock.symbol" 
          class="stock-item"
          @click="$router.push(`/stock/${stock.symbol}`)"
        >
          <div class="stock-name">{{ stock.name }}</div>
          <div class="stock-symbol">{{ stock.symbol }}</div>
          <div class="stock-price" :class="stock.change_percent >= 0 ? 'up' : 'down'">
            ¥{{ stock.price?.toFixed(2) }}
            <span>{{ stock.change_percent >= 0 ? '+' : '' }}{{ stock.change_percent?.toFixed(2) }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { stockApi } from '../api'

const stocks = ref([])

onMounted(async () => {
  const res = await stockApi.getStocks({ page_size: 10 })
  if (res.code === 200) {
    stocks.value = res.data.list
  }
})
</script>

<style scoped>
.home { max-width: 1200px; margin: 0 auto; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 28px; font-weight: 700; color: #1e293b; margin: 0; }
.page-subtitle { color: #64748b; margin-top: 8px; }

.quick-actions { display: flex; gap: 20px; margin-bottom: 24px; }
.action-card {
  flex: 1;
  background: white;
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}
.action-title { font-size: 18px; font-weight: 600; margin-top: 12px; color: #1e293b; }
.action-desc { font-size: 14px; color: #64748b; margin-top: 4px; }

.stock-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.stock-item {
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.stock-item:hover { background: #f1f5f9; }
.stock-name { font-weight: 600; color: #1e293b; }
.stock-symbol { font-size: 12px; color: #94a3b8; margin-top: 4px; }
.stock-price { font-size: 18px; font-weight: 700; margin-top: 8px; }
</style>
