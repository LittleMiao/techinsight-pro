<template>
  <div class="home-page">
    <div class="page-header">
      <h1 class="page-title">股票列表</h1>
      <div class="header-actions">
        <el-select v-model="sectorFilter" placeholder="选择行业" clearable class="sector-select">
          <el-option label="全部行业" value="" />
          <el-option label="科技" value="科技" />
          <el-option label="金融" value="金融" />
          <el-option label="消费" value="消费" />
          <el-option label="医疗" value="医疗" />
          <el-option label="能源" value="能源" />
        </el-select>
      </div>
    </div>

    <el-tabs v-model="activeTab" @tab-change="handleTabChange" class="sector-tabs">
      <el-tab-pane label="全部" name="all" />
      <el-tab-pane label="科技" name="tech" />
      <el-tab-pane label="金融" name="finance" />
      <el-tab-pane label="消费" name="consumer" />
      <el-tab-pane label="医疗" name="healthcare" />
      <el-tab-pane label="能源" name="energy" />
    </el-tabs>

    <div class="search-section">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索股票代码或名称..."
        clearable
        size="large"
        class="stock-search"
        @input="handleSearchInput"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <el-table
      :data="filteredStockList"
      v-loading="loading"
      stripe
      class="stock-table"
      @row-click="handleRowClick"
    >
      <el-table-column prop="code" label="股票代码" width="120" />
      <el-table-column prop="name" label="股票名称" min-width="150">
        <template #default="{ row }">
          <span class="stock-name">{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="sector" label="行业" width="100" />
      <el-table-column prop="price" label="现价" width="100" align="right">
        <template #default="{ row }">
          <span class="price">¥{{ row.price?.toFixed(2) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="change" label="涨跌幅" width="120" align="right">
        <template #default="{ row }">
          <span :class="getChangeClass(row.change)">
            {{ row.change >= 0 ? '+' : '' }}{{ row.change?.toFixed(2) }}%
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="pe" label="市盈率" width="100" align="right" />
      <el-table-column prop="pb" label="市净率" width="100" align="right" />
      <el-table-column prop="marketCap" label="市值(亿)" width="120" align="right">
        <template #default="{ row }">
          {{ row.marketCap?.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" align="center">
        <template #default="{ row }">
          <el-button type="primary" size="small" link @click.stop="viewDetail(row)">
            查看详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      layout="total, prev, pager, next"
      class="pagination"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { stockApi } from '../api'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const stockList = ref([])
const activeTab = ref('all')
const sectorFilter = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const sectorMap = {
  all: '',
  tech: '科技',
  finance: '金融',
  consumer: '消费',
  healthcare: '医疗',
  energy: '能源'
}

const filteredStockList = computed(() => {
  let result = stockList.value

  if (sectorFilter.value) {
    result = result.filter(item => item.sector === sectorFilter.value)
  }

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(item =>
      item.code.toLowerCase().includes(keyword) ||
      item.name.toLowerCase().includes(keyword)
    )
  }

  return result
})

const getChangeClass = (change) => {
  if (change > 0) return 'change-up'
  if (change < 0) return 'change-down'
  return ''
}

const handleTabChange = (tabName) => {
  sectorFilter.value = sectorMap[tabName]
}

const handleSearchInput = () => {
  currentPage.value = 1
}

const handleRowClick = (row) => {
  router.push(`/stock/${row.code}`)
}

const viewDetail = (row) => {
  router.push(`/stock/${row.code}`)
}

const fetchStockList = async () => {
  loading.value = true
  try {
    const response = await stockApi.getStockList({
      page: currentPage.value,
      page_size: pageSize.value
    })
    stockList.value = response.data.stocks || []
    total.value = response.data.total || stockList.value.length
  } catch (error) {
    console.error('获取股票列表失败:', error)
    // 使用模拟数据
    stockList.value = [
      { code: '600519', name: '贵州茅台', sector: '消费', price: 1688.00, change: 2.35, pe: 32.5, pb: 11.2, marketCap: 21200 },
      { code: '000858', name: '五粮液', sector: '消费', price: 145.60, change: -1.23, pe: 22.8, pb: 5.6, marketCap: 5650 },
      { code: '600036', name: '招商银行', sector: '金融', price: 35.80, change: 0.85, pe: 8.2, pb: 1.3, marketCap: 8960 },
      { code: '601318', name: '中国平安', sector: '金融', price: 48.50, change: -0.52, pe: 9.5, pb: 1.5, marketCap: 8880 },
      { code: '000001', name: '平安银行', sector: '金融', price: 12.35, change: 1.20, pe: 6.8, pb: 0.9, marketCap: 2380 },
      { code: '600276', name: '恒瑞医药', sector: '医疗', price: 52.80, change: 3.45, pe: 65.2, pb: 8.9, marketCap: 3360 },
      { code: '300760', name: '迈瑞医疗', sector: '医疗', price: 298.50, change: 1.78, pe: 45.6, pb: 12.3, marketCap: 3640 },
      { code: '002594', name: '比亚迪', sector: '科技', price: 268.00, change: -2.15, pe: 38.5, pb: 7.8, marketCap: 7800 },
      { code: '600030', name: '中信证券', sector: '金融', price: 22.50, change: 0.45, pe: 18.2, pb: 1.8, marketCap: 3280 },
      { code: '601888', name: '中国中免', sector: '消费', price: 68.90, change: 2.10, pe: 28.5, pb: 6.2, marketCap: 1340 }
    ]
    total.value = stockList.value.length
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (route.query.search) {
    searchKeyword.value = route.query.search
  }
  fetchStockList()
})

watch(() => route.query.search, (newVal) => {
  if (newVal) {
    searchKeyword.value = newVal
  }
})
</script>

<style scoped>
.home-page {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.sector-select {
  width: 160px;
}

.sector-tabs {
  margin-bottom: 20px;
}

.search-section {
  margin-bottom: 20px;
}

.stock-search {
  max-width: 400px;
}

.stock-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.stock-table :deep(.el-table__row) {
  cursor: pointer;
  transition: background-color 0.2s;
}

.stock-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.stock-name {
  font-weight: 500;
  color: #409eff;
}

.price {
  font-weight: 600;
  font-family: 'Monaco', 'Menlo', monospace;
}

.change-up {
  color: #f56c6c;
  font-weight: 600;
}

.change-down {
  color: #67c23a;
  font-weight: 600;
}

.pagination {
  margin-top: 20px;
  justify-content: flex-end;
}
</style>
