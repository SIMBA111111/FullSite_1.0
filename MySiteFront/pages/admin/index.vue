<template>
    <div>
        <AdminHeader></AdminHeader>
        
    </div>
</template>

<script setup lang="js">
  definePageMeta({
    middleware: 'auth'
  });

</script>

<style>
</style>