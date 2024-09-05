<template>
  <div>
  <myheader></myheader>
    <div class="register-container">
      <div class="register-form">
        <input v-model="userData.username" type="text" placeholder="Username" />
        <input v-model="userData.password" type="password" placeholder="Password" />
        <input v-model="userData.first_name" type="text" placeholder="First Name" />
        <input v-model="userData.last_name" type="text" placeholder="Last Name" />
        <input v-model="userData.email" type="email" placeholder="Email" />
        <button @click="register">Зарегистрироваться</button>
        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </div>
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
    password: '',
    first_name: '',
    last_name: '',
    email: ''
  });
  
  const register_url = `${url}/auth/register`;
  const error = ref('');
  
  const register = async () => {
    try {
      error.value = ''; // Clear previous error
      const response = await axios.post(register_url, userData.value);
      // console.log('Response data:', response.data);
      // Redirect to login or other page after successful registration
      location.reload()
    } catch (err) {
      error.value = 'Registration failed. Please check your details and try again.';
      console.error('Error:', err);
    }
  };
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 81vh;
    background-color: #d8cef1;
  }
  
  .register-form {
    background-color: #462887;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(221, 22, 239, 0.5);
    width: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .register-form h2 {
    margin-bottom: 1rem;
  }
  
  .register-form input {
    width: 100%;
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .register-form input:hover {
    box-shadow: 0 0 10px 7px rgba(221, 22, 239, 0.5);
  }

  
  .register-form input:focus {
    box-shadow: 0 0 10px 7px rgba(221, 22, 239, 1);
    outline: none;
  }

  .register-form button {
    padding: 0.5rem 1rem;
    background-color: #c5b02b;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .register-form button:hover {
    background-color: #80700e;
  }
  
  .error {
    color: red;
    margin-top: 1rem;
  }
  </style>
  