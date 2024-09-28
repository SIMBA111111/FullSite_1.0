<template>
    <div class="header">
      <div class="first">
        <NuxtLink to="/admin/bidList" exact-active-class="active">АдминПанель</NuxtLink>
      </div>
      <div class="links">
        <div><NuxtLink to="/admin/bidList" exact-active-class="active" class="el write">Заявки</NuxtLink></div>
        <div><NuxtLink to="/admin/adminArticles" exact-active-class="active" class="el write">Статьи</NuxtLink></div>
        <div><NuxtLink to="/admin/adminUsers" exact-active-class="active" class="el write">Юзеры</NuxtLink></div>
        <!-- <div v-else @click="logout" class="el">Выйти</div> -->
      </div>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { ref, watch } from 'vue';
  import { useCookie, useRouter } from '#app';
  import { url } from "../MyConstants.vue";
  // Реактивное состояние для аутентификации
//   const authed = ref(false);
  
  // Функция для проверки аутентификации
//   const checkAuth = () => {
    // const token = useCookie('access_token').value;
    // authed.value = !!token; // Преобразование в boolean
//   };
  
//   const logout_url = `${url}/auth/logout`;
//   const logout = async () => {
//     try {
//       // Получение токена из куки
//       const access_token = useCookie('access_token').value;
  
//       // Выполнение DELETE запроса на сервер
//       const response = await axios.delete(logout_url, {
//         headers: {
//           'access-token': access_token // Используйте правильное название заголовка
//         }
//       });
  
//       // Удаление токена
//       useCookie('access_token').value = null;
  
//       // Обновление состояния аутентификации
//       checkAuth();
  
//       // Переход на другую страницу
//       const router = useRouter();
//       await router.push('/'); // Переход на главную страницу или другую по вашему выбору
//       location.reload();
  
//     } catch (error) {
//       // Обработка ошибок
//       console.error('Error:', error);
//     }
//   };
  
//   // Инициализация аутентификации при загрузке компонента
//   checkAuth();
  
//   // Отслеживание изменений в состоянии аутентификации
//   watch(authed, (newValue) => {});
  </script>
  
  <style scoped>
  .el {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: .6vw 1vw;
    background-color: #fff;
  }
  
  .first {
    margin-right: 2vw;
  }
  
  .first a {
    text-decoration: none;
    color: #333;
    font-size: 2.5vw;
    padding: .6vw 1vw;
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
  }
  
  .links div {
    margin: 0.4vw;
  }
  
  .links a {
    text-decoration: none;
    color: #333;
    font-size: 2vw;
    padding: .6vw .8vw;
    border: 1px solid transparent;
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
    background: rgba(240, 240, 240, 0.5);
    z-index: -1;
    transition: transform 0.3s, filter 0.3s;
    transform: scale(1);
    filter: blur(0);
  }
  
  .links a:active::before {
    transform: scale(1);
  }
  
  .links a:hover {
    color: #000;
    box-shadow: 0 .2vw .4vw rgba(0, 0, 0, 0.2);
    transform: translateZ(1vw);
  }
  
  .links a:active {
    color: #555;
    box-shadow: 0 .2vw .4vw rgba(0, 0, 0, 0.2);
    transform: translateZ(.5vw);
  }
  
  /* Стиль для активной ссылки */
  .links a.active {
    color: #000;
    box-shadow: 0 .2vw .4vw rgba(0, 0, 0, 0.2);
    transform: translateZ(1vw);
  }
  </style>
  