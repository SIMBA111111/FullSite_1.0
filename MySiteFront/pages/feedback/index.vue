<template>
    <div>
        <myheader></myheader>   
        <div class="vac">
          <div class="hr"></div>
          <form @submit.prevent class="login-form" action="">
            <email-field v-model="user.email"/>
            <message-field v-model="user.message"/>
            <div class="btn-wrapper">
             <button @click="feedbackButtonPressed" type="submit" class="btn">Отправить</button>
            </div>
            </form>
            <div style="color: rgb(0, 255, 119);font-size: 30px;">{{ seccessfully }}</div>
        </div>
    </div>
</template>
  
<script setup>
import emailField from '../../components/emailField.vue';
import MessageField from '../../components/messageField.vue';
import useFormValidation from '~/modules/useFormValidation';
import useSubmitButtonState from '~/modules/useSubmitButtonState'
import { url } from "../../MyConstants.vue";
import axios from 'axios';





definePageMeta({
  middleware: 'auth'
});

const user = reactive({
  email: '',
  message: ''
});

const { errors } = useFormValidation();
const feedback_url = `${url}/options/feedback`;
let seccessfully = ref('');


const feedbackButtonPressed = async () => {
  try {
    seccessfully.value = '';
    console.log("user.value - ", user);
    
    const response = await axios.post(feedback_url, user);
    console.log(response.data);

    const access_token = useCookie('access_token');
    access_token.value = response.data.access_token;
    console.log(response);
    // user.email = '';
    // user.message = '';
    seccessfully.value = 'Сообщенине отослано'
    
    // const router = useRouter();
    // await router.push('/');
    location.reload();
  } catch (err) {
    // error.value = 'Login failed. Please check your credentials and try again.';
    console.error('Error:', error);
  }
};

</script>

<style scoped>
  .vac {
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
    border-radius: 0%;
    background-color: #fff;
    margin-bottom: 40px;
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

.btn {
  width: 273px;
  height: 70px;
  background-color: #909090;
  color: #fff;
  font-size: 32px;
  border-radius: 50px;
  border: none;
  cursor: pointer;
}

.btn:hover {
  background-color: #191919;
  border: 3px solid yellow;
}
</style>