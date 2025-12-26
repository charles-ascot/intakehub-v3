import api from './client'

export const testingService = {
  // TODO: Add API methods for testing
  async get() {
    return api.get('/testing')
  },
  async create(data) {
    return api.post('/testing', data)
  }
}

export default testingService
