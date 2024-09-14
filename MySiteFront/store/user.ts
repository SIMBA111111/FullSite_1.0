import { defineStore } from 'pinia'

export const useUserStore = defineStore('useUserStore', {
    state: () => {
      return {
        user: null as UserInfo | null,
      }
    },
  })
  
interface UserInfo {
  username: string
  is_admin: boolean
}
