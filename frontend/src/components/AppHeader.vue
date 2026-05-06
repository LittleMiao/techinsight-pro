<template>
  <header class="header">
    <div class="header-left">
      <div class="logo" @click="$router.push('/')">
        <el-icon size="28" color="#1e40af"><TrendCharts /></el-icon>
        <span class="logo-text">TechInsight Pro</span>
      </div>
    </div>
    <div class="header-center">
      <el-autocomplete
        v-model="searchQuery"
        :fetch-suggestions="handleSearch"
        placeholder="搜索股票代码/名称"
        class="search-input"
        clearable
        @select="handleSelect"
        :trigger-on-focus="false"
      >
        <template #prefix><el-icon><Search /></el-icon></template>
        <template #default="{ item }">
          <div class="search-item">
            <span class="search-name">{{ item.name }}</span>
            <span class="search-symbol">{{ item.symbol }}</span>
            <span class="search-sector">{{ item.sector }}</span>
          </div>
        </template>
      </el-autocomplete>
    </div>
    <div class="header-right">
      <el-button type="primary" plain><el-icon><User /></el-icon>登录</el-button>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { stockApi } from '../api'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = async (queryString, cb) => {
  if (!queryString || queryString.length < 1) {
    cb([])
    return
  }
  try {
    const res = await stockApi.getStocks({ page_size: 100 })
    if (res.code === 200) {
      const q = queryString.toLowerCase()
      const results = res.data.list.filter(s =>
        s.symbol.toLowerCase().includes(q) ||
        s.name.toLowerCase().includes(q)
      ).map(s => ({
        value: s.name,
        name: s.name,
        symbol: s.symbol,
        sector: s.sub_sector || s.sector
      }))
      cb(results)
    } else {
      cb([])
    }
  } catch {
    cb([])
  }
}

const handleSelect = (item) => {
  router.push(`/stock/${item.symbol}`)
  searchQuery.value = ''
}
</script>

<style scoped>
.header {
  height: 60px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}
.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #1e40af;
}
.header-center {
  flex: 1;
  max-width: 400px;
  margin: 0 40px;
}
.search-input { width: 100%; }
.search-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 0;
}
.search-name {
  font-weight: 600;
  color: #1e293b;
}
.search-symbol {
  font-size: 12px;
  color: #64748b;
}
.search-sector {
  font-size: 12px;
  color: #94a3b8;
  margin-left: auto;
}
</style>
