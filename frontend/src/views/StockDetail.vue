<template>
  <div class="stock-detail-page" v-loading="loading">
    <div v-if="stockInfo" class="detail-content">
      <!-- 股票基本信息 -->
      <div class="stock-header">
        <div class="stock-basic">
          <h1 class="stock-name">{{ stockInfo.name }}</h1>
          <span class="stock-code">{{ stockInfo.symbol }}</span>
          <el-tag :type="stockInfo.change_percent >= 0 ? 'danger' : 'success'" size="large">
            {{ sectorMap[stockInfo.sector] || stockInfo.sector || '-' }}
          </el-tag>
          <el-tag v-if="stockInfo.is_hot" type="warning" size="small" effect="dark">热门</el-tag>
        </div>
        <div class="stock-price-info">
          <div class="current-price">
            <span class="price-label">现价</span>
            <span class="price-value">¥{{ fmt(stockInfo.price) }}</span>
          </div>
          <div class="price-extra">
            <div :class="['price-change', stockInfo.change_percent >= 0 ? 'up' : 'down']">
              {{ stockInfo.change_percent >= 0 ? '+' : '' }}{{ fmt(stockInfo.change_percent) }}%
            </div>
            <div :class="['price-amount', stockInfo.change_amount >= 0 ? 'up' : 'down']">
              {{ stockInfo.change_amount >= 0 ? '+' : '' }}{{ fmt(stockInfo.change_amount) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 行情概览 -->
      <div class="quote-bar">
        <div class="quote-item">
          <span class="quote-label">今开</span>
          <span class="quote-val">{{ fmt(stockInfo.open_price) }}</span>
        </div>
        <div class="quote-item">
          <span class="quote-label">最高</span>
          <span class="quote-val up">{{ fmt(stockInfo.high_price) }}</span>
        </div>
        <div class="quote-item">
          <span class="quote-label">最低</span>
          <span class="quote-val down">{{ fmt(stockInfo.low_price) }}</span>
        </div>
        <div class="quote-item">
          <span class="quote-label">昨收</span>
          <span class="quote-val">{{ fmt(stockInfo.prev_close) }}</span>
        </div>
        <div class="quote-item">
          <span class="quote-label">成交量</span>
          <span class="quote-val">{{ fmtVolume(stockInfo.volume) }}</span>
        </div>
        <div class="quote-item">
          <span class="quote-label">成交额</span>
          <span class="quote-val">{{ fmtTurnover(stockInfo.turnover) }}</span>
        </div>
        <div class="quote-item">
          <span class="quote-label">总市值</span>
          <span class="quote-val">{{ fmtMarketCap(stockInfo.market_cap) }}</span>
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
            <el-tag
              v-if="peRank"
              :type="peRank.type"
              size="small"
              effect="dark"
              class="rank-badge"
            >PE {{ peRank.label }}</el-tag>
          </div>
          <div class="metric-cards">
            <div class="metric-card" v-for="item in valuationMetrics" :key="item.key">
              <div class="metric-item">
                <span class="metric-label">{{ item.name }}</span>
                <span class="metric-value" :style="{ color: item.color }">{{ item.value }}</span>
                <div class="metric-compare" v-if="sectorComp && sectorComp[item.key]">
                  <span>行业均值: {{ sectorComp[item.key].sector_avg?.toFixed(1) }}</span>
                  <span class="best">龙头: {{ sectorComp[item.key].sector_best?.name }} {{ sectorComp[item.key].sector_best?.value?.toFixed(1) }}</span>
                </div>
                <div class="metric-trend" v-if="historyTrend && historyTrend[item.key]">
                  <span :class="getTrendClass(item.key, historyTrend[item.key].deviation_pct)">
                    vs 3年均值: {{ historyTrend[item.key].deviation_pct > 0 ? '+' : '' }}{{ historyTrend[item.key].deviation_pct?.toFixed(1) }}%
                  </span>
                </div>
              </div>
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
            <el-tag
              v-if="roeRank"
              :type="roeRank.type"
              size="small"
              effect="dark"
              class="rank-badge"
            >ROE {{ roeRank.label }}</el-tag>
          </div>
          <div class="metric-cards">
            <div class="metric-card" v-for="item in profitabilityMetrics" :key="item.key">
              <div class="metric-item">
                <span class="metric-label">{{ item.name }}</span>
                <span class="metric-value" :style="{ color: item.color }">{{ item.value }}</span>
                <div class="metric-compare" v-if="sectorComp && sectorComp[item.key]">
                  <span>行业均值: {{ sectorComp[item.key].sector_avg?.toFixed(1) }}</span>
                  <span class="best">龙头: {{ sectorComp[item.key].sector_best?.name }} {{ sectorComp[item.key].sector_best?.value?.toFixed(1) }}</span>
                </div>
                <div class="metric-trend" v-if="historyTrend && historyTrend[item.key]">
                  <span :class="getTrendClass(item.key, historyTrend[item.key].deviation_pct)">
                    vs 3年均值: {{ historyTrend[item.key].deviation_pct > 0 ? '+' : '' }}{{ historyTrend[item.key].deviation_pct?.toFixed(1) }}%
                  </span>
                </div>
              </div>
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
            <div class="metric-card" v-for="item in growthMetrics" :key="item.key">
              <div class="metric-item">
                <span class="metric-label">{{ item.name }}</span>
                <span class="metric-value" :style="{ color: item.color }">{{ item.value }}</span>
                <div class="metric-compare" v-if="sectorComp && sectorComp[item.key]">
                  <span>行业均值: {{ sectorComp[item.key].sector_avg?.toFixed(1) }}</span>
                  <span class="best">龙头: {{ sectorComp[item.key].sector_best?.name }} {{ sectorComp[item.key].sector_best?.value?.toFixed(1) }}</span>
                </div>
                <div class="metric-trend" v-if="historyTrend && historyTrend[item.key]">
                  <span :class="getTrendClass(item.key, historyTrend[item.key].deviation_pct)">
                    vs 3年均值: {{ historyTrend[item.key].deviation_pct > 0 ? '+' : '' }}{{ historyTrend[item.key].deviation_pct?.toFixed(1) }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 财务健康 -->
        <div class="metric-section health">
          <div class="section-header">
            <div class="section-icon">
              <el-icon><FirstAidKit /></el-icon>
            </div>
            <h2 class="section-title">财务健康</h2>
          </div>
          <div class="metric-cards">
            <div class="metric-card" v-for="item in healthMetrics" :key="item.key">
              <div class="metric-item">
                <span class="metric-label">{{ item.name }}</span>
                <span class="metric-value" :style="{ color: item.color }">{{ item.value }}</span>
                <div class="metric-compare" v-if="sectorComp && sectorComp[item.key]">
                  <span>行业均值: {{ sectorComp[item.key].sector_avg?.toFixed(1) }}</span>
                  <span class="best">龙头: {{ sectorComp[item.key].sector_best?.name }} {{ sectorComp[item.key].sector_best?.value?.toFixed(1) }}</span>
                </div>
                <div class="metric-trend" v-if="historyTrend && historyTrend[item.key]">
                  <span :class="getTrendClass(item.key, historyTrend[item.key].deviation_pct)">
                    vs 3年均值: {{ historyTrend[item.key].deviation_pct > 0 ? '+' : '' }}{{ historyTrend[item.key].deviation_pct?.toFixed(1) }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 同业对比 -->
      <div class="peer-section" v-if="peers && peers.length > 0">
        <div class="section-header">
          <div class="section-icon peer-icon">
            <el-icon><User /></el-icon>
          </div>
          <h2 class="section-title">同业对比</h2>
          <el-tag type="info" size="small" class="rank-badge">
            {{ sectorMap[stockInfo.sector] || stockInfo.sector || '' }} - {{ stockInfo.sub_sector || '' }}
          </el-tag>
        </div>
        <el-table
          :data="peers"
          style="width: 100%"
          :row-class-name="peerRowClassName"
          size="small"
          stripe
          class="peer-table"
        >
          <el-table-column prop="name" label="股票名称" min-width="120">
            <template #default="{ row }">
              <span :class="{ 'current-stock-name': row.symbol === stockInfo.symbol }">
                {{ row.name }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="pe_ttm" label="PE-TTM" width="100" align="right">
            <template #default="{ row }">
              <span :class="{ 'best-value': isBestPeerValue('pe_ttm', row.pe_ttm, true) }">
                {{ fmt(row.pe_ttm) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="roe" label="ROE(%)" width="100" align="right">
            <template #default="{ row }">
              <span :class="{ 'best-value': isBestPeerValue('roe', row.roe, false) }">
                {{ fmt(row.roe) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="gross_margin" label="毛利率(%)" width="110" align="right">
            <template #default="{ row }">
              <span :class="{ 'best-value': isBestPeerValue('gross_margin', row.gross_margin, false) }">
                {{ fmt(row.gross_margin) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="revenue_growth_3y" label="营收增速(%)" width="120" align="right">
            <template #default="{ row }">
              <span :class="{ 'best-value': isBestPeerValue('revenue_growth_3y', row.revenue_growth_3y, false) }">
                {{ fmtPct(row.revenue_growth_3y) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="debt_to_equity" label="资产负债率(%)" width="130" align="right">
            <template #default="{ row }">
              <span :class="{ 'best-value': isBestPeerValue('debt_to_equity', row.debt_to_equity, true) }">
                {{ fmt(row.debt_to_equity) }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 综合评分 -->
      <div class="overall-rating">
        <div class="rating-header">
          <h3>综合评分</h3>
          <div class="rating-score">
            <span class="score-value" :style="{ color: getScoreColor(overallScore) }">{{ overallScore }}</span>
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
            <span class="value" :style="{ color: getScoreColor(valuationScore) }">{{ valuationScore }}</span>
          </div>
          <div class="rating-item">
            <span class="label">盈利评分</span>
            <span class="value" :style="{ color: getScoreColor(profitabilityScore) }">{{ profitabilityScore }}</span>
          </div>
          <div class="rating-item">
            <span class="label">成长评分</span>
            <span class="value" :style="{ color: getScoreColor(growthScore) }">{{ growthScore }}</span>
          </div>
          <div class="rating-item">
            <span class="label">健康评分</span>
            <span class="value" :style="{ color: getScoreColor(healthScore) }">{{ healthScore }}</span>
          </div>
        </div>
      </div>

      <!-- 分析师观点 -->
      <div class="analyst-views-section" v-if="analystViews.length > 0">
        <div class="section-header">
          <div class="section-icon analyst-icon">
            <el-icon><User /></el-icon>
          </div>
          <h2 class="section-title">分析师观点</h2>
        </div>
        <div class="analyst-views-list">
          <div class="analyst-view-card" v-for="view in analystViews" :key="view.id">
            <div class="view-header">
              <div class="analyst-info">
                <el-avatar :size="36" class="analyst-avatar">{{ (view.analyst_name || '?')[0] }}</el-avatar>
                <div class="analyst-meta">
                  <span class="analyst-name">{{ view.analyst_name || '匿名分析师' }}</span>
                  <span class="view-date">{{ view.created_at || '' }}</span>
                </div>
              </div>
              <el-tag
                :type="getRatingType(view.rating)"
                size="small"
                effect="dark"
              >{{ view.rating || '-' }}</el-tag>
            </div>
            <div class="view-content">
              <p>{{ view.content || view.summary || '暂无详细观点' }}</p>
            </div>
            <div class="view-tags" v-if="view.tags && view.tags.length">
              <el-tag v-for="tag in view.tags" :key="tag" size="small" type="info" class="view-tag">{{ tag }}</el-tag>
            </div>
          </div>
        </div>
      </div>

      <!-- 报告日期 -->
      <div class="report-date" v-if="stockInfo.report_date">
        数据截止日期：{{ stockInfo.report_date }}
      </div>
    </div>

    <el-empty v-else-if="!loading" description="暂无数据" />

    <!-- 信息源浮动按钮 -->
    <div class="source-fab" @click="sourceDrawerVisible = true">
      <el-icon :size="24"><Reading /></el-icon>
    </div>

    <!-- 信息源抽屉 -->
    <el-drawer
      v-model="sourceDrawerVisible"
      title="信息源"
      direction="rtl"
      size="420px"
      :before-close="handleDrawerClose"
    >
      <el-tabs v-model="activeSourceTab" @tab-change="handleSourceTabChange">
        <el-tab-pane label="全部" name="all" />
        <el-tab-pane label="财报" name="financial_report" />
        <el-tab-pane label="研报" name="research_report" />
        <el-tab-pane label="新闻" name="news" />
        <el-tab-pane label="博主观点" name="blogger" />
      </el-tabs>
      <div class="source-list" v-loading="sourceLoading">
        <div
          class="source-card"
          v-for="item in sourceList"
          :key="item.id"
          :class="'sentiment-border-' + (item.sentiment || 'neutral')"
        >
          <div class="source-title">{{ item.title }}</div>
          <div class="source-meta">
            <span class="source-name">{{ item.source }}</span>
            <span class="source-time">{{ formatTime(item.publish_time) }}</span>
          </div>
          <div class="source-summary">{{ item.summary }}</div>
          <el-tag
            :type="getSentimentType(item.sentiment)"
            size="small"
            class="source-sentiment"
          >{{ getSentimentLabel(item.sentiment) }}</el-tag>
        </div>
        <el-empty v-if="!sourceLoading && sourceList.length === 0" description="暂无信息" />
      </div>
      <div class="source-pagination" v-if="sourceTotal > sourcePageSize">
        <el-pagination
          small
          layout="prev, pager, next"
          :total="sourceTotal"
          :page-size="sourcePageSize"
          v-model:current-page="sourcePage"
          @current-change="handleSourcePageChange"
        />
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Coin, TrendCharts, DataLine, FirstAidKit, User, Reading } from '@element-plus/icons-vue'
import { stockApi, analystApi } from '../api'

const route = useRoute()
const loading = ref(false)
const stockInfo = ref(null)
const analystViews = ref([])

// ---------- 新增响应式数据 ----------
const sectorComp = ref(null)
const peers = ref([])
const historyTrend = ref(null)
const sourceDrawerVisible = ref(false)
const sourceLoading = ref(false)
const sourceList = ref([])
const sourceTotal = ref(0)
const sourcePage = ref(1)
const sourcePageSize = ref(10)
const activeSourceTab = ref('all')

const sectorMap = {
  semiconductor: '半导体',
  ai: 'AI',
  new_energy: '新能源',
  cloud_computing: '云计算'
}

// ---------- 格式化工具 ----------

const fmt = (v) => {
  if (v === null || v === undefined) return '-'
  return Number(v).toFixed(2)
}

const fmtPct = (v) => {
  if (v === null || v === undefined) return '-'
  const prefix = v >= 0 ? '+' : ''
  return prefix + Number(v).toFixed(2) + '%'
}

const fmtVolume = (v) => {
  if (v === null || v === undefined) return '-'
  const n = Number(v)
  if (n >= 1e8) return (n / 1e8).toFixed(2) + '亿'
  if (n >= 1e4) return (n / 1e4).toFixed(2) + '万'
  return n.toString()
}

const fmtTurnover = (v) => {
  if (v === null || v === undefined) return '-'
  const n = Number(v)
  if (n >= 1e8) return (n / 1e8).toFixed(2) + '亿'
  if (n >= 1e4) return (n / 1e4).toFixed(2) + '万'
  return n.toFixed(2)
}

const fmtMarketCap = (v) => {
  if (v === null || v === undefined) return '-'
  const n = Number(v)
  if (n >= 1e12) return (n / 1e12).toFixed(2) + '万亿'
  if (n >= 1e8) return (n / 1e8).toFixed(2) + '亿'
  if (n >= 1e4) return (n / 1e4).toFixed(2) + '万'
  return n.toFixed(2)
}

const fmtPercent = (v) => {
  if (v === null || v === undefined) return '-'
  return Number(v).toFixed(2) + '%'
}

const formatTime = (isoString) => {
  if (!isoString) return '-'
  const d = new Date(isoString)
  if (isNaN(d.getTime())) return isoString
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  const hh = String(d.getHours()).padStart(2, '0')
  const mi = String(d.getMinutes()).padStart(2, '0')
  const yyyy = d.getFullYear()
  // 如果是今年则省略年份
  if (yyyy === new Date().getFullYear()) {
    return `${mm}-${dd} ${hh}:${mi}`
  }
  return `${yyyy}-${mm}-${dd}`
}

// 涨跌颜色（中国市场惯例：红涨绿跌）
const growthColor = (v) => {
  if (v === null || v === undefined) return '#909399'
  return v >= 0 ? '#f56c6c' : '#67c23a'
}

const growthValue = (v) => {
  if (v === null || v === undefined) return '-'
  const prefix = v >= 0 ? '+' : ''
  return prefix + Number(v).toFixed(2) + '%'
}

// ---------- 越低越好的指标判断 ----------

const isLowerBetter = (metricKey) => {
  const lowerSet = ['pe_ttm', 'pb', 'ps_ttm', 'ev_ebitda', 'pcf', 'debt_ratio', 'debt_to_equity']
  return lowerSet.includes(metricKey)
}

// ---------- 趋势颜色逻辑 ----------

const getTrendClass = (metricKey, deviationPct) => {
  if (deviationPct === null || deviationPct === undefined) return ''
  const lower = isLowerBetter(metricKey)
  if (lower) {
    // 越低越好：高于均值(正值)是坏的(红色)，低于均值(负值)是好的(绿色)
    return deviationPct > 0 ? 'trend-up' : 'trend-down'
  }
  // 越高越好：高于均值(正值)是好的(绿色)，低于均值(负值)是坏的(红色)
  return deviationPct > 0 ? 'trend-down' : 'trend-up'
}

// ---------- PE 评级 ----------

const peRank = computed(() => {
  const pe = stockInfo.value?.pe_ttm
  if (pe === null || pe === undefined) return null
  if (pe < 20) return { label: '低估', type: 'success' }
  if (pe < 40) return { label: '合理', type: '' }
  if (pe < 60) return { label: '偏高', type: 'warning' }
  return { label: '高估', type: 'danger' }
})

// ---------- ROE 评级 ----------

const roeRank = computed(() => {
  const roe = stockInfo.value?.roe
  if (roe === null || roe === undefined) return null
  if (roe >= 20) return { label: '优秀', type: 'success' }
  if (roe >= 15) return { label: '良好', type: '' }
  if (roe >= 10) return { label: '一般', type: 'warning' }
  return { label: '较弱', type: 'danger' }
})

// ---------- 四大指标区域（带 key） ----------

const d = computed(() => stockInfo.value || {})

const valuationMetrics = computed(() => [
  { key: 'pe_ttm', name: 'PE-TTM', value: fmt(d.value.pe_ttm), color: '#303133' },
  { key: 'pb', name: 'PB', value: fmt(d.value.pb), color: '#303133' },
  { key: 'ps_ttm', name: 'PS-TTM', value: fmt(d.value.ps_ttm), color: '#303133' },
  { key: 'ev_ebitda', name: 'EV/EBITDA', value: fmt(d.value.ev_ebitda), color: '#303133' },
  { key: 'pcf', name: 'PCF', value: fmt(d.value.pcf), color: '#303133' }
])

const profitabilityMetrics = computed(() => [
  { key: 'roe', name: 'ROE', value: fmtPercent(d.value.roe), color: growthColor(d.value.roe) },
  { key: 'roa', name: 'ROA', value: fmtPercent(d.value.roa), color: growthColor(d.value.roa) },
  { key: 'gross_margin', name: '毛利率', value: fmtPercent(d.value.gross_margin), color: growthColor(d.value.gross_margin) },
  { key: 'net_margin', name: '净利率', value: fmtPercent(d.value.net_margin), color: growthColor(d.value.net_margin) },
  { key: 'operating_margin', name: '营业利润率', value: fmtPercent(d.value.operating_margin), color: growthColor(d.value.operating_margin) }
])

const growthMetrics = computed(() => [
  { key: 'revenue_growth_3y', name: '营收增速(3年)', value: growthValue(d.value.revenue_growth_3y), color: growthColor(d.value.revenue_growth_3y) },
  { key: 'profit_growth_3y', name: '利润增速(3年)', value: growthValue(d.value.profit_growth_3y), color: growthColor(d.value.profit_growth_3y) },
  { key: 'revenue_growth_5y', name: '营收增速(5年)', value: growthValue(d.value.revenue_growth_5y), color: growthColor(d.value.revenue_growth_5y) },
  { key: 'profit_growth_5y', name: '利润增速(5年)', value: growthValue(d.value.profit_growth_5y), color: growthColor(d.value.profit_growth_5y) }
])

const healthMetrics = computed(() => [
  { key: 'current_ratio', name: '流动比率', value: fmt(d.value.current_ratio), color: '#303133' },
  { key: 'quick_ratio', name: '速动比率', value: fmt(d.value.quick_ratio), color: '#303133' },
  { key: 'debt_ratio', name: '资产负债率', value: fmtPercent(d.value.debt_ratio), color: '#303133' },
  { key: 'interest_coverage', name: '利息保障倍数', value: fmt(d.value.interest_coverage), color: '#303133' }
])

// ---------- 同业对比辅助 ----------

const peerRowClassName = ({ row }) => {
  if (row.symbol === stockInfo.value?.symbol) return 'current-peer-row'
  return ''
}

const isBestPeerValue = (field, value, lowerBetter) => {
  if (value === null || value === undefined) return false
  const list = peers.value.filter(p => p[field] !== null && p[field] !== undefined)
  if (list.length === 0) return false
  const best = lowerBetter
    ? Math.min(...list.map(p => p[field]))
    : Math.max(...list.map(p => p[field]))
  return Number(value) === Number(best)
}

// ---------- 信息源辅助 ----------

const getSentimentType = (sentiment) => {
  if (sentiment === 'positive') return 'success'
  if (sentiment === 'negative') return 'danger'
  return 'info'
}

const getSentimentLabel = (sentiment) => {
  if (sentiment === 'positive') return '正面'
  if (sentiment === 'negative') return '负面'
  return '中性'
}

const handleDrawerClose = (done) => {
  done()
}

const handleSourceTabChange = (tab) => {
  sourcePage.value = 1
  fetchSources(tab)
}

const handleSourcePageChange = (page) => {
  fetchSources(activeSourceTab.value, page)
}

const fetchSources = async (sourceType, page) => {
  sourceLoading.value = true
  try {
    const symbol = route.params.symbol
    const params = {
      page: page || sourcePage.value,
      page_size: sourcePageSize.value
    }
    if (sourceType && sourceType !== 'all') {
      params.source_type = sourceType
    }
    const res = await stockApi.getSources(symbol, params)
    if (res.code === 200 && res.data) {
      sourceList.value = res.data.list || []
      sourceTotal.value = res.data.total || 0
    }
  } catch (error) {
    console.error('获取信息源失败:', error)
    sourceList.value = []
    sourceTotal.value = 0
  } finally {
    sourceLoading.value = false
  }
}

// ---------- 评分算法 ----------

/**
 * 每个维度满分 25，总分 100
 * 估值：PE 越低越好；PB、PS、EV/EBITDA、PCF 同理
 * 盈利：ROE、ROA、毛利率、净利率、营业利润率越高越好
 * 成长：增速越高越好
 * 健康：流动比率/速动比率适中最好，资产负债率越低越好，利息保障倍数越高越好
 */
const valuationScore = computed(() => {
  const s = d.value
  let score = 0
  const pe = s.pe_ttm
  const pb = s.pb
  const ps = s.ps_ttm
  const ev = s.ev_ebitda
  const pcf = s.pcf

  // PE 评分 (0-7)
  if (pe !== null && pe !== undefined) {
    if (pe < 0) score += 1
    else if (pe < 15) score += 7
    else if (pe < 25) score += 6
    else if (pe < 40) score += 5
    else if (pe < 60) score += 3
    else score += 1
  }

  // PB 评分 (0-5)
  if (pb !== null && pb !== undefined) {
    if (pb < 1) score += 5
    else if (pb < 2) score += 4
    else if (pb < 4) score += 3
    else if (pb < 8) score += 2
    else score += 1
  }

  // PS 评分 (0-5)
  if (ps !== null && ps !== undefined) {
    if (ps < 2) score += 5
    else if (ps < 5) score += 4
    else if (ps < 10) score += 3
    else if (ps < 20) score += 2
    else score += 1
  }

  // EV/EBITDA 评分 (0-4)
  if (ev !== null && ev !== undefined) {
    if (ev < 10) score += 4
    else if (ev < 20) score += 3
    else if (ev < 35) score += 2
    else score += 1
  }

  // PCF 评分 (0-4)
  if (pcf !== null && pcf !== undefined) {
    if (pcf < 10) score += 4
    else if (pcf < 20) score += 3
    else if (pcf < 35) score += 2
    else score += 1
  }

  return Math.min(25, score)
})

const profitabilityScore = computed(() => {
  const s = d.value
  let score = 0

  // ROE (0-7)
  const roe = s.roe
  if (roe !== null && roe !== undefined) {
    if (roe >= 25) score += 7
    else if (roe >= 20) score += 6
    else if (roe >= 15) score += 5
    else if (roe >= 10) score += 3
    else if (roe >= 5) score += 2
    else score += 1
  }

  // ROA (0-5)
  const roa = s.roa
  if (roa !== null && roa !== undefined) {
    if (roa >= 15) score += 5
    else if (roa >= 10) score += 4
    else if (roa >= 5) score += 3
    else if (roa >= 2) score += 2
    else score += 1
  }

  // 毛利率 (0-5)
  const gm = s.gross_margin
  if (gm !== null && gm !== undefined) {
    if (gm >= 60) score += 5
    else if (gm >= 40) score += 4
    else if (gm >= 25) score += 3
    else if (gm >= 10) score += 2
    else score += 1
  }

  // 净利率 (0-4)
  const nm = s.net_margin
  if (nm !== null && nm !== undefined) {
    if (nm >= 25) score += 4
    else if (nm >= 15) score += 3
    else if (nm >= 8) score += 2
    else score += 1
  }

  // 营业利润率 (0-4)
  const om = s.operating_margin
  if (om !== null && om !== undefined) {
    if (om >= 20) score += 4
    else if (om >= 12) score += 3
    else if (om >= 5) score += 2
    else score += 1
  }

  return Math.min(25, score)
})

const growthScore = computed(() => {
  const s = d.value
  let score = 0

  const scoreGrowth = (v) => {
    if (v === null || v === undefined) return 0
    if (v >= 30) return 7
    if (v >= 20) return 6
    if (v >= 10) return 5
    if (v >= 5) return 3
    if (v >= 0) return 2
    if (v >= -10) return 1
    return 0
  }

  // 营收增速3年 (0-7)
  score += scoreGrowth(s.revenue_growth_3y)
  // 利润增速3年 (0-6)
  score += Math.round(scoreGrowth(s.profit_growth_3y) * 6 / 7)
  // 营收增速5年 (0-6)
  score += Math.round(scoreGrowth(s.revenue_growth_5y) * 6 / 7)
  // 利润增速5年 (0-6)
  score += Math.round(scoreGrowth(s.profit_growth_5y) * 6 / 7)

  return Math.min(25, score)
})

const healthScore = computed(() => {
  const s = d.value
  let score = 0

  // 流动比率 (0-7)：2左右最佳
  const cr = s.current_ratio
  if (cr !== null && cr !== undefined) {
    if (cr >= 2 && cr <= 4) score += 7
    else if (cr >= 1.5 && cr < 2) score += 6
    else if (cr > 4 && cr <= 6) score += 5
    else if (cr >= 1 && cr < 1.5) score += 4
    else if (cr > 6) score += 3
    else if (cr >= 0.5 && cr < 1) score += 2
    else score += 1
  }

  // 速动比率 (0-6)：1.5左右最佳
  const qr = s.quick_ratio
  if (qr !== null && qr !== undefined) {
    if (qr >= 1.5 && qr <= 3) score += 6
    else if (qr >= 1 && qr < 1.5) score += 5
    else if (qr > 3 && qr <= 5) score += 4
    else if (qr >= 0.5 && qr < 1) score += 3
    else if (qr > 5) score += 2
    else score += 1
  }

  // 资产负债率 (0-6)：越低越好
  const dr = s.debt_ratio
  if (dr !== null && dr !== undefined) {
    if (dr < 20) score += 6
    else if (dr < 35) score += 5
    else if (dr < 50) score += 4
    else if (dr < 65) score += 3
    else if (dr < 80) score += 2
    else score += 1
  }

  // 利息保障倍数 (0-6)：越高越好
  const ic = s.interest_coverage
  if (ic !== null && ic !== undefined) {
    if (ic >= 20) score += 6
    else if (ic >= 10) score += 5
    else if (ic >= 5) score += 4
    else if (ic >= 3) score += 3
    else if (ic >= 1) score += 2
    else score += 1
  }

  return Math.min(25, score)
})

const overallScore = computed(() => {
  return valuationScore.value + profitabilityScore.value + growthScore.value + healthScore.value
})

const getScoreColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}

// ---------- 分析师观点 ----------

const getRatingType = (rating) => {
  if (!rating) return 'info'
  const r = rating.toLowerCase()
  if (r.includes('买入') || r.includes('强烈推荐') || r.includes('增持')) return 'danger'
  if (r.includes('中性') || r.includes('持有')) return 'warning'
  if (r.includes('减持') || r.includes('卖出') || r.includes('回避')) return 'success'
  return 'info'
}

// ---------- 数据获取（并行请求） ----------

const fetchAllData = async () => {
  loading.value = true
  try {
    const symbol = route.params.symbol
    const [detailRes, compRes, peersRes, trendRes, sourcesRes] = await Promise.all([
      stockApi.getStockDetail(symbol).catch(e => { console.error('获取股票详情失败:', e); return null }),
      stockApi.getSectorComparison(symbol).catch(e => { console.error('获取行业对比失败:', e); return null }),
      stockApi.getPeers(symbol).catch(e => { console.error('获取同业数据失败:', e); return null }),
      stockApi.getHistoryTrend(symbol).catch(e => { console.error('获取历史趋势失败:', e); return null }),
      stockApi.getSources(symbol, { page: 1, page_size: 10 }).catch(e => { console.error('获取信息源失败:', e); return null })
    ])

    if (detailRes && detailRes.code === 200 && detailRes.data) {
      stockInfo.value = detailRes.data
    }
    if (compRes && compRes.code === 200 && compRes.data) {
      sectorComp.value = compRes.data
    }
    if (peersRes && peersRes.code === 200 && peersRes.data) {
      peers.value = Array.isArray(peersRes.data) ? peersRes.data : []
    }
    if (trendRes && trendRes.code === 200 && trendRes.data) {
      historyTrend.value = trendRes.data
    }
    if (sourcesRes && sourcesRes.code === 200 && sourcesRes.data) {
      sourceList.value = sourcesRes.data.list || []
      sourceTotal.value = sourcesRes.data.total || 0
    }
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

const fetchAnalystViews = async () => {
  try {
    const symbol = route.params.symbol
    const res = await analystApi.getStockViews(symbol)
    if (res.code === 200 && res.data) {
      analystViews.value = Array.isArray(res.data) ? res.data : (res.data.list || res.data.records || [])
    }
  } catch (error) {
    console.error('获取分析师观点失败:', error)
  }
}

onMounted(() => {
  fetchAllData()
  fetchAnalystViews()
})
</script>

<style scoped>
.stock-detail-page {
  padding: 0;
  position: relative;
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
  flex-wrap: wrap;
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

.price-extra {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.price-change {
  padding: 6px 16px;
  border-radius: 6px;
  font-size: 18px;
  font-weight: 600;
}

.price-amount {
  font-size: 14px;
  font-weight: 500;
}

.price-change.up,
.price-amount.up {
  color: #f56c6c;
}

.price-change.down,
.price-amount.down {
  color: #67c23a;
}

.price-change.up {
  background: #fef0f0;
}

.price-change.down {
  background: #f0f9eb;
}

/* 行情概览 */
.quote-bar {
  background: white;
  border-radius: 12px;
  padding: 16px 24px;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.quote-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 80px;
}

.quote-label {
  font-size: 12px;
  color: #909399;
}

.quote-val {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  font-family: 'Monaco', 'Menlo', monospace;
}

.quote-val.up {
  color: #f56c6c;
}

.quote-val.down {
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
  flex-shrink: 0;
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

.peer-icon {
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
  color: white;
}

.analyst-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  flex: 1;
}

.rank-badge {
  flex-shrink: 0;
}

.metric-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.growth .metric-cards,
.health .metric-cards {
  grid-template-columns: repeat(2, 1fr);
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

.metric-item {
  display: flex;
  flex-direction: column;
}

.metric-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 4px;
  font-family: 'Monaco', 'Menlo', monospace;
}

/* 行业对比 & 历史趋势 */
.metric-compare {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 4px;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.metric-compare .best {
  color: #b0b8c4;
}

.metric-trend {
  font-size: 11px;
  margin-top: 2px;
}

.metric-trend .trend-up {
  color: #f56c6c;
}

.metric-trend .trend-down {
  color: #67c23a;
}

/* 同业对比 */
.peer-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.peer-section .section-header {
  margin-bottom: 16px;
}

.peer-table {
  font-size: 13px;
}

.peer-table :deep(.current-peer-row) {
  background-color: #f0f5ff !important;
}

.peer-table :deep(.current-peer-row td) {
  background-color: #f0f5ff !important;
}

.current-stock-name {
  font-weight: 600;
  color: #667eea;
}

.best-value {
  font-weight: 700;
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
}

/* 分析师观点 */
.analyst-views-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.analyst-views-section .section-header {
  margin-bottom: 20px;
}

.analyst-views-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.analyst-view-card {
  background: #f9fafb;
  border-radius: 10px;
  padding: 18px;
  transition: all 0.2s;
}

.analyst-view-card:hover {
  background: #f0f2f5;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.analyst-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.analyst-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.analyst-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.analyst-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.view-date {
  font-size: 12px;
  color: #909399;
}

.view-content p {
  font-size: 14px;
  color: #606266;
  line-height: 1.7;
  margin: 0;
}

.view-tags {
  display: flex;
  gap: 6px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.view-tag {
  border-radius: 4px;
}

/* 报告日期 */
.report-date {
  text-align: center;
  font-size: 13px;
  color: #909399;
  padding: 8px 0;
}

/* 信息源浮动按钮 */
.source-fab {
  position: fixed;
  bottom: 40px;
  right: 40px;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  transition: all 0.3s;
  z-index: 100;
}

.source-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 24px rgba(102, 126, 234, 0.6);
}

/* 信息源抽屉 */
.source-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 200px;
}

.source-card {
  padding: 14px;
  border-radius: 8px;
  background: #f9fafb;
  border-left: 3px solid #dcdfe6;
  transition: background 0.2s;
}

.source-card:hover {
  background: #f0f2f5;
}

.source-card.sentiment-border-positive {
  border-left-color: #67c23a;
}

.source-card.sentiment-border-negative {
  border-left-color: #f56c6c;
}

.source-card.sentiment-border-neutral {
  border-left-color: #dcdfe6;
}

.source-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 6px;
  line-height: 1.4;
}

.source-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.source-name {
  font-size: 12px;
  color: #909399;
}

.source-time {
  font-size: 12px;
  color: #b0b8c4;
}

.source-summary {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 8px;
}

.source-sentiment {
  margin-top: 4px;
}

.source-pagination {
  display: flex;
  justify-content: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

/* 响应式 */
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

  .quote-bar {
    justify-content: flex-start;
  }

  .rating-detail {
    flex-wrap: wrap;
    gap: 16px;
  }

  .source-fab {
    bottom: 24px;
    right: 24px;
    width: 44px;
    height: 44px;
  }
}
</style>
