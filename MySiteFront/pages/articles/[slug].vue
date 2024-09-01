<template>
    <div>
        <myheader></myheader>
        
        <div id="article"></div>
    </div>
</template>

<script setup charset="UTF-8">
import axios from 'axios';
import { url } from '../../MyConstants.vue';

useHead({
  title: 'My App',
  head: {
      charset: 'UTF-8'
    }
})

const slug = useRouter().currentRoute.value.params.slug
const article_url = `${url}/articles/get-article`;

const response = await axios.post(article_url, {
    slug: slug,
}, {
    headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': useCookie("access_token").value
    }
});


const articleData = response.data.file_content

onMounted(() => {
    var articleDiv = document.getElementById('article');
    if (articleDiv) {
        articleDiv.innerHTML = articleData;
    } else {
        console.error('Element with id "article" not found');
    }
});

</script>

<style>
p {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 18px;
}

.code{
    display: block;
    background-color: #f0f0f0;
    color: #333;
    border-left: 4px solid #cccccc;
    padding: 15px;
    margin: 20px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 1em;
    white-space: pre-wrap;
    word-wrap: break-word;
}

</style>