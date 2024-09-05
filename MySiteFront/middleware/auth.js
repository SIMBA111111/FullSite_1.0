import { useUserStore } from "~/store/user";
import { url } from "../MyConstants.vue";
import axios from 'axios';
import { useCookie } from '#app';

export default defineNuxtRouteMiddleware(async (to, from) => {
  const userStore = useUserStore(); 
  const getMeUrl = `${url}/users/me`;

  try {
    const result = await axios.post(getMeUrl, null, {
      headers: {
        "Authorization": useCookie('access_token').value
      }
    });

    const me = result.data;
    
    if (!userStore.user) {
      userStore.user = {};
    }

    userStore.user.is_admin = me.data.is_admin;
    userStore.user.username = me.data.username;
    
  } catch (error) {
    console.error('Error fetching user data:', error);
  }
});
