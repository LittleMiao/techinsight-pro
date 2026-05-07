import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 30000
})

apiClient.interceptors.response.use(
  response => response.data,
  error => Promise.reject(error)
)

// 分析师 API
export const analystApi = {
  getAnalysts: (params) => apiClient.get('/analysts', { params }),
  getAnalyst: (id) => apiClient.get(`/analysts/${id}`),
  getAnalystList: (params) => apiClient.get('/analysts', { params }),
  getAnalystDetail: (id) => apiClient.get(`/analysts/${id}`),
  simulateAnalysis: (analystId, symbol) => apiClient.post(`/analysts/${analystId}/simulate`, { symbol }),
  getStockViews: (symbol) => apiClient.get(`/stocks/${symbol}/analyst-views`)
}

// 股票 API
export const stockApi = {
  getStocks: (params) => apiClient.get('/stocks', { params }),
  getStockList: (params) => apiClient.get('/stocks', { params }),
  getStockDetail: (symbol) => apiClient.get(`/stocks/${symbol}`),
  // 新增：行业对比
  getSectorComparison: (symbol) => apiClient.get(`/stocks/${symbol}/sector-comparison`),
  // 新增：同业对比
  getPeers: (symbol) => apiClient.get(`/stocks/${symbol}/peers`),
  // 新增：历史趋势
  getHistoryTrend: (symbol) => apiClient.get(`/stocks/${symbol}/history-trend`),
  // 新增：信息源
  getSources: (symbol, params) => apiClient.get(`/stocks/${symbol}/sources`, { params })
}

export default apiClient
