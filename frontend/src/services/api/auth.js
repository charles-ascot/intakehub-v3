import api from './client'

export const authService = {
  // TODO: Add API methods for auth
  async get() {
    return api.get('/auth')
  },
  async create(data) {
    return api.post('/auth', data)
  }
}

export default authService
