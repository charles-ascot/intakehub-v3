import api from './client'

export const healthService = {
  // TODO: Add API methods for health
  async get() {
    return api.get('/health')
  },
  async create(data) {
    return api.post('/health', data)
  }
}

export default healthService
