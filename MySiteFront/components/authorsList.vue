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

        <!-- <Author
        v-for="author in authors" 
        :key="author.email"
        :authorObj="authorO"
        /> -->
    </div>
    <!-- <button @click="f"></button> -->
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




.authors-list {
  display: grid;
  grid-template-columns: repeat(2, 380px);
  /* grid-template-columns: 380px, 380px; */

  /* grid-template-rows: 246px 245px; */
  grid-template-rows: repeat(3, 245px);
  gap: 10px;
}


</style>