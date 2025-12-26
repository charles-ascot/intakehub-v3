import api from './client'

export const providersService = {
  // TODO: Add API methods for providers
  async get() {
    return api.get('/providers')
  },
  async create(data) {
    return api.post('/providers', data)
  }
}

export default providersService
