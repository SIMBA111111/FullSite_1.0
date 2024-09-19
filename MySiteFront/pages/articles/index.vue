<template>
    <div>
        <myheader></myheader>
        <div class="main-container">
          <div class="hr"></div>
          <articlesList/>
        </div>
    </div>
</template>
  
<script>
definePageMeta({
  middleware: 'auth'
});
</script>

<style scoped>
.main-container {
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

</style>