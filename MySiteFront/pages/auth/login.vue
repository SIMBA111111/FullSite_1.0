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
// }

const logUpButtonPressed = async () => {
  try {
    error.value = '';

    const response = await axios.post(login_url, user);

    const access_token = useCookie('access_token');
    access_token.value = response.data.access_token;

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

.btn-wrapper {
  display: flex;
  gap: 1vw;
}
.btn-wrapper button {
  width:19vw;
  height: 6.5vw;
  background-color: #909090;
  color: #fff;
  font-size: 2.5vw;
  border-radius: 6vw;
  border: none;
}

.btn-wrapper button:hover {
  background-color: #191919;
}

.btn-wrapper button:disabled:hover {
  background-color: #909090;
}

.btn {
  width: 27vw;
  height: 7vw;
  background-color: #909090;
  color: #fff;
  font-size: 3.5vw;
  border-radius: 4vw;
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
  border: .3vw solid yellow;
}

.btn-rec {
  text-decoration: none;
  color: #fff;
}

.btn-sign-up {
  background-color: transparent;
  border: none;
  font-size: 3vw;
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
