import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 分析师 API
export const analystApi = {
  // 获取分析师列表
  getAnalystList(params) {
    return apiClient.get('/analysts', { params })
  },

  // 获取分析师详情
  getAnalystDetail(analystId) {
    return apiClient.get(`/analysts/${analystId}`)
  },

  // 获取分析师评分历史
  getAnalystRatingHistory(analystId) {
    return apiClient.get(`/analysts/${analystId}/ratings`)
  },

  // 获取分析师关注的股票
  getAnalystFollowedStocks(analystId) {
    return apiClient.get(`/analysts/${analystId}/stocks`)
  }
}

// 股票 API
export const stockApi = {
  // 获取股票列表
  getStockList(params) {
    return apiClient.get('/stocks', { params })
  },

  // 获取股票详情
  getStockDetail(code) {
    return apiClient.get(`/stocks/${code}`)
  },

  // 获取股票估值指标
  getValuationMetrics(code) {
    return apiClient.get(`/stocks/${code}/valuation`)
  },

  // 获取股票盈利能力指标
  getProfitabilityMetrics(code) {
    return apiClient.get(`/stocks/${code}/profitability`)
  },

  // 获取股票成长性指标
  getGrowthMetrics(code) {
    return apiClient.get(`/stocks/${code}/growth`)
  },

  // 获取股票健康度指标
  getHealthMetrics(code) {
    return apiClient.get(`/stocks/${code}/health`)
  },

  // 获取股票历史评分
  getStockRatingHistory(code) {
    return apiClient.get(`/stocks/${code}/ratings`)
  }
}

export default apiClient
