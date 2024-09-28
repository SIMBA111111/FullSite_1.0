<template>
    <div>
        <myheader></myheader>   
        <div class="vac">
          <p>Вакансии</p>
          <p>SOON</p>
        </div>
    </div>
</template>
  
<script>
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
    padding-top: 1.3vw;
  }

  p{
    color: #fff;
    font-size: 7vw;
    margin: 3vw 0;
  }
</style>