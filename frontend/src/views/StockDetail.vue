<template>
  <div class="stock-detail" v-if="stock">
    <div class="stock-header">
      <div class="stock-basic">
        <h1 class="stock-name">{{ stock.name }}</h1>
        <span class="stock-symbol">{{ stock.symbol }}</span>
        <span class="stock-sector">{{ stock.sector }} · {{ stock.sub_sector }}</span>
      </div>
      <div class="stock-price" :class="stock.change_percent >= 0 ? 'up' : 'down'">
        <div class="current-price">¥{{ stock.price?.toFixed(2) }}</div>
        <div class="price-change">{{ stock.change_percent >= 0 ? '+' : '' }}{{ stock.change_percent?.toFixed(2) }}%</div>
      </div>
    </div>

    <div class="card">
      <h3 class="card-title">关键指标</h3>
      <div class="metrics-grid">
        <div class="metric-item">
          <span class="metric-label">PE</span>
          <span class="metric-value">{{ stock.pe_ttm?.toFixed(2) || '-' }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">PB</span>
          <span class="metric-value">{{ stock.pb?.toFixed(2) || '-' }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">ROE</span>
          <span class="metric-value">{{ stock.roe?.toFixed(2) || '-' }}%</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">营收增长</span>
          <span class="metric-value">{{ stock.revenue_growth?.toFixed(2) || '-' }}%</span>
        </div>
      </div>
    </div>

    <div class="card">
      <h3 class="card-title">博主观点</h3>
      <div class="views-list" v-if="analystViews.length">
        <div v-for="view in analystViews" :key="view.analyst_id" class="view-item">
          <div class="view-analyst">{{ view.analyst_name }}</div>
          <div class="view-judgment" :class="view.judgment">{{ viewText(view.judgment) }}</div>
          <div class="view-confidence">置信度: {{ view.confidence }}%</div>
        </div>
      </div>
      <div v-else class="no-views">暂无博主分析数据</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { stockApi, analystApi } from '../api'

const route = useRoute()
const symbol = route.params.symbol
const stock = ref(null)
const analystViews = ref([])

const viewText = (j) => ({ buy: '看多', sell: '看空', hold: '中性' }[j] || '中性')

onMounted(async () => {
  const [stockRes, viewsRes] = await Promise.all([
    stockApi.getStockDetail(symbol),
    analystApi.getStockViews(symbol)
  ])
  if (stockRes.code === 200) stock.value = stockRes.data
  if (viewsRes.code === 200) analystViews.value = viewsRes.data.views
})
</script>

<style scoped>
.stock-detail { max-width: 1200px; margin: 0 auto; }
.stock-header { display: flex; justify-content: space-between; align-items: center; background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; }
.stock-name { font-size: 28px; font-weight: 700; margin: 0; }
.stock-symbol { font-size: 14px; color: #64748b; margin-left: 12px; }
.stock-sector { font-size: 14px; color: #94a3b8; margin-left: 12px; }
.current-price { font-size: 36px; font-weight: 700; }
.price-change { font-size: 16px; margin-top: 4px; }
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.metric-item { text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px; }
.metric-label { display: block; font-size: 12px; color: #94a3b8; margin-bottom: 4px; }
.metric-value { font-size: 20px; font-weight: 600; color: #1e293b; }
.views-list { display: flex; flex-direction: column; gap: 12px; }
.view-item { display: flex; align-items: center; gap: 16px; padding: 12px; background: #f8fafc; border-radius: 8px; }
.view-analyst { font-weight: 600; flex: 1; }
.view-judgment { padding: 4px 12px; border-radius: 4px; font-size: 14px; font-weight: 600; }
.view-judgment.buy { background: #dcfce7; color: #166534; }
.view-judgment.sell { background: #fee2e2; color: #991b1b; }
.view-judgment.hold { background: #fef9c3; color: #854d0e; }
.view-confidence { font-size: 12px; color: #64748b; }
.no-views { text-align: center; color: #94a3b8; padding: 24px; }
</style>
