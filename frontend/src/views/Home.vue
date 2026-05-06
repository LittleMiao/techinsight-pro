<template>
  <div class="home-page">
    <div class="page-header">
      <h1 class="page-title">股票列表</h1>
      <div class="header-actions">
        <el-select v-model="sectorFilter" placeholder="选择行业" clearable class="sector-select" @change="handleSectorChange">
          <el-option label="全部行业" value="" />
          <el-option label="半导体" value="semiconductor" />
          <el-option label="AI" value="ai" />
          <el-option label="新能源" value="new_energy" />
          <el-option label="云计算" value="cloud_computing" />
        </el-select>
      </div>
    </div>

    <el-tabs v-model="activeTab" @tab-change="handleTabChange" class="sector-tabs">
      <el-tab-pane label="全部" name="all" />
      <el-tab-pane label="半导体" name="semiconductor" />
      <el-tab-pane label="AI" name="ai" />
      <el-tab-pane label="新能源" name="new_energy" />
      <el-tab-pane label="云计算" name="cloud_computing" />
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
      <el-table-column prop="symbol" label="股票代码" width="140" />
      <el-table-column prop="name" label="股票名称" min-width="150">
        <template #default="{ row }">
          <span class="stock-name">
            {{ row.name }}
            <el-tag v-if="row.is_hot" type="danger" size="small" class="hot-tag">热</el-tag>
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="sector" label="行业" width="100">
        <template #default="{ row }">
          {{ sectorLabelMap[row.sector] || row.sector }}
        </template>
      </el-table-column>
      <el-table-column prop="market" label="市场" width="80" />
      <el-table-column prop="price" label="现价" width="100" align="right">
        <template #default="{ row }">
          <span class="price">&yen;{{ row.price?.toFixed(2) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="change_percent" label="涨跌幅" width="120" align="right">
        <template #default="{ row }">
          <span :class="getChangeClass(row.change_percent)">
            {{ row.change_percent >= 0 ? '+' : '' }}{{ row.change_percent?.toFixed(2) }}%
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="market_cap" label="市值(亿)" width="120" align="right">
        <template #default="{ row }">
          {{ formatMarketCap(row.market_cap) }}
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
      @current-change="handlePageChange"
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

const sectorLabelMap = {
  semiconductor: '半导体',
  ai: 'AI',
  new_energy: '新能源',
  cloud_computing: '云计算'
}

// 前端本地搜索过滤（API 不支持关键字搜索）
const filteredStockList = computed(() => {
  if (!searchKeyword.value) {
    return stockList.value
  }
  const keyword = searchKeyword.value.toLowerCase()
  return stockList.value.filter(item =>
    item.symbol.toLowerCase().includes(keyword) ||
    item.name.toLowerCase().includes(keyword)
  )
})

const formatMarketCap = (marketCap) => {
  if (marketCap == null) return '--'
  return (marketCap / 100000000).toFixed(2)
}

const getChangeClass = (changePercent) => {
  if (changePercent > 0) return 'change-up'
  if (changePercent < 0) return 'change-down'
  return ''
}

const handleTabChange = (tabName) => {
  if (tabName === 'all') {
    sectorFilter.value = ''
  } else {
    sectorFilter.value = tabName
  }
  currentPage.value = 1
  fetchStockList()
}

const handleSectorChange = () => {
  // 同步 tab 状态
  if (sectorFilter.value === '') {
    activeTab.value = 'all'
  } else {
    activeTab.value = sectorFilter.value
  }
  currentPage.value = 1
  fetchStockList()
}

const handleSearchInput = () => {
  // 搜索为前端本地过滤，不需要重新请求
}

const handlePageChange = () => {
  fetchStockList()
}

const handleRowClick = (row) => {
  router.push(`/stock/${row.symbol}`)
}

const viewDetail = (row) => {
  router.push(`/stock/${row.symbol}`)
}

const fetchStockList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (sectorFilter.value) {
      params.sector = sectorFilter.value
    }
    const res = await stockApi.getStockList(params)
    // 响应拦截器已解包 response.data，res = { code: 200, data: { total, page, page_size, list } }
    stockList.value = res.data?.list || []
    total.value = res.data?.total || 0
  } catch (error) {
    console.error('获取股票列表失败:', error)
    stockList.value = []
    total.value = 0
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

.hot-tag {
  margin-left: 4px;
  vertical-align: middle;
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
