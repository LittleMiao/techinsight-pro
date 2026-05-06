<template>
  <header class="app-header">
    <div class="header-content">
      <div class="header-left">
        <div class="logo" @click="$router.push('/')">
          <span class="logo-icon">T</span>
          <span class="logo-text">TechInsight<span class="logo-pro">Pro</span></span>
        </div>
        <nav class="nav-menu">
          <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
            股票列表
          </router-link>
          <router-link to="/analyst" class="nav-item" :class="{ active: $route.path === '/analyst' }">
            分析师
          </router-link>
        </nav>
      </div>
      <div class="header-right">
        <el-input
          v-model="searchQuery"
          placeholder="搜索股票代码或名称..."
          class="search-input"
          clearable
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/', query: { search: searchQuery.value } })
  }
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.logo-text {
  font-size: 22px;
  font-weight: 600;
  color: white;
}

.logo-pro {
  font-size: 14px;
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 4px;
}

.nav-menu {
  display: flex;
  gap: 8px;
}

.nav-item {
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.25);
  color: white;
}

.header-right {
  flex: 0 0 300px;
}

.search-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: none;
}

.search-input :deep(.el-input__inner) {
  color: #303133;
}
</style>
