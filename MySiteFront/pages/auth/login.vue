<template>
  <div>
    <myheader></myheader>
    <div class="login-container">
      <form ref="form" @submit.prevent class="login-form" action="">
        <username-field v-model="user.username"/>
        <password-field v-model="user.password"/>
        <div class="btn-wrapper">
          <button :disabled="isSignupButtonDisabled" @click="logUpButtonPressed" type="submit" class="btn">ВХОД</button>
          <button class="btn"><NuxtLink class="btn-rec" to="/recoverPassword">ЗАБЫЛ ПАРОЛЬ</NuxtLink></button>
        </div>
        <div class="btn-sign-up" @click="login"><NuxtLink to="/auth/register">Зарегистрироваться</NuxtLink></div>
      </form>
      <div style="color: red;font-size: 30px;">{{ error }}</div>
    </div>
    <!-- <notification
      v-if="notificationMessage"
      :notificationMessage="notificationMessage"
    /> -->
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
import Notification from '../../components/notification.vue';

import useFormValidation from '~/modules/useFormValidation';
import useSubmitButtonState from '~/modules/useSubmitButtonState'


definePageMeta({
  middleware: 'auth'
});

const user = reactive({
  username: '',
  password: ''
});

// const succes = ref();

const notificationMessage = ref('');

const resetData = reactive({
  username: "",
  email: ""
});

const codeData = reactive({
  code: "",
  username: "",
  email: ""
});

const new_pwd = reactive({
  new_password: "",
  email: ""
});

const { errors } = useFormValidation();
const { isSignupButtonDisabled } = useSubmitButtonState(user, errors);

let error = ref('');
const login_url = `${url}/auth/login`;

// const signUpButtonPressed = () => {
//   console.log(user);
// }

const logUpButtonPressed = async () => {
  try {
    error.value = '';
    console.log("user.value - ", user);
    
    const response = await axios.post(login_url, user);
    console.log(response.data);

    const access_token = useCookie('access_token');
    access_token.value = response.data.access_token;
    console.log(response);
    if (response.status == 200) {

      notificationMessage.value = 'Вы вошли'
      setTimeout(() => {
        notificationMessage.value = '';
        // location.reload();
      }, 3000)
    }
    
    const router = useRouter();
    await router.push('/');
    // location.reload();
  } catch (err) {
    error.value = 'Login failed. Please check your credentials and try again.';
    console.error('Error:', error);
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
  justify-content: space-between;
}

.btn-wrapper button {
  width: 273px;
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

.btn:disabled:hover {
  border: none;
}


.btn:hover {
  background-color: #191919;
  border: 3px solid yellow;
}

.btn-rec {
  text-decoration: none;
  color: #fff;
}

.btn-sign-up {
  background-color: transparent;
  border: none;
  font-size: 33px;
  cursor: pointer;
}
.btn-sign-up a {
  text-decoration: none;
  color: #fff;
}


.btn-sign-up a:hover {
  color: #747474;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
