<template>
  <div class="outer-author-card">
    <div class="author-card">
      <div class="author-info">
        <!-- <img :src="avatar" alt="Avatar" class="avatar" /> -->
        <div class="author-name">{{ first_name }} {{ last_name }}</div>
      </div>
      <div class="date">пишет с {{ formatDate(first_article_date) }}</div>
      <div class="eye-card">
        <span class="eye">👁</span>
        <span> {{ views_count }}</span>
      </div>
      <!-- <div><NuxtLink :to="`/authors/${username}`" class="title ">{{ username }}</NuxtLink></div> -->
      <!-- <div><NuxtLink to="/" class="content content_">{{ main_text }}...<NuxtLink to="/" class="read-more content_">читать полностью</NuxtLink></NuxtLink></div> -->
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

// const props = defineProps({
//   authorObj: {
//    type: Object
//  }
// })

const props = defineProps({
 id: {
   type: Number
 },
 last_name: {
   type: String
 },
 first_name: {
   type: String
 },
 email: {
   type: String
 },
 views_count: {
   type: Number
 },
 first_article_date: {
   type: String
 }
})
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric'};
  return new Date(dateString).toLocaleString('ru-RU', options);
}; 
</script>


<style scoped>
.author-card {
  display: flex;
  flex-direction: column;
  gap: .8vw;
  margin: 0px; 
  background-color: #d9d9d9;
  border-radius: .5vw;
  padding: 1.2vw;
  width: 26.5vw;
  height: 15.6vw;
  box-shadow: 0 .3vw .6vw rgba(255, 255, 255, .1);
}

.author-card:hover {
  box-shadow: .9vw .9vw .9vw rgba(199, 199, 199, .2);
  transform: translateZ(1vw);
  transition: box-shadow 0.5s ease, color 0.9s ease, transform 0.9s ease; /* Указываем свойства, для которых применяем переход */
  transition-delay: 0.1s; /* Указываем задержку перед началом перехода */
}

.author-info {
  font-size: 2.5vw;
  font-weight: bold;
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  margin-bottom: .7vw;
}

.date {
  color: black;
  font-size: 1.5vw;
  margin-top: .7vw;
  margin-bottom: .7vw;
}

.eye-card {
  font-size: 2vw;
  display: flex;
  align-items: center;
  height: 1.2vw;
}

.eye {
  display: inline-block;
  font-size: 2.4vw;
  width: 2.3vw;
  height: 2.3vw;
  margin-right: .4vw;
  padding-bottom: 1.2vw;
}

@media (max-width: 425px) {

.article-card {
  gap: .1vw;
}

.author-info {
  font-size: 3.5vw;
}

.date {
  font-size: 2vw;
  margin-bottom: 3vw;
}

.eye-card {
  font-size: 3vw;
}

.eye {
  height: 7.6vw;
  width: 5vw;
  font-size: 5vw;
}

}

</style>
