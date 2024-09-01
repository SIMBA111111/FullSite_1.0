<template>
    <div>
        <myheader></myheader>
        <div>{{ authorData.id }}</div>
        <div>{{ authorData.username }}</div>
        <div>{{ authorData.email }}</div>
    </div>
</template>

<script setup charset="UTF-8">
import axios from 'axios';
import { url } from '../../MyConstants.vue';


const username = useRouter().currentRoute.value.params.username

const author_url = `${url}/users/get-author`;

const response = await axios.post(author_url, {
    username: username,
    }, 
);

const authorData = response.data.author
</script>

<style scoped>
</style>