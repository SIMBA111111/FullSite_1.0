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
  padding-top: 3vw;
}

.login-form {
  background-color: transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2.5vw;
}

.login-form button {
  cursor: pointer;
}
/* 
.btn {
  width: 27vw;
  height: 7vw;
  background-color: #909090;
  color: #fff;
  font-size: 3.5vw;
  border-radius: 4vw;
  border: none;
} */

.btn-wrapper button {
  width: 40vw;
  height: 8vw;
  background-color: #909090;
  color: #fff;
  font-size: 3.5vw;
  border-radius: 6vw;
  border: none;
}

.btn-wrapper button:hover {
  background-color: #191919;
}

.btn-wrapper button:disabled:hover {
  background-color: #909090;
}

.btn:disabled {
  opacity: .3;
  cursor: default;
}

.btn:hover {
  background-color: #191919;
  border: .3vw solid yellow;
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
