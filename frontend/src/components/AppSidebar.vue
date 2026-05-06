<template>
  <aside class="sidebar">
    <nav class="nav-menu">
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
        <el-icon><HomeFilled /></el-icon>
        <span>首页</span>
      </router-link>
      <router-link to="/analysts" class="nav-item" :class="{ active: $route.path.startsWith('/analysts') }">
        <el-icon><UserFilled /></el-icon>
        <span>分析师视角</span>
      </router-link>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 200px;
  background: white;
  border-right: 1px solid #e2e8f0;
  padding: 16px 0;
  flex-shrink: 0;
}
.nav-menu {
  display: flex;
  flex-direction: column;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: #64748b;
  text-decoration: none;
  transition: all 0.2s;
}
.nav-item:hover {
  background: #f1f5f9;
  color: #1e40af;
}
.nav-item.active {
  background: #eff6ff;
  color: #1e40af;
  border-right: 3px solid #1e40af;
}
</style>
