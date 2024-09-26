<template>
      <div class="login-container">
        <form v-if="!succes" @submit.prevent class="login-form" action="">
          <code-field  v-model="code.code"/>
          <div class="btn-wrapper">
            <button :disabled="isSignupButtonDisabled" @click="sendButtonPressed" type="submit" class="btn">Ввести код</button>
          </div>
        </form>
        <new-password v-if="succes" :emailProp="emailProp"/>
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
  import codeField from '../components/codeField.vue'
  
  import useFormValidation from '~/modules/useFormValidation';
  import useSubmitButtonState from '~/modules/useSubmitButtonState'

  import newPassword from '../../components/newPassword.vue'

  
  const props = defineProps({
    userEmail: {
        type: String,
        required: true
    }
  })
  
  console.log('PROPS', props.userEmail);

  const code = reactive({
    email: props.userEmail,
    code: ''
  });

  const emailProp = ref(null);
  const succes = ref(false);


  const { errors } = useFormValidation();
  const { isSignupButtonDisabled } = useSubmitButtonState(code, errors);
  
  let error = ref('');
  const sendCode_url = `${url}/options/check-code`;
 
  const sendButtonPressed = async () => {
    emailProp.value = code.email;
    try {
      
      console.log(code);     
      error.value = '';
      const response = await axios.post(sendCode_url, code);
      console.log('res code', response);
      if (response.status == 200) {
        succes.value = true;
      }
      // const router = useRouter();
      // await router.push('/');
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
    justify-content: center;
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
  