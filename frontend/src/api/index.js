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
  getStockDetail: (symbol) => apiClient.get(`/stocks/${symbol}`)
}

export default apiClient
