<template>
  <div class="outer-author-card">
    <div class="author-card">
      <div class="author-info">
        <!-- <img :src="avatar" alt="Avatar" class="avatar" /> -->
        <div class="author-name">{{ first_name }} {{ last_name }}</div>
      </div>
      <div class="date"> date</div>
      <div class="eye-card">
        <span class="eye">👁</span>
        <span> count_views</span>
      </div>
      <!-- <div><NuxtLink :to="`/authors/${username}`" class="title ">{{ username }}</NuxtLink></div> -->
      <!-- <div><NuxtLink to="/" class="content content_">{{ main_text }}...<NuxtLink to="/" class="read-more content_">читать полностью</NuxtLink></NuxtLink></div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Author {
  id: number;
  first_name: string;
  last_name: string;
}

const props = defineProps<{
  id: Number;
  first_name: string;
  last_name: string;
  emain: string;
  username: string
}>();

</script>

<style scoped>



.author-card {
  margin: 20px; 
  /* height: 100%; */
  
  background-color: rgb(210, 210, 210);
  border-radius: 10px;
  padding: 16px;
  margin: 20px;
  /* width: 180px; */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.author-card:hover {
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
  font-size: 42px;
}

.date {
  color: gray;
  font-size: 24px;
  margin-bottom: 8px;
}

.eye-card {
  font-size: 28px;
}

.eye {
  width: 30px;
  height: 30px;
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