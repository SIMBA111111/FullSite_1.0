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

    <!-- <pagination/> -->

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
import { ref, defineProps, watch } from 'vue';
import Article from './article.vue';
import { url } from "../MyConstants.vue";
import axios from 'axios';

const props = defineProps({
  urlLink: {
    type: String,
    required: true
  },
  query: {
    type: String
  }
});

const articles = ref([]);
const hasMorePages = ref(false);

const get_articles_with_authors_url = (page) => `${props.urlLink}${page}`;
const get_articles_with_authors_url_next = (pageNext) => `${props.urlLink}${pageNext}`;


const get_articles_with_authors = async (page, pageNext) => {
  try {
    if (!props.urlLink) {
      return
    }
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
  get_search_articles_with_authors(nowPageVariable.value, nextPageVariable.value, props.query)
  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value)
}

const getNextPage = () => {
  lastPageVariable.value++
  nowPageVariable.value++
  nextPageVariable.value++
  get_search_articles_with_authors(nowPageVariable.value, nextPageVariable.value, props.query)
  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value)
}





  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value);


// --------------------------------------------------

const get_search_articles_with_authors_url = (page, query) => `${url}/articles/request-articles?article_title=${query}&page=${page}`;
const get_search_articles_with_authors_url_next = (pageNext, query) => `${url}/articles/request-articles?article_title=${query}&page=${pageNext}`;

const get_search_articles_with_authors = async (page, pageNext, query) => {
  try {
    const { data } = await axios(get_search_articles_with_authors_url(page, query), {
      headers: {
        "Authorization": useCookie("access_token").value
      }
    });
    const { data : dataNext } = await axios(get_search_articles_with_authors_url_next(pageNext, query), {
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

    if (!props.query) {
      articles.value.length = 0
    } else {
      articles.value = data;
    }

  } catch (error) {
    console.error('Error:', error);
  }
};





watch(()=>props.query, () => get_search_articles_with_authors(nowPageVariable.value, nextPageVariable.value, props.query))
</script>

<style scoped>
.articles-list-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.articles-list {
  height: 100%; 
  display: grid;
  /* grid-template-columns: repeat(2, 380px); */
  grid-template-columns: repeat(2, 31.5vw);
  /* grid-template-rows: repeat(3, 245px); */
  grid-template-rows: repeat(3, 20.2vw);
  /* gap: 10px; */
  gap: .9vw;
  /* margin-bottom: 20px; */
  margin-bottom: 1.6vw;
}

.pagination-controls-2 {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  /* margin-top: 20px; */
  margin-top: .8vw;
  /* gap: 8px; */
  gap: .4vw;
}

.arrow{
  /* width: 100px; */
  width: 4vw;
  /* height: 20px; */
  height: .8vw;
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
  /* font-size: 29px; */
  font-size: 1.3vw;
  /* padding: 2px; */
  padding: .1vw;
  color: #9d9d9d;
}

.num:hover {
  color: #fff;
}

.num:nth-child(3n) {
  /* font-size: 39px; */
  font-size: 1.6vw;
}

@media (max-width: 425px) {

  .arrow {
    width: 10vw;
    height: 3vw;
  }

  .num {
    font-size: 5vw;
  }

  .num:nth-child(3n) {
  /* font-size: 39px; */
  font-size: 3vw;
  }
}

</style>
