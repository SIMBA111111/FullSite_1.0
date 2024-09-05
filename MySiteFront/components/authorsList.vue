<template>
  <div class="author-list-container">
    <div class="authors-list">
        <Author
        v-for="author in authors" 
        :key="author.id"
        :id="author.id"
        :username="author.username"
        :last_name="author.last_name"
        :first_name="author.first_name"
        :email="author.email">
        </Author>
    </div>
  </div>
  </template>

<script setup>
import { ref } from 'vue';
import article from './article.vue';
import {url} from "../MyConstants.vue";
import axios from 'axios';

const authors = ref();

const get_authors_url = `${url}/users/get-all-authors`


const get_authors = () => {
  axios.get(get_authors_url, 
  )
    .then(response => {
      console.log('Response data:', response.data);
      authors.value = response.data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

get_authors()
console.log("authors", - authors);
</script>

<style scoped>


.author-list-container {
  display: flex;
  flex-direction: column;
  height: 100%;
} 

.authors-list {
  display: grid;
  flex-wrap: wrap;
  gap: 16px;
}


</style>