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

const slug = useRouter().currentRoute.value.params.slug

const fetchArticle = async () => {
    try {
        const article_url = `${url}/articles/get-article`;
        const response = await axios.post(article_url, {
            slug: slug,
        }, {
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': useCookie("access_token").value,
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
            }
        });

        const articleData = response.data.file_content;

        const articleDiv = document.getElementById('article');
        if (articleDiv) {
            articleDiv.innerHTML = articleData;
        } else {
            console.error('Element with id "article" not found');
        }
    } catch (error) {
        console.error('Error fetching article:', error);
    }
};

onMounted(() => {
    fetchArticle();
});
</script>

<style>
.article-container {
    background-color: #191919;
}

p {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 10px 0px;
    font-size: 18px;
    color: #f0f0f0;
    display: flex;
    align-items: center;
}

img {
    max-width: 100%;
    max-height: 100%;
    height: auto;
    width: auto;

}

#article {
    margin: 0% 10%;
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
