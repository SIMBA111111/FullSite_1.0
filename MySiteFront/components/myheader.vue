<template>
  <div class="header">
    <div class="first">
      <NuxtLink to="/" exact-active-class="active">Название</NuxtLink>
    </div>
    <div class="links">
      <div v-if="authed"><NuxtLink to="/articles/create" exact-active-class="active" class="el write">Написать</NuxtLink></div>
      <div><NuxtLink to="/articles" exact-active-class="active" class="el">Статьи</NuxtLink></div>
      <div><NuxtLink to="/vacancies" exact-active-class="active" class="el">Вакансии</NuxtLink></div>
      <div><NuxtLink to="/authors" exact-active-class="active" class="el">Авторы</NuxtLink></div>
      <div v-if="!authed"><NuxtLink to="/auth/register" exact-active-class="active" class="el">Регистрация</NuxtLink></div>
      <div v-if="!authed"><NuxtLink to="/auth/login" exact-active-class="active" class="el">Войти</NuxtLink></div>
      <div v-else @click="logout"><NuxtLink to="/" exact-active-class="active" class="el">Выйти</NuxtLink></div>
    </div>
  </div>
  <hr>
</template>

<script setup>
import axios from 'axios';
import { ref, watch } from 'vue';
import { useCookie, useRouter } from '#app';
import { url } from "../MyConstants.vue";

// Реактивное состояние для аутентификации
const authed = ref(false);

// Функция для проверки аутентификации
const checkAuth = () => {
  const token = useCookie('access_token').value;
  authed.value = !!token; // Преобразование в boolean
};

const logout_url = `${url}/auth/logout`;
const logout = async () => {
  try {
    // Получение токена из куки
    const access_token = useCookie('access_token').value;

    // Выполнение DELETE запроса на сервер
    const response = await axios.delete(logout_url, {
      headers: {
        'access-token': access_token,
        'Authorization': access_token // Используйте правильное название заголовка
         // Используйте правильное название заголовка
      }
    });

    // Удаление токена
    useCookie('access_token').value = null;

    // Обновление состояния аутентификации
    checkAuth();

    // Переход на другую страницу
    const router = useRouter();
    await router.push('/'); // Переход на главную страницу или другую по вашему выбору
    location.reload();

  } catch (error) {
    // Обработка ошибок
    console.error('Error:', error);
  }
};

// Инициализация аутентификации при загрузке компонента
checkAuth();

// Отслеживание изменений в состоянии аутентификации
watch(authed, (newValue) => {});
</script>

<style scoped>
*{
  box-sizing: border-box;
}

.el {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0px 70px;
  background-color: #462887;
  overflow: hidden;
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
}

.links div {
  /* margin: 0 10px; */
  height: 70px;
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
  background: rgba(0, 0, 0, 0.5);
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
  border-bottom: 4px solid #c5b02b
}

.links a:active {
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateZ(5px);
  border-bottom: 4px solid #c5b02b
}

/* Стиль для активной ссылки */
.links a.active {
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateZ(10px);
  border-bottom: 4px solid #c5b02b
}
</style>
