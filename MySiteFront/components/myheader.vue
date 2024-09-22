<template>
  <div class="header">
    <div class="first">
      <NuxtLink to="/" exact-active-class="active">Название</NuxtLink>
    </div>
    <div class="links">
      <div v-if="userStore.user?.is_admin"><NuxtLink to="/admin/bidList" target="_blank" exact-active-class="active" class="el write">В админку</NuxtLink></div>
      <div v-if="authed"><NuxtLink to="/articles/create" exact-active-class="active" class="el write">Написать</NuxtLink></div>
      <div><NuxtLink to="/search" exact-active-class="active" class="el">Поиск</NuxtLink></div>
      <div><NuxtLink to="/articles" exact-active-class="active" class="el">Статьи</NuxtLink></div>
      <div><NuxtLink to="/authors" exact-active-class="active" class="el">Авторы</NuxtLink></div>
      <!-- <div><NuxtLink to="/vacancies" exact-active-class="active" class="el">Услуги</NuxtLink></div> -->
      <div><NuxtLink @mouseover="f" @mouseout="f1" exact-active-class="active" class="el">Услуги</NuxtLink></div>
      <div v-if="showOption" @mouseover="f" @mouseout="f1" class="option">
        <div><NuxtLink to="/vacancies" exact-active-class="active" class="el">Вакансии</NuxtLink></div>
        <div><NuxtLink to="/feedback" exact-active-class="active" class="el">Обратная связь</NuxtLink></div>
        <div><NuxtLink to="/mentoring" exact-active-class="active" class="el">Менторство</NuxtLink></div>
      </div>
      
      <!-- <div>
        <select class="select el" name="vac" id="">
          <option class="option" selected value=""><NuxtLink>serves</NuxtLink></option>
          <option class="option" value=""><NuxtLink>vac</NuxtLink></option>
          <option class="option" value=""><NuxtLink>back</NuxtLink></option>
          <option class="option" value=""><NuxtLink>ment</NuxtLink></option>
        </select>
      </div> -->
      <!-- <div v-if="!authed"><NuxtLink to="/auth/register" exact-active-class="active" class="el">Регистрация</NuxtLink></div> -->
      <div v-if="!authed"><NuxtLink to="/auth/login" exact-active-class="active" class="el">Вход</NuxtLink></div>
      <div v-else @click="logout" @mouseover="mouseOverExit" @mouseout="mouseOutExit"><NuxtLink to="/" exact-active-class="active" class="el d">{{ exit || userStore.user?.username }}</NuxtLink></div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, watch } from 'vue';
import { useCookie, useRouter } from '#app';
import { url } from "../MyConstants.vue";
import { useUserStore } from '~/store/user';
import { set } from '~/node_modules/nuxt/dist/app/compat/capi';

const exit = ref('');

const mouseOverExit = () => {
  exit.value = 'Выйти';
} 

const mouseOutExit = () => {
  exit.value = '';
} 

const showOption = ref(false);

let timer = null;

const startTimeout = () => {
  timer = setTimeout(() => {
    showOption.value = false;
  }, 100);
};


const f = () => {
  // document.querySelector('.option').style = 'opacity: 1;';
  showOption.value = true;
  clearTimeout(timer);
}

const f1 = () => {
  startTimeout()
  // document.querySelector('.option').style = 'opacity: 0;';
}

const authed = ref(false);
const userStore = useUserStore()

const checkAuth = () => {
  const token = useCookie('access_token').value;
  authed.value = !!token;
};

const logout_url = `${url}/auth/logout`;
const logout = async () => {
  try {
    const access_token = useCookie('access_token').value;

    const response = await axios.delete(logout_url, {
      headers: {
        'access-token': access_token,
        'Authorization': access_token 
      }
    });

    useCookie('access_token').value = null;

    checkAuth();

    const router = useRouter();
    await router.push('/');
    location.reload();

  } catch (error) {
    console.error('Error:', error);
  }
};

checkAuth();

watch(authed, (newValue) => {});
</script>

<style scoped>
*{
  box-sizing: border-box;
}

.option{
  opacity: 1;
}

.select {
  width: 100px;
  height: 70px;
  text-decoration: none;
  border: none;
  border-radius: 50px;
  color: #ffffff;
  font-size: 18px;
  padding: 20px 20px;
  /* border: 1px solid transparent; */
  position: relative;
  display: inline-block;
  background-color: transparent;
  transition: color 0.3s, transform 0.3s, filter 0.3s, box-shadow 0.3s;
  /* -webkit-appearance: none */
}

.select:hover {
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateZ(10px);
  border-radius: 50%;
  background: linear-gradient(to right, transparent 1%, #686868 15% 85%,  transparent 99%);
}

.el {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.option {
  height: 100px;
  display: flex;
  flex-direction: column;
  /* justify-content: center; */
  align-items: center;
  position: absolute;
  top: 100%;
  right: 8%;
}

/* .option {
  width: 100px;
  height: 70px;
  text-decoration: none;
  border: none;
  border-radius: 50px;
  color: #ffffff;
  font-size: 18px;
  padding: 20px 20px;
  position: relative;
  display: inline-block;
  background-color: transparent;
  transition: color 0.3s, transform 0.3s, filter 0.3s, box-shadow 0.3s;
} */

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0px 70px;
  background-color: #191919;
  /* overflow: hidden; */
}

.first {
  margin-right: 50px; /* Промежуток между первым и вторым элементами */
}

.first a {
  text-decoration: none;
  color: #ffffff;
  font-size: 35px;
  padding: 0px 20px;
  border: 1px solid transparent;
  position: relative;
  display: inline-block;
  transition: color 0.3s, transform 0.3s, filter 0.3s, box-shadow 0.3s;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.links {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  position: relative;
}

.links div {
  /* margin: 0 10px; */
  height: 70px;
  border-radius: 50%;
}

.links div:hover {
  padding-bottom: -5px;
}

.links a {
  height: 70px;
  text-decoration: none;
  color: #ffffff;
  font-size: 18px;
  padding: 20px 20px;
  /* border: 1px solid transparent; */
  position: relative;
  display: inline-block;
  transition: color 0.3s, transform 0.3s, filter 0.3s, box-shadow 0.3s;
}

.links a::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* background: rgba(0, 0, 0, 0.5); */
  z-index: -1;
  transition: transform 0.3s, filter 0.3s;
  transform: scale(1);
  filter: blur(0);
}

.links a:active::before {
  transform: scale(1);
}

.links a:hover {
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateZ(10px);
  border-radius: 50%;
  background: radial-gradient(#686868 15%, transparent 70%);

  /* box-shadow: inset #686868 0px 0px 60px -12px; */
  /* background: linear-gradient(to right, transparent 1%, #686868 15% 85%,  transparent 99%); */
}

.links a:active {
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateZ(5px);
  border-radius: 50%;
  background: radial-gradient(#686868 15%, transparent 70%);

  /* box-shadow: inset #686868 0px 0px 60px -12px; */

  /* background: linear-gradient(to right, transparent 1%, #686868 15% 85%,  transparent 99%); */
}

/* Стиль для активной ссылки */
.links a.active {
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateZ(10px);
  border-radius: 50%;
  background: radial-gradient(#686868 15%, transparent 70%);


  /* background: #686868; */

  /* box-shadow: h-offset v-offset blur #191919; */
  /* box-shadow: inset #191919 0px 0px 70px -20px; */

/* background: linear-gradient(to right, transparent 1%, #686868 15% 85%,  transparent 99%); */
}

</style>
