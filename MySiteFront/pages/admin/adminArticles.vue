<template>
    <div>
        <AdminHeader></AdminHeader>
        <adminArticleList></adminArticleList>
    </div>
</template>

<script setup lang="js">
  definePageMeta({
    middleware: 'auth'
  });

</script>

<style>
</style>