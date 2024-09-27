<template>
    <div class="article-card">
      <div class="-">
        <div class="author-title">{{ props.title }}</div>
      </div>
      <div class="author-info">
        <div class="author-name">{{ props.user?.first_name }} {{ props.user?.last_name }}</div>
      </div>
      <div class="count_views">
        <div class="eye-card">
        <span class="eye">👁</span>
        <span>{{ count_views }}</span>
        </div>
      </div>
      <div class="date">
        {{ formatDate(props.date) }}
      </div>
      <div class="content-container"><NuxtLink :to="`/articles/${slug}`" class="content content_">{{ intro_text }}...<NuxtLink :to="`/articles/${slug}`" class="read-more content_">читать полностью</NuxtLink></NuxtLink></div>
    </div>
  </template>

<script setup>

import { defineProps } from 'vue';

 const props = defineProps({
  user: {
    type: Object
  },
  name: {
    type: String
  },
  title: {
    type: String
  },
  intro_text: {
    type: String
  },
  slug: {
    type: String
  },
  count_views: {
    type: Number
  },
  date: {
    type: String
  }
 })

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'};
  return new Date(dateString).toLocaleString('ru-RU', options);
};  
</script>

<style scoped>

.author-title {
  /* font-size: 28px; */
  font-size: 2.2vw;
  font-weight: bold;
}

.article-card {
  display: flex;
  flex-direction: column;
  /* gap: 10px; */
  gap: .8vw;
  margin: 0px; 
  /* height: 100%; */
  
  background-color: #d9d9d9;
  /* border-radius: 5px; */
  border-radius: .5vw;
  /* padding: 16px; */
  padding: 1.2vw;
  /* margin: 20px; */
  /* width: 340px; */
  width: 26.5vw;
  /* height: 200px; */
  height: 15.6vw;
  /* box-shadow: 0 4px 8px rgba(255, 255, 255, .1); */
  box-shadow: 0 .3vw .6vw rgba(255, 255, 255, .1);
}

.article-card:hover {
  /* box-shadow: 12px 12px 12px rgba(199, 199, 199, .2); */
  box-shadow: .9vw .9vw .9vw rgba(199, 199, 199, .2);
  /* transform: translateZ(10px); */
  transform: translateZ(1vw);
  transition: box-shadow 0.5s ease, color 0.9s ease, transform 0.9s ease; /* Указываем свойства, для которых применяем переход */
  transition-delay: 0.1s; /* Указываем задержку перед началом перехода */
}

.author-info {
  display: flex;
  align-items: center;
  /* margin-bottom: 8px; */
  margin-bottom: .7vw;
}

.date {
  color: black;
  /* font-size: 12px; */
  font-size: 1vw;
  margin-top: .7vw;
  /* margin-bottom: 8px; */
  /* margin-bottom: .7vw; */
}

.eye {
  display: inline-block;
  /* font-size: 30px; */
  font-size: 2.4vw;
  /* width: 30px; */
  width: 2.3vw;
  /* height: 30px; */
  height: 2.3vw;
  /* margin-right: 5px; */
  margin-right: .4vw;
  /* padding-bottom: 15px; */
  padding-bottom: 1.2vw;
}

.eye-card {
  /* font-size: 20px; */
  font-size: 1.5vw;
  display: flex;
  align-items: center;
  /* height: 15px; */
  height: 1.2vw;
}

.content {
  /* font-size: 14px; */
  font-size: 1vw;
  /* margin-bottom: 8px; */
  margin-bottom: .7vw;
  /* height: 80px; */
  height: 2vw;
  overflow: hidden;
}

.content_ {
  text-decoration: none;
  color: #555;
}

.read-more {
  /* font-size: 18px; */
  font-size: 1.5vw;
  color: #403d8b;
  text-decoration: underline;
  cursor: pointer;
}


.read-more:hover {
  /* font-size: 19px; */
  font-size: 1.5vw;
}

@media (max-width: 425px) {

  .article-card {
    gap: .1vw;
  }
  .author-title {
    font-size: 3vw;
  }

  .author-info {
    font-size: 2.5vw;
  }
  
  .date {
    font-size: 1.5vw;
  }

  .content {
    font-size: 1.5vw;
  }

}


</style>
