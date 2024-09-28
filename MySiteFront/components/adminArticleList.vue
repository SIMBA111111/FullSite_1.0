<template>
    <div class="articles-list-container">
      <div class="articles-list">
        <adminArticle
          v-for="article in articles"
          :key="article.id"
          :user="article.user"
          :date="article.date"
          :name="article.name"
          :title="article.title"
          :slug="article.slug"
          :count_views="article.count_views"
        />
      </div>
  
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1">Предыдущая</button>
        <span>Страница {{ currentPage }}</span>
        <button @click="nextPage" :disabled="!hasMorePages">Следующая</button>
      </div>
    </div>
  </template>

<script setup>
import { ref } from 'vue';
import article from './adminArticle.vue';
import { url } from "../MyConstants.vue";
import axios from 'axios';

const currentPage = ref(1);
const articles = ref([]);
const hasMorePages = ref(true);

const get_articles_with_authors_url = (page) => `${url}/admin/get-all-articles?page=${page}`;

const get_articles_with_authors = async (page) => {
  try {
    const response = await axios.get(get_articles_with_authors_url(page), {
      headers: {
        "Authorization": useCookie("access_token").value
      }
    });

    if (response.data.length === 0) {
      hasMorePages.value = false;
    } else {
      hasMorePages.value = true;
      articles.value = response.data;
    }
  } catch (error) {
    console.error('Error:', error);
  }
};

const nextPage = () => {
  if (hasMorePages.value) {
    currentPage.value += 1;
    get_articles_with_authors(currentPage.value);
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1;
    get_articles_with_authors(currentPage.value);
  }
};

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
  /* gap: 16px; */
  gap: 2vw;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 4vw;
}

.pagination-controls button {
  padding: 2vw 4vw;
  margin: 0 2vw;
  background-color: #462887;
  color: white;
  border: none;
  border-radius: .7vw;
  cursor: pointer;
  font-size: 2vw;
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