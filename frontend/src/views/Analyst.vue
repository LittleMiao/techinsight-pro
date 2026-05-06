<template>
  <div class="analyst-page">
    <div class="page-header">
      <h1 class="page-title">分析师列表</h1>
      <div class="header-actions">
        <el-select v-model="sortBy" placeholder="排序方式" class="sort-select">
          <el-option label="评分最高" value="rating" />
          <el-option label="关注最多" value="followers" />
          <el-option label="最新加入" value="newest" />
        </el-select>
      </div>
    </div>

    <div class="analyst-grid">
      <div
        v-for="analyst in analystList"
        :key="analyst.id"
        class="analyst-card"
      >
        <div class="card-header">
          <el-avatar :size="64" :src="analyst.avatar" class="analyst-avatar">
            {{ analyst.name?.charAt(0) }}
          </el-avatar>
          <div class="analyst-info">
            <h3 class="analyst-name">{{ analyst.name }}</h3>
            <p class="analyst-title">{{ analyst.title }}</p>
            <p class="analyst-institution">{{ analyst.institution }}</p>
          </div>
        </div>

        <div class="card-stats">
          <div class="stat-item">
            <span class="stat-value">{{ analyst.rating }}</span>
            <span class="stat-label">综合评分</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ analyst.correctRate }}%</span>
            <span class="stat-label">准确率</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ analyst.followers }}</span>
            <span class="stat-label">关注者</span>
          </div>
        </div>

        <div class="card-tags">
          <el-tag
            v-for="tag in analyst.expertise"
            :key="tag"
            size="small"
            class="expertise-tag"
          >
            {{ tag }}
          </el-tag>
        </div>

        <div class="card-footer">
          <span class="join-date">加入于 {{ analyst.joinDate }}</span>
          <el-button type="primary" size="small" plain @click="viewProfile(analyst)">
            查看详情
          </el-button>
        </div>
      </div>
    </div>

    <el-empty v-if="analystList.length === 0" description="暂无分析师数据" />

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-count="totalPages"
      layout="prev, pager, next, jumper"
      class="pagination"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { analystApi } from '../api'

const router = useRouter()
const loading = ref(false)
const analystList = ref([])
const sortBy = ref('rating')
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

const handlePageChange = (page) => {
  currentPage.value = page
  fetchAnalystList()
}

const viewProfile = (analyst) => {
  router.push(`/analyst/${analyst.id}`)
}

const fetchAnalystList = async () => {
  loading.value = true
  try {
    const response = await analystApi.getAnalystList({
      page: currentPage.value,
      page_size: pageSize.value,
      sort: sortBy.value
    })
    analystList.value = response.data.analysts || []
    total.value = response.data.total || analystList.value.length
  } catch (error) {
    console.error('获取分析师列表失败:', error)
    // 使用模拟数据
    analystList.value = [
      {
        id: 1,
        name: '张明远',
        title: '首席分析师',
        institution: '中信证券',
        rating: 92.5,
        correctRate: 78,
        followers: 12580,
        expertise: ['科技', '半导体', '人工智能'],
        joinDate: '2022-03-15',
        avatar: ''
      },
      {
        id: 2,
        name: '李婷婷',
        title: '高级分析师',
        institution: '国泰君安',
        rating: 88.3,
        correctRate: 72,
        followers: 8920,
        expertise: ['消费', '食品饮料', '零售'],
        joinDate: '2021-08-22',
        avatar: ''
      },
      {
        id: 3,
        name: '王建国',
        title: '资深分析师',
        institution: '华泰证券',
        rating: 85.6,
        correctRate: 68,
        followers: 6540,
        expertise: ['金融', '银行', '保险'],
        joinDate: '2020-11-10',
        avatar: ''
      },
      {
        id: 4,
        name: '陈思琪',
        title: '行业分析师',
        institution: '招商证券',
        rating: 82.1,
        correctRate: 65,
        followers: 4280,
        expertise: ['医疗', '生物医药', '医疗器械'],
        joinDate: '2023-01-05',
        avatar: ''
      },
      {
        id: 5,
        name: '刘浩然',
        title: '策略分析师',
        institution: '海通证券',
        rating: 90.2,
        correctRate: 75,
        followers: 10580,
        expertise: ['宏观策略', '新能源', '汽车'],
        joinDate: '2021-05-18',
        avatar: ''
      },
      {
        id: 6,
        name: '赵雅婷',
        title: '高级研究员',
        institution: '广发证券',
        rating: 87.8,
        correctRate: 71,
        followers: 7620,
        expertise: ['地产', '建筑', '建材'],
        joinDate: '2022-09-30',
        avatar: ''
      }
    ]
    total.value = analystList.value.length
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAnalystList()
})
</script>

<style scoped>
.analyst-page {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.sort-select {
  width: 140px;
}

.analyst-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.analyst-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.analyst-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.analyst-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-size: 24px;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.analyst-info {
  flex: 1;
  min-width: 0;
}

.analyst-name {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.analyst-title {
  font-size: 14px;
  color: #409eff;
  margin-bottom: 2px;
}

.analyst-institution {
  font-size: 13px;
  color: #909399;
}

.card-stats {
  display: flex;
  justify-content: space-between;
  padding: 16px 0;
  margin-bottom: 16px;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.expertise-tag {
  background: #ecf5ff;
  border-color: #b3d8fd;
  color: #409eff;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.join-date {
  font-size: 12px;
  color: #c0c4cc;
}

.pagination {
  justify-content: center;
}
</style>
