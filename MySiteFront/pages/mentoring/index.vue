<template>
  <div>
    <myheader></myheader>
    <div class="vac">
      <div class="container">
        <svg
          style="color: blue; width: 20vw; height: 18vw"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 496 512"
        >
          <path
            d="M248 8C111 8 0 119 0 256S111 504 248 504 496 393 496 256 385 8 248 8zM363 176.7c-3.7 39.2-19.9 134.4-28.1 178.3-3.5 18.6-10.3 24.8-16.9 25.4-14.4 1.3-25.3-9.5-39.3-18.7-21.8-14.3-34.2-23.2-55.3-37.2-24.5-16.1-8.6-25 5.3-39.5 3.7-3.8 67.1-61.5 68.3-66.7 .2-.7 .3-3.1-1.2-4.4s-3.6-.8-5.1-.5q-3.3 .7-104.6 69.1-14.8 10.2-26.9 9.9c-8.9-.2-25.9-5-38.6-9.1-15.5-5-27.9-7.7-26.8-16.3q.8-6.7 18.5-13.7 108.4-47.2 144.6-62.3c68.9-28.6 83.2-33.6 92.5-33.8 2.1 0 6.6 .5 9.6 2.9a10.5 10.5 0 0 1 3.5 6.7A43.8 43.8 0 0 1 363 176.7z"
            fill="blue"
          ></path>
        </svg>
        <a
          class="tg"
          target="_blank"
          href="https://web.telegram.org/k/#@SIMBA1111"
          >Telegram</a
        >
      </div>
    </div>

  </div>
</template>

<script setup>
import emailField from "../../components/emailField.vue";
import MessageField from "../../components/messageField.vue";
import useFormValidation from "~/modules/useFormValidation";
import useSubmitButtonState from "~/modules/useSubmitButtonState";
import { url } from "../../MyConstants.vue";
import axios from "axios";

definePageMeta({
  middleware: "auth",
});


</script>

<style scoped>
.vac {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  background-color: #191919;
  padding-top: 1.3vw;
}



.container{
  display: flex;
  gap: 3vw;
}
.tg {
  color: #fff;
  font-size: 7vw;
  margin: 4.8vw 0;
  text-decoration: none;
}

.tg:hover {
  color: rgb(141, 0, 143);
}
</style>
