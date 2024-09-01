<template>
    <div class="article-card">
      <div class="author-info">
        <!-- <img :src="avatar" alt="Avatar" class="avatar" /> -->
        <div class="author-name">{{ user.first_name }} {{ user.last_name }}</div>
      </div>
      <div class="date">{{ date }}</div>
      <div class="count_views">{{ count_views }}</div>
      <div><NuxtLink :to="`/articles/${slug}`" class="title ">{{ name }}</NuxtLink></div>
      <div><NuxtLink to="/" class="content content_">{{ main_text }}...<NuxtLink :to="`/articles/${slug}`" class="read-more content_">читать полностью</NuxtLink></NuxtLink></div>
    </div>
  </template>

<script setup lang="ts">
import { computed } from 'vue';

interface ArticleAuthor {
  id: number;
  first_name: string;
  last_name: string;
}

const props = defineProps<{
  user: ArticleAuthor;
  date: string;
  name: string;
  text: string;
  main_text: string;
  slug: string;
  count_views: number;
}>();

</script>

<style scoped>
.articles-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.article-card {
  background-color: rgba(240, 240, 240, 0.5);
  border-radius: 10px;
  padding: 16px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.article-card:hover {
  box-shadow: 12px 12px 12px rgba(0, 0, 0, 0.2);
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

.author-name {
  font-weight: bold;
}

.date {
  color: gray;
  font-size: 12px;
  margin-bottom: 8px;
}

.title {
  color: black;
  text-decoration: none;
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 8px;
}

.content {
  font-size: 22px;
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

</style>