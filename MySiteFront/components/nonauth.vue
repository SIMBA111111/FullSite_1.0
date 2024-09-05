<template>
  <div class="unauthorized-container">
    <NuxtLink class="unauthorized-message" to="/auth/login">Необходимо авторизоваться</NuxtLink>
  </div>
</template>
  
<style>
  .unauthorized-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 81vh;
    background-color: #d8cef1;
  }
  
  .unauthorized-message {
    background-color: #462887;
    color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(221, 22, 239, 0.5);
    text-align: center;
    font-size: 1.2rem;
    width: 300px;
    text-decoration: none;
  }
  
  .unauthorized-message:hover {
    box-shadow: 0 0 10px 7px rgba(221, 22, 239, .5);
  }
  
  .unauthorized-message:focus {
    outline: none;
    box-shadow: 0 0 10px 10px rgba(221, 22, 239, 1);
  }
</style>
  