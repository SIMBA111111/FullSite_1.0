<template>
    <div>
        <myheader></myheader>
        <div class="main-container">
          <articlesList :url-link="urlLink"/>
        </div>
    </div>
</template>
  
<script setup>
import { url } from "../MyConstants.vue";
import articlesList from "../../components/articlesList.vue";

definePageMeta({
  middleware: 'auth'
});

const urlLink = `${url}/articles/get-all-articles?page=`;

</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
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

</style>