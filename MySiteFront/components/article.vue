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
      <div style="font-size: 16px;">
        date - {{ props.date }}
      </div>
      <div><NuxtLink :to="`/articles/${slug}`" class="content content_">{{ intro_text }}...<NuxtLink :to="`/articles/${slug}`" class="read-more content_">читать полностью</NuxtLink></NuxtLink></div>
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

console.log("props- ", props);
console.log("props.date - ", props.date);


</script>

<style scoped>

.author-title {
  font-size: 28px;
  font-weight: bold;
}

.article-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 0px; 
  /* height: 100%; */
  
  background-color: #d9d9d9;
  border-radius: 5px;
  padding: 16px;
  /* margin: 20px; */
  width: 340px;
  height: 200px;
  box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
}

.article-card:hover {
  box-shadow: 12px 12px 12px rgba(199, 199, 199, 0.2);
  transform: translateZ(10px);
  transition: box-shadow 0.5s ease, color 0.9s ease, transform 0.9s ease; /* Указываем свойства, для которых применяем переход */
  transition-delay: 0.1s; /* Указываем задержку перед началом перехода */
}

.author-info {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 8px;
}

.date {
  color: black;
  font-size: 12px;
  margin-bottom: 8px;
}

.count_views {
  font-size: 30px;
}

.eye {
  display: inline-block;
  font-size: 30px;
  width: 30px;
  height: 30px;
  margin-right: 5px;
  padding-bottom: 15px;
}

.eye-card {
  font-size: 20px;
  display: flex;
  align-items: center;
  height: 15px;
}

.title {
  padding-bottom: 10px; 
}

.title-link {
  color: black;
  text-decoration: none;
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 8px;
  /* gap: 100px; */
}

.content {
  font-size: 14px;
  margin-bottom: 8px;
  height: 80px;
  overflow: hidden;
}

.content_ {
  text-decoration: none;
  color: #555;
}

.read-more {
  font-size: 18px;
  color: #403d8b;
  text-decoration: underline;
  cursor: pointer;
}


.read-more:hover {
  font-size: 19px;
}


</style>