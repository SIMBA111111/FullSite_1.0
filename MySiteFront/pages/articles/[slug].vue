<template>
    <div>
        <myheader></myheader>
        <div class="article-container">
           <div id="article"></div>
        </div>
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
.article-container {
    background-color: #191919;
}
#article {
    margin: 0% 20%;
}

p {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 10px 0px;
    font-size: 18px;
    color: #f0f0f0;
}

.code{
    display: block;
    background-color: #444242;
    color: #000000;
    border-left: 4px solid #cccccc;
    padding: 15px;
    margin: 0px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 1em;
    white-space: pre-wrap;
    word-wrap: break-word;
}
</style>