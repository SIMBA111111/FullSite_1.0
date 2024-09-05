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

    <!-- Пагинация -->
    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1">Предыдущая</button>
      <span>Страница {{ currentPage }}</span>
      <button @click="nextPage">Следующая</button>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import article from './article.vue';
import {url} from "../MyConstants.vue";
import axios from 'axios';

const currentPage = ref(1);
const articles = ref([]);

const get_articles_with_authors_url = (page) => `${url}/articles/get-all-articles?page=${page}`;

const get_articles_with_authors = (page) => {
  axios.get(get_articles_with_authors_url(page), 
  {
    headers: {
      "Authorization": useCookie("access_token").value
    }
  })
    .then(response => {
      console.log('Response data:', response.data);
      articles.value = response.data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
};

// Переход на следующую страницу
const nextPage = () => {
  currentPage.value += 1;
  get_articles_with_authors(currentPage.value);
};

// Переход на предыдущую страницу
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1;
    get_articles_with_authors(currentPage.value);
  }
};

// Изначально загружаем статьи первой страницы
get_articles_with_authors(currentPage.value);
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

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-controls button {
  padding: 10px 20px;
  margin: 0 10px;
  background-color: #462887;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination-controls button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination-controls button:hover:not(:disabled) {
  background-color: #3a1a6b;
}

</style>