<template>
  <myheader></myheader>
  <div class="login-container">
    <div class="login-form">
      <input v-model="userData.username" type="text" placeholder="Username" />
      <input v-model="userData.password" type="password" placeholder="Password" />
      <button @click="login">Войти</button>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { url } from "../../MyConstants.vue";

const userData = ref({
  username: '',
  password: ''
});

const login_url = `${url}/auth/login`;
const error = ref('');

const login = async () => {
  try {
    error.value = ''; // Clear previous error
    const response = await axios.post(login_url, userData.value);
    const access_token = useCookie('access_token');
    access_token.value = response.data.access_token;
    const router = useRouter();
    await router.push('/');
    location.reload();
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
