<template>
    <div>
      <myheader></myheader>
      <div class="login-container">
        <form v-if="!userEmail" @submit.prevent class="login-form" action="">
          <email-field v-model="email.email"/>
          <div class="btn-wrapper">
            <button :disabled="isSignupButtonDisabled" @click="recoverButtonPressed" type="submit" class="btn">Отправить</button>            
          </div>
        </form>
        <send-code v-if="userEmail" :userEmail="userEmail" />
        <div style="color: red;font-size: 30px;">{{ error }}</div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed, reactive, ref } from 'vue';
  import axios from 'axios';
  import { url } from "../../MyConstants.vue";
  import UsernameField from '../../components/usernameField.vue';
  import FirstnameField from '../../components/firstnameField.vue';
  import LastnameField from '../../components/lastnameField.vue';
  import EmailField from '../../components/emailField.vue';
  import PasswordField from '../../components/passwordField.vue';
  
  import useFormValidation from '~/modules/useFormValidation';
  import useSubmitButtonState from '~/modules/useSubmitButtonState'

  import sendCode from '../../components/sendCode.vue'
  import newPassword from '../../components/newPassword.vue'

  
  
  definePageMeta({
    middleware: 'auth'
  });
  
  
  const email = reactive({
    email: ''
  });
  const userEmail = ref(null);
  const succes = ref(false);
  
  const { errors } = useFormValidation();
  const { isSignupButtonDisabled } = useSubmitButtonState(email, errors);
  
  let error = ref('');
  const recover_url = `${url}/options/reset-password`;
  
  const recoverButtonPressed = async () => {
    userEmail.value = email.email;

    try {
      error.value = '';
      // const response = await axios.post(recover_url, email.value);
      const response = await axios.post(recover_url, email.email, {
        headers: {
          'Content-Type': 'application/json'
        }});
      if (response.status == 200) {
        succes.value = true;
      }
      // const router = useRouter();
      // await router.push('/');
      // location.reload();
    } catch (err) {
      error.value = 'Login failed. Please check your credentials and try again.';
      console.error('Error:', err);
    }
  };
  
  // const userEmailFunc = computed(() => {
  //   return userEmail
  // })
  
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
  
/* .btn-wrapper button {
  width: 40vw;
  height: 8vw;
  background-color: #909090;
  color: #fff;
  font-size: 3.5vw;
  border-radius: 6vw;
  border: none;
} */
.btn-wrapper button:disabled:hover {
  background-color: #909090;
}

.btn {
  width: 21vw;
  height: 5vw;
  background-color: #909090;
  color: #fff;
  font-size: 2.5vw;
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

  
  .error {
    color: red;
    margin-top: 1rem;
  }
  </style>
  