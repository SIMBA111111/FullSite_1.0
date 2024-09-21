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

    <div class="pagination-controls-2">
      <button @click="getLastPage" :disabled="nowPageVariable == 1" class="arrow left"></button>
      <div @click="getLastPage" v-show="lastPageVariable" class="num"> {{ lastPageVariable }} </div>
      <div class="num"> {{nowPageVariable}} </div>
      <div @click="getNextPage" v-show="hasMorePages" class="num"> {{nextPageVariable}} </div>
      <button @click="getNextPage" :disabled="!hasMorePages" class="arrow right"></button>
    </div>
    
  </div>
</template>

<script setup>
import { ref } from 'vue';
import article from './article.vue';
import { url } from "../MyConstants.vue";
import axios from 'axios';

const articles = ref([]);
const hasMorePages = ref(false);

const get_articles_with_authors_url = (page) => `${url}/articles/get-all-articles?page=${page}`;
const get_articles_with_authors_url_next = (pageNext) => `${url}/articles/get-all-articles?page=${pageNext}`;


const get_articles_with_authors = async (page, pageNext) => {
  try {
    const { data } = await axios(get_articles_with_authors_url(page), {
      headers: {
        "Authorization": useCookie("access_token").value
      }
    });
    const { data : dataNext } = await axios(get_articles_with_authors_url_next(pageNext), {
      headers: {
        "Authorization": useCookie("access_token").value
      }
    });

    console.log('Res dataNext', dataNext);
    console.log('Response dataaaa:', data);
  
    if (data.length < 6) {
      hasMorePages.value = false;
    } else {
      hasMorePages.value = true;
    }

    if (!dataNext.length) {
      hasMorePages.value = false;
    }

    articles.value = data;
    console.log('articles', articles);
  } catch (error) {
    console.error('Error:', error);
  }
};

const lastPageVariable = ref('');
const nowPageVariable = ref('1');
const nextPageVariable = ref('2');


const getLastPage = () => {
  lastPageVariable.value--
  nowPageVariable.value--
  nextPageVariable.value--
  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value)
}

const getNextPage = () => {
  lastPageVariable.value++
  nowPageVariable.value++
  nextPageVariable.value++
  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value)
}





get_articles_with_authors(nowPageVariable.value, nextPageVariable.value);
</script>

<style scoped>
.articles-list-container {
  /* border: 1px solid green; */
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.articles-list {
  /* border: 1px solid red; */
  /* width: 130vh;
  height: 130VH; */
  display: grid;
  grid-template-columns: 380px 380px;
  grid-template-rows: 246px 245px;
  gap: 10px;
  /* display: flex;
  justify-content: space-around; */
  /* flex-wrap: wrap; */
  /* gap: 16px; */
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-controls span {
  color: #fff;
  font-size: 14px;
  font-weight: bold;
}

.pagination-controls button {
  padding: 10px 20px;
  margin: 0 10px;
  background-color: #462887;
  color: black;
  font-size: 14px;
  font-weight: bold;
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

.pagination-controls-2 {
  display: flex;
  align-items: center;
  margin: auto;
  gap: 8px;
  position: absolute;
  bottom: 10%;
  left: 36%;
}

.arrow{
  width: 100px;
  height: 20px;
  background-color: #9d9d9d;
}

.arrow:disabled {
  background-color: #191919;
  border: none;
}

.arrow:disabled:hover {
  background-color: #191919;
}

.arrow:hover {
  background-color: #ffffff;
  scale: 1.1;
}

.left {
  clip-path: polygon(100% 0%, 100% 0%, 0% 60%, 100% 100%);
}

.right {
  clip-path: polygon(0% 0%, 0% 0%, 100% 60%, 0% 100%);
}

.num {
  /* border: 1px solid #9d9d9d; */
  font-size: 29px;
  padding: 2px;
  color: #9d9d9d;
}

.num:hover {
  color: #fff;
}

.num:nth-child(3n) {
  font-size: 39px;
}

</style>
