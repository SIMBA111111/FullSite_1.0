<template>
  <div>
      <myheader></myheader>   
      <div class="vac">
        <authors-list/>
      </div>
  </div>
</template>

<script>
import authorList from '../../components/authorsList.vue'
// import {url} from "../MyConstants.vue";


// const res = reactive([]);

// onMounted (()=>{
//   res = axios(`${url}/authors/get-all-authors`)
// })

definePageMeta({
middleware: 'auth'
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
p{
  color: #fff;
  font-size: 100px;
  margin: 50px 0;
}
</style>