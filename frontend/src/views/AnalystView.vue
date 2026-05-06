<template>
  <div class="analyst-view">
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><UserFilled /></el-icon>
        分析师视角
      </h1>
      <p class="page-subtitle">用博主的思考框架模拟分析股票</p>
    </div>

    <!-- 博主框架库 -->
    <div class="card">
      <h3 class="card-title">博主框架库</h3>
      <div class="analyst-grid">
        <div 
          v-for="analyst in analysts" 
          :key="analyst.analyst_id"
          class="analyst-card"
          :class="{ selected: selectedAnalyst?.analyst_id === analyst.analyst_id }"
          @click="selectAnalyst(analyst)"
        >
          <img :src="analyst.avatar_url" class="analyst-avatar" />
          <div class="analyst-info">
            <div class="analyst-name">{{ analyst.analyst_name }}</div>
            <div class="analyst-platform">{{ analyst.platform }}</div>
            <div class="analyst-stats">
              <span class="stat">
                <el-icon><TrendCharts /></el-icon>
                胜率 {{ analyst.hit_rate?.toFixed(1) }}%
              </span>
              <span class="stat">
                <el-icon><Document /></el-icon>
                {{ analyst.total_judgments }}条判断
              </span>
            </div>
            <div class="analyst-tags">
              <el-tag v-for="tag in analyst.style_tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 模拟分析区域 -->
    <div class="simulation-section" v-if="selectedAnalyst">
      <div class="card">
        <h3 class="card-title">模拟分析</h3>
        
        <div class="simulation-form">
          <div class="form-row">
            <el-select v-model="selectedStock" placeholder="选择股票" filterable style="width: 300px">
              <el-option 
                v-for="stock in stocks" 
                :key="stock.symbol"
                :label="`${stock.name} (${stock.symbol})`"
                :value="stock.symbol"
              />
            </el-select>
            <el-button type="primary" :loading="loading" @click="runSimulation">
              <el-icon><Cpu /></el-icon>
              生成模拟分析
            </el-button>
          </div>
        </div>

        <!-- 分析结果 -->
        <div class="simulation-result" v-if="simulationResult">
          <div class="result-header">
            <div class="result-judgment" :class="judgmentClass">
              {{ judgmentText }}
            </div>
            <div class="result-meta">
              <div class="confidence">
                <span class="label">置信度</span>
                <el-progress :percentage="simulationResult.confidence_score" :color="confidenceColor" />
              </div>
              <div class="similarity">
                风格相似度: <strong>{{ simulationResult.style_similarity }}</strong>
              </div>
            </div>
          </div>

          <div class="analysis-steps">
            <h4>分析过程</h4>
            <div class="step-list">
              <div 
                v-for="(step, idx) in simulationResult.steps" 
                :key="idx"
                class="step-item"
                :class="stepClass(step.result)"
              >
                <div class="step-icon">
                  <el-icon v-if="step.result === '通过'"><CircleCheckFilled /></el-icon>
                  <el-icon v-else-if="step.result === '不通过'"><CircleCloseFilled /></el-icon>
                  <el-icon v-else><WarningFilled /></el-icon>
                </div>
                <div class="step-content">
                  <div class="step-name">{{ step.step }}</div>
                  <div class="step-detail">{{ step.detail }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="findings-section">
            <div class="findings">
              <h4>关键发现</h4>
              <ul>
                <li v-for="(f, idx) in simulationResult.key_findings" :key="idx">{{ f }}</li>
              </ul>
            </div>
            <div class="risks">
              <h4>风险提示</h4>
              <ul>
                <li v-for="(r, idx) in simulationResult.risk_warnings" :key="idx">{{ r }}</li>
              </ul>
            </div>
          </div>

          <div class="full-report">
            <el-collapse>
              <el-collapse-item title="查看完整模拟报告" name="report">
                <pre class="report-content">{{ simulationResult.report }}</pre>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
      </div>
    </div>

    <!-- 博主框架详情 -->
    <div class="card framework-detail" v-if="selectedAnalyst">
      <h3 class="card-title">{{ selectedAnalyst.analyst_name }} 的分析框架</h3>
      
      <div class="framework-sections">
        <div class="framework-section">
          <h4>选股标准</h4>
          <div class="criteria-list">
            <div v-for="(c, idx) in selectedAnalyst.selection_criteria" :key="idx" class="criteria-item">
              <span class="criteria-name">{{ c.criteria }}</span>
              <el-progress :percentage="c.weight" :show-text="false" style="width: 100px" />
              <span class="criteria-weight">{{ c.weight }}%</span>
            </div>
          </div>
        </div>

        <div class="framework-section">
          <h4>决策流程</h4>
          <div class="process-list">
            <div v-for="(p, idx) in selectedAnalyst.decision_process" :key="idx" class="process-item">
              <div class="process-step">{{ idx + 1 }}</div>
              <div class="process-content">
                <div class="process-name">{{ p.step }}</div>
                <div class="process-focus">关注: {{ p.focus }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="framework-section">
          <h4>回避模式</h4>
          <div class="avoid-list">
            <el-tag v-for="a in selectedAnalyst.avoid_patterns" :key="a" type="danger" effect="plain">
              {{ a }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { analystApi, stockApi } from '../api'

const analysts = ref([])
const stocks = ref([])
const selectedAnalyst = ref(null)
const selectedStock = ref('')
const loading = ref(false)
const simulationResult = ref(null)

const judgmentClass = computed(() => {
  if (!simulationResult.value) return ''
  const j = simulationResult.value.simulated_judgment
  return j === 'buy' ? 'judgment-buy' : j === 'sell' ? 'judgment-sell' : 'judgment-hold'
})

const judgmentText = computed(() => {
  if (!simulationResult.value) return ''
  const map = { buy: '看多', sell: '看空', hold: '中性' }
  return map[simulationResult.value.simulated_judgment] || '中性'
})

const confidenceColor = computed(() => {
  if (!simulationResult.value) return '#409eff'
  const c = simulationResult.value.confidence_score
  if (c >= 70) return '#10b981'
  if (c >= 40) return '#f59e0b'
  return '#ef4444'
})

const stepClass = (result) => {
  if (result === '通过') return 'step-pass'
  if (result === '不通过') return 'step-fail'
  return 'step-warn'
}

const selectAnalyst = (analyst) => {
  selectedAnalyst.value = analyst
  simulationResult.value = null
}

const runSimulation = async () => {
  if (!selectedStock.value) return
  loading.value = true
  try {
    const res = await analystApi.simulateAnalysis(selectedAnalyst.value.analyst_id, selectedStock.value)
    if (res.code === 200) {
      simulationResult.value = res.data
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const [analystsRes, stocksRes] = await Promise.all([
    analystApi.getAnalysts(),
    stockApi.getStocks({ page_size: 50 })
  ])
  if (analystsRes.code === 200) analysts.value = analystsRes.data.list
  if (stocksRes.code === 200) stocks.value = stocksRes.data.list
})
</script>

<style scoped>
.analyst-view { max-width: 1400px; margin: 0 auto; }
.page-header { margin-bottom: 24px; }
.page-title { display: flex; align-items: center; gap: 12px; font-size: 28px; font-weight: 700; color: #1e293b; margin: 0; }
.page-subtitle { color: #64748b; margin-top: 8px; }

.analyst-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.analyst-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}
.analyst-card:hover { background: #f1f5f9; }
.analyst-card.selected { border-color: #1e40af; background: #eff6ff; }
.analyst-avatar { width: 60px; height: 60px; border-radius: 50%; }
.analyst-name { font-size: 16px; font-weight: 600; color: #1e293b; }
.analyst-platform { font-size: 12px; color: #94a3b8; margin-top: 2px; }
.analyst-stats { display: flex; gap: 12px; margin-top: 8px; font-size: 12px; color: #64748b; }
.analyst-tags { display: flex; gap: 4px; margin-top: 8px; flex-wrap: wrap; }

.simulation-form { margin-bottom: 24px; }
.form-row { display: flex; gap: 16px; align-items: center; }

.simulation-result { padding-top: 24px; border-top: 1px solid #e2e8f0; }
.result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.result-judgment { font-size: 32px; font-weight: 700; padding: 8px 24px; border-radius: 8px; }
.judgment-buy { background: #dcfce7; color: #166534; }
.judgment-sell { background: #fee2e2; color: #991b1b; }
.judgment-hold { background: #fef9c3; color: #854d0e; }
.result-meta { display: flex; gap: 32px; align-items: center; }
.confidence { width: 200px; }
.confidence .label { font-size: 12px; color: #64748b; margin-bottom: 4px; display: block; }
.similarity { font-size: 14px; color: #64748b; }

.analysis-steps { margin-bottom: 24px; }
.analysis-steps h4 { font-size: 16px; margin-bottom: 16px; color: #1e293b; }
.step-list { display: flex; flex-direction: column; gap: 12px; }
.step-item { display: flex; gap: 12px; padding: 12px; border-radius: 8px; }
.step-pass { background: #f0fdf4; }
.step-fail { background: #fef2f2; }
.step-warn { background: #fffbeb; }
.step-icon { font-size: 24px; }
.step-pass .step-icon { color: #10b981; }
.step-fail .step-icon { color: #ef4444; }
.step-warn .step-icon { color: #f59e0b; }
.step-name { font-weight: 600; color: #1e293b; }
.step-detail { font-size: 14px; color: #64748b; margin-top: 4px; }

.findings-section { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
.findings h4, .risks h4 { font-size: 16px; margin-bottom: 12px; color: #1e293b; }
.findings ul, .risks ul { margin: 0; padding-left: 20px; }
.findings li, .risks li { font-size: 14px; color: #475569; line-height: 1.8; }
.risks li { color: #dc2626; }

.report-content { white-space: pre-wrap; font-size: 13px; line-height: 1.6; background: #f8fafc; padding: 16px; border-radius: 8px; }

.framework-detail { margin-top: 24px; }
.framework-sections { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.framework-section h4 { font-size: 14px; color: #64748b; margin-bottom: 12px; }
.criteria-list { display: flex; flex-direction: column; gap: 8px; }
.criteria-item { display: flex; align-items: center; gap: 8px; }
.criteria-name { flex: 1; font-size: 14px; }
.criteria-weight { font-size: 12px; color: #64748b; width: 40px; }
.process-list { display: flex; flex-direction: column; gap: 8px; }
.process-item { display: flex; gap: 12px; align-items: flex-start; }
.process-step { width: 24px; height: 24px; background: #1e40af; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; }
.process-name { font-size: 14px; font-weight: 500; }
.process-focus { font-size: 12px; color: #94a3b8; }
.avoid-list { display: flex; flex-direction: column; gap: 8px; }
</style>
