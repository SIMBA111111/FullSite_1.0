<template>
  <myheader></myheader>
  <div class="login-container">
    <div class="login-form">
      <input v-model="userData.username" type="text" placeholder="Username" />
      <input v-model="userData.password" type="password" placeholder="Password" />
      <button @click="login">Войти</button>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
    <input v-model="resetData.username" type="code" placeholder="username" />
    <input v-model="resetData.email" type="email" placeholder="email" />
    <button @click="reset_password">Восстановить пароль</button>
    <br>
    <input v-model="codeData.code" type="code" placeholder="код" />
    <input v-model="codeData.username" type="username" placeholder="username" />
    <input v-model="codeData.email" type="email" placeholder="email" />
    <button @click="check_code">проверить код</button>
    <br>
    <input v-model="new_pwd.new_password" type="code" placeholder="новый пароль" />
    <input v-model="new_pwd.email" type="code" placeholder="email" />
    <button @click="new_pwd_func">заменить пароль</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { url } from "../../MyConstants.vue";

definePageMeta({
    middleware: 'auth'
});

const userData = ref({
  username: '',
  password: ''
});

const codeData = ref({
  code: '',
  username: '',
  email: ''
})
const new_pwd = ref({
  new_password: '',   
  email: ''
})
const resetData = ref({
  username: '',
  email: ''
})

const login_url = `${url}/auth/login`;
const reset_password_url = `${url}/options/reset-password`;
const check_code_url = `${url}/options/check-code`;
const new_pwd_url = `${url}/options/new-password`;
const error = ref('');

const login = async () => {
  try {
    error.value = '';
    const response = await axios.post(login_url, userData.value);
    const access_token = useCookie('access_token');
    access_token.value = response.data.access_token;
    console.log(response);
    
    const router = useRouter();
    await router.push('/');
    location.reload();
  } catch (err) {
    error.value = 'Login failed. Please check your credentials and try again.';
    console.error('Error:', err);
  }
};


const reset_password = async () => {
  try {
    // const resetData = {
    //   "username": "admin",
    //   "email": "naaro2930@gmail.com"
    // }
    const response = await axios.post(reset_password_url, resetData.value);
    // const access_token = useCookie('access_token');
    // access_token.value = response.data.access_token;
    console.log(response);
    
    // const router = useRouter();
    // await router.push('/');
    // location.reload();
  } catch (err) {
    error.value = 'Login failed. Please check your credentials and try again.';
    console.error('Error:', err);
  }
};


const check_code = async () => {
  try {
    const response = await axios.post(check_code_url, codeData.value);
    // const access_token = useCookie('access_token');
    // access_token.value = response.data.access_token;
    console.log(response);
    
    // const router = useRouter();
    // await router.push('/');
    // location.reload();
  } catch (err) {
    error.value = 'Login failed. Please check your credentials and try again.';
    console.error('Error:', err);
  }
};


const new_pwd_func = async () => {
  try {
    const response = await axios.post(new_pwd_url, new_pwd.value);
    // const access_token = useCookie('access_token');
    // access_token.value = response.data.access_token;
    console.log(response);
    
    // const router = useRouter();
    // await router.push('/');
    // location.reload();
  } catch (err) {
    error.value = 'Login failed. Please check your credentials and try again.';
    console.error('Error:', err);
  }
};


</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 81vh;
  background-color: #d8cef1;
}

.login-form {
  background-color: #462887;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(221, 22, 239, 0.5);
  width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-form h2 {
  margin-bottom: 1rem;
}

.login-form input {
  width: 100%;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.login-form input:hover {
  box-shadow: 0 0 10px 7px rgba(221, 22, 239, .5);
}

.login-form input:focus {
  box-shadow: 0 0 10px 10px rgba(221, 22, 239, 1);
  outline: none;
}

.login-form button {
  padding: 0.5rem 1rem;
  background-color: #c5b02b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-form button:hover {
  background-color: #80700e;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
