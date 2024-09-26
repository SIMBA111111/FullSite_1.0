<template>
  <div>
    <myheader></myheader>
    <div class="login-container">
      <form @submit.prevent class="login-form" action="">
        <username-field v-model="userStorage.username"/>
        <firstname-field v-model="userStorage.first_name"/>
        <lastname-field v-model="userStorage.last_name"/>
        <email-field v-model="userStorage.email"/>
        <password-field v-model="userStorage.password"/>
        <repeatPasswordField v-model="userStorage.repeatPassword" :userPassword="userStorage.password"/>
        <div class="btn-wrapper">
          <button :disabled="isSignupButtonDisabled" @click="signUpButtonPressed" type="submit" class="btn">Зарегистрироваться</button>
        </div>
      </form>
      <div style="color: red;font-size: 30px;">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import { url } from "../../MyConstants.vue";
import UsernameField from '../../components/usernameField.vue';
import FirstnameField from '../../components/firstnameField.vue';
import LastnameField from '../../components/lastnameField.vue';
import EmailField from '../../components/emailField.vue';
import PasswordField from '../../components/passwordField.vue';
import repeatPasswordField from '~/components/repeatPasswordField.vue';

import useFormValidation from '~/modules/useFormValidation';
import useSubmitButtonState from '~/modules/useSubmitButtonState'


definePageMeta({
  middleware: 'auth'
});

const userStorage = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  repeatPassword: ''
});


const { errors } = useFormValidation();
const { isSignupButtonDisabled } = useSubmitButtonState(userStorage, errors);

let error = ref('');

const register_url = `${url}/auth/register`;

const signUpButtonPressed = async () => {
  const user = reactive({
    username: userStorage.username,
    email: userStorage.email,
    first_name: userStorage.first_name,
    last_name: userStorage.last_name,
    password: userStorage.password
  })
    try {
      error.value = ''; // Clear previous error
      const response = await axios.post(register_url, user);
      if (response.status == 200) {
        const router = useRouter();
        await router.push('/auth/login');
      }

      // Redirect to login or other page after successful registration
      // location.reload()
    } catch (err) {
      error.value = 'Registration failed. Please check your details and try again.';
      console.error('Error:', err);
    }
  };

</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  background-color: #191919;
  padding-top: 20px;
}

.hr {
    width: 90%;
    height: 5px;
    background-color: #fff;
    margin-bottom: 40px;
    padding: 2px;
    clip-path: polygon(60% 0%, 60% 0%, 100% 100%, 0% 100%);
}

.login-form {
  background-color: transparent;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 21px;
}

.login-form button {
  cursor: pointer;
}

.login-form h2 {
  margin-bottom: 1rem;
}

.search {
    width: 560px;
    height: 76px;
    padding: 15px 40px 15px 35px;
    box-sizing: border-box;
    border: 0px;
    border-radius: 50px;
    background-color: #D9D9D9;
    font-size: 1.1rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search::placeholder {
    font-size: 25px;
}

.search:focus { 
    box-shadow: 0 0 8px rgba(70, 40, 135, 0.5);
    border-color: #462887;
    outline: none;
}

.btn-wrapper {
  width: 560px;
  height: 70px;
  display: flex;
  justify-content: center;
}

.btn-wrapper button {
  width: 330px;
  height: 70px;
  background-color: #909090;
  color: #fff;
  font-size: 32px;
  border-radius: 50px;
  border: none;
}

.btn-wrapper button:hover {
  background-color: #191919;
}

.btn-wrapper button:disabled:hover {
  background-color: #909090;
}

.btn {
  width: 273px;
  height: 70px;
  background-color: #909090;
  color: #fff;
  font-size: 32px;
  border-radius: 50px;
  border: none;
}

.btn:disabled {
  opacity: .3;
  cursor: default;
}

.btn:hover {
  background-color: #191919;
  border: 3px solid yellow;
}

.btn:disabled:hover {
  border: none;
}

.btn-logout {
  color: #fff;
  background-color: transparent;
  border: none;
  font-size: 33px;
}

.btn-logout:hover {
  color: #747474;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
