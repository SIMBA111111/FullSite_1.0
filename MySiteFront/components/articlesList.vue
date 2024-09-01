<template>
  <div class="articles-list-container">
    <div class="articles-list">
      <Article
        v-for="article in articles"
        :key="article.id"
        :user="article.user"
        :avatar="article.avatar"
        :date="article.date"
        :name="article.name"
        :title="article.title"
        :text="article.text"
        :intro_text="article.intro_text"
        :slug="article.slug"
        :count_views="article.count_views"
      />
    </div>
  </div>
  </template>

<script setup>
import { ref } from 'vue';
import article from './article.vue';
import {url} from "../MyConstants.vue";
import axios from 'axios';


const articles = ref();

const get_articles_with_authors_url = `${url}/articles/get-all-articles`


const get_articles_with_authors = () => {
  axios.get(get_articles_with_authors_url, 
  {
    headers: {
      "Authorization": useCookie("access_token").value
    }
  }
  )
    .then(response => {
      console.log('Response data:', response.data);
      articles.value = response.data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

get_articles_with_authors()
console.log("articles", - articles);
</script>

<style scoped>

.articles-list-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}


.articles-list {
  display: grid;
  flex-wrap: wrap;
  gap: 16px;
}
</style>