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
    <button @click="f"></button>
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
      console.log('res Au', authors);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

get_authors()
console.log("authors", - authors);



const articles = reactive([]);

const s = () => {
  authors
}


const f = async () => {
  const { data } = await axios.get(`${url}/articles/get-all-articles?page=1`)
  articles.value = data;
  for(let art of articles.value) {
    let name
    console.log(art.name);
  }
  console.log('gdff' , articles.value[0]);
  console.log('gdss' , authors.value);
}




</script>

<style scoped>




.authors-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  flex-wrap: wrap;
  gap: 16px;
}


</style>