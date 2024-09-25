<template>
    <div class="pagination-controls-2">
      <button @click="getLastPage" :disabled="nowPageVariable == 1" class="arrow left"></button>
      <div @click="getLastPage" v-show="lastPageVariable" class="num"> {{ lastPageVariable }} </div>
      <div class="num"> {{nowPageVariable}} </div>
      <div @click="getNextPage" v-show="hasMorePages" class="num"> {{nextPageVariable}} </div>
      <button @click="getNextPage" :disabled="!hasMorePages" class="arrow right"></button>
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
    
    if (data.length < 6) {
      hasMorePages.value = false;
    } else {
      hasMorePages.value = true;
    }

    if (!dataNext.length) {
      hasMorePages.value = false;
    }

    articles.value = data;
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