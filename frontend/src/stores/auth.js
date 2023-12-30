import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({ isAuthenticated: false }),
    actions: {
      login() {
        this.isAuthenticated = true
        this.router.push('/')
      },
      logout() {
        this.isAuthenticated = false
      },
    },
  })
  