<template>
  <div class="articles-list-container">
    
    <div class="articles-sort-container">
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

      <div v-if="!isSearchPage" class="custom-select" @click="toggleDropdown" @focusout="isOpen = false" tabindex="0">
        <div class="selected">{{ sortLabel }}</div>
        <div class="arrow-down"></div>
        <ul :class="{ 'options': true, 'show': isOpen }" @focusout="isOpen = false">
          <li @click="selectSort('newest')">Новые</li>
          <li @click="selectSort('oldest')">Старые</li>
          <li @click="selectSort('most viewed')">Популярные</li>
        </ul>
      </div>
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
import { ref, defineProps, watch } from 'vue';
import Article from './article.vue';
import { url } from "../MyConstants.vue";
import axios from 'axios';
import { RouterLink } from '~/node_modules/vue-router/dist/vue-router';

const props = defineProps({
  urlLink: {
    type: String,
    required: true
  },
  query: {
    type: String
  }
});

const sort_by = ref("newest")
const articles = ref([]);
const hasMorePages = ref(false);
const sortLabel = ref("Новые");

const get_articles_with_authors_url = (page, sort_by) => `${props.urlLink}${page}&sort_by=${sort_by}`;
const get_articles_with_authors_url_next = (pageNext, sort_by) => `${props.urlLink}${pageNext}&sort_by=${sort_by}`;


const get_articles_with_authors = async (page, pageNext, sort_by) => {
  try {
    if (!props.urlLink) {
      return
    }
    const { data } = await axios(get_articles_with_authors_url(page, sort_by), {
      headers: {
        "Authorization": useCookie("access_token").value
      }
    });
    const { data : dataNext } = await axios(get_articles_with_authors_url_next(pageNext, sort_by), {
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

onMounted(() => {
  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value, sort_by.value);
});

const onSortChange = (event) => {
  sort_by.value = event.target.value;
  lastPageVariable.value = 0;
  nowPageVariable.value = 1;
  nextPageVariable.value = 2;  
  get_articles_with_authors(nowPageVariable.value, nowPageVariable.value+1, sort_by.value);
};

const isOpen = ref(false);

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const selectSort = (value) => {
  sort_by.value = value;
  isOpen.value = false; // Закрыть дропдаун после выбора
  sortLabel.value = value === 'newest' ? 'Новые' : value === 'oldest' ? 'Старые' : 'Популярные';
  onSortChange({ target: { value } }); // Вызов существующей логики сортировки
};

const getLastPage = () => {
  lastPageVariable.value--
  nowPageVariable.value--
  nextPageVariable.value--
  get_search_articles_with_authors(nowPageVariable.value, nextPageVariable.value, props.query, sort_by.value)
  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value, sort_by.value)
}

const getNextPage = () => {
  lastPageVariable.value++
  nowPageVariable.value++
  nextPageVariable.value++
  get_search_articles_with_authors(nowPageVariable.value, nextPageVariable.value, props.query, sort_by.value)
  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value, sort_by.value)
}





  get_articles_with_authors(nowPageVariable.value, nextPageVariable.value, sort_by);


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


const route = useRoute();
console.log("route - ", route.path);

const isSearchPage = computed(() => {
  return route.path === '/search';
});

</script>

<style scoped>
.articles-list-container {
  display: flex;
  flex-direction: column;
  height: 10%;
  position: relative;
  margin-top: 20px;
}

.articles-sort-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  /* margin-bottom: 20px; */
}

.articles-list {

  height: 80%;
  display: grid;
  grid-template-columns: repeat(2, 31.5vw);
  grid-template-rows: repeat(3, 20.2vw);
  gap: .9vw;
  margin-bottom: 1.6vw;
}

.custom-select {
  position: relative;
  display: inline-block;
  margin-left: 20px;
  width: 150px;
}

.arrow-down {
  position: absolute;
  top: 50%;
  right: 10px; /* Позиция стрелки по горизонтали */
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid white; /* Цвет стрелки */
  transform: translateY(-50%); /* Центрирование по вертикали */
  pointer-events: none; /* Чтобы стрелка не мешала кликам */
}

.selected {
  padding: 10px 0px;
  font-size: 14px;
  font-weight: bold;
  background-color: #462887;
  color: rgb(0, 0, 0);
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.selected:hover {
  background-color: #685f5f;
}

.options {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: #9d9d9d;
  border-radius: 4px;
  z-index: 1;
  list-style: none;
  padding: 0;
  margin: 0;
  display: none;
}

.options.show {
  display: block;
}

.options li {
  padding: 10px 20px;
  cursor: pointer;
  color: #000000;
}

.options li:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.custom-select {
  position: relative;
  display: inline-block;
  margin-left: 20px;
  width: 150px;
}

.selected {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: bold;
  background-color: #9d9d9d;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
  width: 100%;
  box-sizing: border-box;
}

.options {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: #9d9d9d;
  border-radius: 4px;
  z-index: 1;
  list-style: none;
  padding: 0;
  margin: 0;
  display: none;
  width: 100%;
}

.options li {
  padding: 10px 20px;
  color: rgb(0, 0, 0);
  cursor: pointer;
  width: 100%;
  box-sizing: border-box; 
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

/* .pagination-controls-2 {
  display: flex;
  align-items: center;
  margin: auto;
  gap: 8px;
  position: absolute;
  bottom: 10%;
  left: 36%;
  justify-content: center;
  margin-top: 20px;
  gap: 8px;
} */

.pagination-controls-2 {
  height: 100%;
  display: flex;
  align-items: center;

justify-content: center;
  margin-top: .8vw;
  gap: .4vw;
}

.arrow {
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

.sort-select {
  margin-left: 20px;
}
</style>
