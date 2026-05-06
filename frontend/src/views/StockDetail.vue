<template>
  <div class="stock-detail-page" v-loading="loading">
    <div v-if="stockInfo" class="detail-content">
      <!-- 股票基本信息 -->
      <div class="stock-header">
        <div class="stock-basic">
          <h1 class="stock-name">{{ stockInfo.name }}</h1>
          <span class="stock-code">{{ stockInfo.code }}</span>
          <el-tag :type="stockInfo.change >= 0 ? 'danger' : 'success'" size="large">
            {{ stockInfo.sector }}
          </el-tag>
        </div>
        <div class="stock-price-info">
          <div class="current-price">
            <span class="price-label">现价</span>
            <span class="price-value">¥{{ stockInfo.price?.toFixed(2) }}</span>
          </div>
          <div :class="['price-change', stockInfo.change >= 0 ? 'up' : 'down']">
            <span>{{ stockInfo.change >= 0 ? '+' : '' }}{{ stockInfo.change?.toFixed(2) }}%</span>
          </div>
        </div>
      </div>

      <!-- 四大指标模块 -->
      <div class="metrics-container">
        <!-- 估值指标 -->
        <div class="metric-section valuation">
          <div class="section-header">
            <div class="section-icon">
              <el-icon><Coin /></el-icon>
            </div>
            <h2 class="section-title">估值指标</h2>
          </div>
          <div class="metric-cards">
            <div class="metric-card" v-for="item in valuationMetrics" :key="item.name">
              <div class="metric-label">{{ item.name }}</div>
              <div class="metric-value">{{ item.value }}</div>
              <div class="metric-desc">{{ item.description }}</div>
            </div>
          </div>
        </div>

        <!-- 盈利能力 -->
        <div class="metric-section profitability">
          <div class="section-header">
            <div class="section-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <h2 class="section-title">盈利能力</h2>
          </div>
          <div class="metric-cards">
            <div class="metric-card" v-for="item in profitabilityMetrics" :key="item.name">
              <div class="metric-label">{{ item.name }}</div>
              <div class="metric-value">{{ item.value }}</div>
              <div class="metric-desc">{{ item.description }}</div>
            </div>
          </div>
        </div>

        <!-- 成长性 -->
        <div class="metric-section growth">
          <div class="section-header">
            <div class="section-icon">
              <el-icon><DataLine /></el-icon>
            </div>
            <h2 class="section-title">成长性</h2>
          </div>
          <div class="metric-cards">
            <div class="metric-card" v-for="item in growthMetrics" :key="item.name">
              <div class="metric-label">{{ item.name }}</div>
              <div class="metric-value">{{ item.value }}</div>
              <div class="metric-desc">{{ item.description }}</div>
            </div>
          </div>
        </div>

        <!-- 健康度 -->
        <div class="metric-section health">
          <div class="section-header">
            <div class="section-icon">
              <el-icon><FirstAidKit /></el-icon>
            </div>
            <h2 class="section-title">健康度</h2>
          </div>
          <div class="metric-cards">
            <div class="metric-card" v-for="item in healthMetrics" :key="item.name">
              <div class="metric-label">{{ item.name }}</div>
              <div class="metric-value">{{ item.value }}</div>
              <div class="metric-desc">{{ item.description }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 综合评分 -->
      <div class="overall-rating">
        <div class="rating-header">
          <h3>综合评分</h3>
          <div class="rating-score">
            <span class="score-value">{{ overallScore }}</span>
            <span class="score-max">/100</span>
          </div>
        </div>
        <el-progress
          :percentage="overallScore"
          :color="getScoreColor(overallScore)"
          :stroke-width="12"
          striped
          striped-flow
        />
        <div class="rating-detail">
          <div class="rating-item">
            <span class="label">估值评分</span>
            <span class="value">{{ valuationScore }}</span>
          </div>
          <div class="rating-item">
            <span class="label">盈利评分</span>
            <span class="value">{{ profitabilityScore }}</span>
          </div>
          <div class="rating-item">
            <span class="label">成长评分</span>
            <span class="value">{{ growthScore }}</span>
          </div>
          <div class="rating-item">
            <span class="label">健康评分</span>
            <span class="value">{{ healthScore }}</span>
          </div>
        </div>
      </div>
    </div>

    <el-empty v-else description="暂无数据" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Coin, TrendCharts, DataLine, FirstAidKit } from '@element-plus/icons-vue'
import { stockApi } from '../api'

const route = useRoute()
const loading = ref(false)
const stockInfo = ref(null)

// 估值指标
const valuationMetrics = ref([
  { name: '市盈率 (PE)', value: '28.5', description: '低于行业平均' },
  { name: '市净率 (PB)', value: '5.2', description: '处于中等水平' },
  { name: '市销率 (PS)', value: '8.3', description: '略有高估' },
  { name: '企业价值倍数', value: '18.6', description: '估值合理' },
  { name: 'PEG', value: '0.85', description: '具有成长性' }
])

// 盈利能力指标
const profitabilityMetrics = ref([
  { name: '毛利率', value: '68.5%', description: '优秀的盈利能力' },
  { name: '净利率', value: '35.2%', description: '处于行业中上' },
  { name: 'ROE', value: '22.5%', description: '股东回报优秀' },
  { name: 'ROA', value: '12.8%', description: '资产利用高效' },
  { name: '每股收益', value: '¥18.50', description: '每股盈利能力强' }
])

// 成长性指标
const growthMetrics = ref([
  { name: '营收增长率', value: '15.8%', description: '保持稳健增长' },
  { name: '净利润增长率', value: '22.3%', description: '利润增速较快' },
  { name: '3年复合增长率', value: '18.5%', description: '持续稳定增长' },
  { name: '季度环比增长', value: '5.2%', description: '近期表现良好' },
  { name: '研发投入占比', value: '8.5%', description: '持续高研发投入' }
])

// 健康度指标
const healthMetrics = ref([
  { name: '资产负债率', value: '35.2%', description: '财务结构稳健' },
  { name: '流动比率', value: '2.5', description: '短期偿债能力强' },
  { name: '速动比率', value: '2.1', description: '流动性充足' },
  { name: '现金流负债比', value: '0.85', description: '现金流状况良好' },
  { name: '应收账款周转', value: '8.5次', description: '回款效率较高' }
])

// 评分
const overallScore = ref(78)
const valuationScore = ref(72)
const profitabilityScore = ref(88)
const growthScore = ref(75)
const healthScore = ref(82)

const getScoreColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}

const fetchStockDetail = async () => {
  loading.value = true
  try {
    const code = route.params.code
    const response = await stockApi.getStockDetail(code)
    stockInfo.value = response.data
  } catch (error) {
    console.error('获取股票详情失败:', error)
    // 使用模拟数据
    stockInfo.value = {
      code: route.params.code || '600519',
      name: '模拟股票',
      sector: '科技',
      price: 128.50,
      change: 2.35,
      pe: 28.5,
      pb: 5.2
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStockDetail()
})
</script>

<style scoped>
.stock-detail-page {
  padding: 0;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 股票头部 */
.stock-header {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.stock-basic {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stock-name {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.stock-code {
  font-size: 16px;
  color: #909399;
  background: #f5f7fa;
  padding: 4px 12px;
  border-radius: 4px;
}

.stock-price-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.current-price {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.price-label {
  font-size: 14px;
  color: #909399;
}

.price-value {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  font-family: 'Monaco', 'Menlo', monospace;
}

.price-change {
  padding: 6px 16px;
  border-radius: 6px;
  font-size: 18px;
  font-weight: 600;
}

.price-change.up {
  background: #fef0f0;
  color: #f56c6c;
}

.price-change.down {
  background: #f0f9eb;
  color: #67c23a;
}

/* 指标容器 */
.metrics-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

/* 指标区块 */
.metric-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

.section-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.valuation .section-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.profitability .section-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.growth .section-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.health .section-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.metric-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.metric-card {
  background: #f9fafb;
  border-radius: 8px;
  padding: 14px;
  transition: all 0.2s;
}

.metric-card:hover {
  background: #f0f2f5;
  transform: translateY(-2px);
}

.metric-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 4px;
  font-family: 'Monaco', 'Menlo', monospace;
}

.metric-desc {
  font-size: 12px;
  color: #67c23a;
}

/* 综合评分 */
.overall-rating {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.rating-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.rating-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.rating-score {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.score-value {
  font-size: 36px;
  font-weight: 700;
  color: #409eff;
}

.score-max {
  font-size: 16px;
  color: #909399;
}

.rating-detail {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.rating-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.rating-item .label {
  font-size: 13px;
  color: #909399;
}

.rating-item .value {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

@media (max-width: 768px) {
  .metrics-container {
    grid-template-columns: 1fr;
  }

  .metric-cards {
    grid-template-columns: 1fr;
  }

  .stock-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>
