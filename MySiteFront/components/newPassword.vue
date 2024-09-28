<template>
      <div class="login-container">
        <form @submit.prevent class="login-form" action="">
          <password-field v-model="newPasswordStorage.password"/>
          <repeatPasswordField v-model="newPasswordStorage.repeatPassword" :userPassword="newPasswordStorage.password"/>
          <div class="btn-wrapper">
            <button :disabled="isSignupButtonDisabled" @click="newPassButtonPressed" type="submit" class="btn">Новый пароль</button>
          </div>
        </form>
        <div style="color: red;font-size: 30px;">{{ error }}</div>
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

  const props = defineProps({
    emailProp: {
        type: String,
        required: true
    }
  })

  const newPasswordStorage = reactive({
    email: props.emailProp,
    password: '',
    repeatPassword: ''
  });


  const { errors } = useFormValidation();
  const { isSignupButtonDisabled } = useSubmitButtonState(newPasswordStorage, errors);
  
  let error = ref('');
  const recover_url = `${url}/options/reset-password`;
  const sendCode_url = `${url}/options/check-code`;
  const newPass_url = `${url}/options/new-password`;


  const newPassButtonPressed = async () => {
    const newPassword = reactive({
      new_password: newPasswordStorage.password,
      email: newPasswordStorage.email
    })
    try {
      error.value = '';
      const response = await axios.post(newPass_url, newPassword);
      const router = useRouter();
      await router.push('/auth/login');
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
  