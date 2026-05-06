import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000
})

api.interceptors.response.use(
  response => response.data,
  error => Promise.reject(error)
)

// 博主相关API
export const analystApi = {
  getAnalysts: () => api.get('/analysts'),
  getAnalyst: (id) => api.get(`/analysts/${id}`),
  createAnalyst: (data) => api.post('/analysts', data),
  getJudgments: (id, limit = 20) => api.get(`/analysts/${id}/judgments?limit=${limit}`),
  simulateAnalysis: (analystId, symbol) => api.post(`/analysts/${analystId}/simulate`, { symbol }),
  getStockViews: (symbol) => api.get(`/stocks/${symbol}/analyst-views`)
}

// 股票相关API
export const stockApi = {
  getStocks: (params) => api.get('/stocks', { params }),
  getStockDetail: (symbol) => api.get(`/stocks/${symbol}`)
}

export default api
