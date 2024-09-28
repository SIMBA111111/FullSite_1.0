<template>
  <div class="header" :class='{
    open: isBurgerMenu
  }'>
    <div class="container">
      <div class="title">
        <NuxtLink to="/" exact-active-class="active"><span class="title_num">24</span>articles</NuxtLink>
      </div>
      <button @click="openBurgerMenu" class="header__burger-btn">
        <span></span><span></span><span></span>
      </button>
      <div class="links">
        <div v-if="userStore.user?.is_admin"><NuxtLink to="/admin/bidList" target="_blank" exact-active-class="active" class="el write">В админку</NuxtLink></div>
        <div v-if="authed"><NuxtLink to="/articles/create" exact-active-class="active" class="el write">Написать</NuxtLink></div>
        <div><NuxtLink to="/search" exact-active-class="active" class="el">Поиск</NuxtLink></div>
        <div><NuxtLink to="/articles" exact-active-class="active" class="el">Статьи</NuxtLink></div>
        <div><NuxtLink to="/authors" exact-active-class="active" class="el">Авторы</NuxtLink></div>
        <div class="servises"><NuxtLink @mouseover="f" @mouseout="f1" exact-active-class="active" class="el">Услуги</NuxtLink></div>
        <div v-if="showOption" @mouseover="f" @mouseout="f1" class="options">
          <div><NuxtLink to="/vacancies" exact-active-class="active" class="el">Вакансии</NuxtLink></div>
          <div><NuxtLink to="/feedback" exact-active-class="active" class="el">Обратная связь</NuxtLink></div>
          <div><NuxtLink to="/mentoring" exact-active-class="active" class="el">Менторство</NuxtLink></div>
        </div>
        
        <div class="option"><NuxtLink to="/vacancies" exact-active-class="active" class="el">Вакансии</NuxtLink></div>
        <div class="option"><NuxtLink to="/feedback" exact-active-class="active" class="el">Обратная связь</NuxtLink></div>
        <div class="option"><NuxtLink to="/mentoring" exact-active-class="active" class="el">Менторство</NuxtLink></div>

        <div v-if="!authed"><NuxtLink to="/auth/login" exact-active-class="active" class="el">Вход</NuxtLink></div>
        <div v-else @click="logout" @mouseover="mouseOverExit" @mouseout="mouseOutExit"><NuxtLink to="/" exact-active-class="active" class="el d">{{ exit || userStore.user?.username }}</NuxtLink></div>
      </div>
    </div>
    <div class="hr"></div>
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

const isBurgerMenu = ref(false);

const openBurgerMenu = () => {
  isBurgerMenu.value = !isBurgerMenu.value;
}


checkAuth();

watch(authed, (newValue) => {});
</script>

<style scoped>
*{
  box-sizing: border-box;
}

.header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 0px 5vw;
  background-color: #191919;
}

.container {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.title_num {
  color: red;
  /* font-size: 2.5rem; */
  font-size: 3vw;
  font-weight: bold;
}

.title a {
  text-decoration: none;
  color: #ffffff;
  /* font-size: 2.25rem; */
  font-size: 2.85vw;

  padding: 0px 1.25rem;
  border: 1px solid transparent;
  position: relative;
  display: inline-block;
  transition: color 0.3s, transform 0.3s, filter 0.3s, box-shadow 0.3s;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.hr {
  width: 90%;
  height: .5vh;
  border-radius: 0%;
  background-color: #fff;
  margin-bottom: 2vh;
  clip-path: polygon(60% 0%, 60% 0%, 100% 100%, 0% 100%);
}

.el {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.links {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  position: relative;
}

.links div {
  /* height: 70px; */
  border-radius: 50%;
}

.links a {
  /* height: 10.7vh; */
  text-decoration: none;
  color: #ffffff;
  /* font-size: 1.12rem; */
  font-size: 1.4vw;
  /* padding: 1.25rem; */
  padding: 1.5vw;
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
}

.links a:active {
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateZ(5px);
  border-radius: 50%;
  background: radial-gradient(#686868 15%, transparent 70%);
}

/* Стиль для активной ссылки */
.links a.active {
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateZ(10px);
  border-radius: 50%;
  background: radial-gradient(#686868 15%, transparent 70%);
}

.servises {
  display: block;
}

.options{
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  top: 100%;
  right: 8%;

  opacity: 1;
}

.option {
  display: none;
}

.header__burger-btn {
  display: none;
  position: relative;
  width: 40px;
  height: 40px;
  /* border: 1px solid #fff; */
  background-color: transparent;
  z-index: 10;
}

.header__burger-btn span {
  position: absolute;
  width: 30px;
  height: 3px;
  background-color: #fff;
  left: 4px;
  transition: transform .5s, opacity .5s, background-color .5s;
}

.header__burger-btn span:nth-child(1) {
  transform: translateY(-10px);
}

.header__burger-btn span:nth-child(3) {
  transform: translateY(10px);
}

.header.open .header__burger-btn span {
  background-color: black;
}

.header.open .header__burger-btn span:nth-child(1) {
  transform: translateY(0) rotate(-45deg);
}
.header.open .header__burger-btn span:nth-child(2) {
  opacity: 0;
}
.header.open .header__burger-btn span:nth-child(3) {
  transform: translateY(0) rotate(45deg);
}

@media (max-width: 425px) {
  .header__burger-btn {
    display: block;
  }

  .links{
    position: absolute;
    right: -42vw;
    z-index: 9;
    top: 0;
    display: block;
    padding-top: 10vw;
    background-color: rgba(232, 232, 232, 0.9);
    transition: transform .5s;
  }

  .title_num {
    font-size: 8vw;
  }

  .title a {
    font-size: 7vw;
  }

  .links a {
    font-size: 5vw;
    font-weight: bold;
    float: right;
    right: 1vw;
    color: black;  
  }

  .links a:active {
    color: black;
  }
  .links a.active {
    color: black;
  }


  .links a:hover {
    color: black;
  }

  .servises {
    display: none;
  }

  .option {
    display: block;
  }

  .header.open .links {
    transform: translateX(-101%);
  }

}

</style>

<!-- <style scoped>
* {
  box-sizing: border-box;
}

.first_num {
  color: red;
  font-size: 3vw; /* Адаптивный размер */
  font-weight: bold;
}

.hr {
  width: 90%;
  height: 4px;
  border-radius: 0;
  background-color: #fff;
  margin-bottom: 15px;
  clip-path: polygon(60% 0%, 60% 0%, 100% 100%, 0% 100%);
}

.container {
  width: 100%;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap; /* Для адаптивности */
}

.option {
  opacity: 1;
}

.select {
  width: 100px;
  height: 70px;
  text-decoration: none;
  border: none;
  border-radius: 50px;
  color: #ffffff;
  font-size: 1rem; /* Использование rem */
  padding: 20px;
  position: relative;
  display: inline-block;
  background-color: transparent;
  transition: color 0.3s, transform 0.3s, filter 0.3s, box-shadow 0.3s;
}

.select:hover {
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateZ(10px);
  border-radius: 50%;
  background: linear-gradient(to right, transparent 1%, #686868 15% 85%, transparent 99%);
}

.el {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 1rem;
}

.option {
  height: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  top: 100%;
  right: 8%;
}

.header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 10px 5vw; /* Адаптивные отступы */
  background-color: #191919;
}

.first {
  margin-right: 3vw; /* Адаптивный отступ */
}

.first a {
  text-decoration: none;
  color: #ffffff;
  font-size: 2vw; /* Адаптивный размер текста */
  padding: 0px 1vw;
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
  flex-wrap: wrap; /* Для адаптации */
}

.links div {
  height: 70px;
  border-radius: 50%;
}

.links a {
  height: auto;
  text-decoration: none;
  color: #ffffff;
  font-size: 1rem;
  padding: 1rem;
  position: relative;
  display: inline-block;
  transition: color 0.3s, transform 0.3s, filter 0.3s, box-shadow 0.3s;
}

.links a:hover {
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateZ(10px);
  border-radius: 50%;
  background: radial-gradient(#686868 15%, transparent 70%);
}

@media (max-width: 768px) {
  .header {
    padding: 10px 3vw;
  }

  .first a {
    font-size: 4vw; /* Увеличение для мобильных устройств */
  }

  .first_num {
    font-size: 5vw;
  }

  .links {
    flex-direction: column;
    align-items: flex-start;
  }

  .links a {
    font-size: 4vw;
  }
}
</style> -->

