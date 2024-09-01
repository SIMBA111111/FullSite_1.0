<template>
    <div>
        <h1>TEST</h1>
        
        <div><NuxtLink to="/">index</NuxtLink></div> 
        <button @click="test">test</button>

    </div>
    </template>
    
<script setup>
import {url} from "../MyConstants.vue";
import axios from 'axios';

const test_url = `${url}/auth/test`

const access_token = useCookie("access_token").value


const test = () => {
  axios.get(test_url, {
    headers: {
      'Authorization': `${access_token}`
    }
  })
    .then(response => {
      console.log('Response data:', response.data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
</script>
    
<style>
</style>