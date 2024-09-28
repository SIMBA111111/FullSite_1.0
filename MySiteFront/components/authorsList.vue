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
        :email="author.email"
        :views_count="author.views_count"
        :first_article_date="author.first_article_date"
        />
    </div>

  </div>
  </template>

<script setup>
import { ref, reactive } from 'vue';
import Author from './author.vue';
import {url} from "../MyConstants.vue";
import axios from 'axios';

const authors = ref([]);

const get_authors_url = `${url}/users/get-all-authors`


const get_authors = () => {
  axios.get(get_authors_url, 
  )
    .then(response => {
      authors.value = response.data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

get_authors()
</script>

<style scoped>

.author-list-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}


.authors-list {
  height: 100%; 
  display: grid;
  grid-template-columns: repeat(2, 31.5vw);
  grid-template-rows: repeat(3, 20.2vw);
  gap: .9vw;
  margin-bottom: 1.6vw;
}


</style>