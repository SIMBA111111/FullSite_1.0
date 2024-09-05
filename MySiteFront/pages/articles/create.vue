<template>
    <div>
        <myheader></myheader>
        <div class="create-container">
            <div class="create-form">    
                <form @submit.prevent="handleSubmit">
                    <div>
                        <input id="file" name="file" type="file" @change="handleFileChange" />
                    </div>
                    <div>
                        <input v-model="title" name="title" type="text" placeholder="Название статьи" />
                    </div>
                    <div>
                        <input v-model="introText" name="introText" type="text" placeholder="Завлекающий текст"/>
                    </div>
                    <button type="submit">Отправить</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { url } from '../../MyConstants.vue';

definePageMeta({
  middleware: 'auth'
});

const file = ref(null);
const title = ref('');
const introText = ref('');

const handleFileChange = (event) => {
    file.value = event.target.files[0];
};

const handleSubmit = async () => {
    if (!file.value) {
        alert('Пожалуйста, выберите файл.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file.value);
    formData.append('title', title.value);
    formData.append('intro_text', introText.value);

    try {
        const response = await axios.post(`${url}/articles/create`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': useCookie('access_token').value
            }
        });
        console.log('Ответ сервера:', response.data);
        alert('Файл успешно отправлен.');
    } catch (error) {
        console.error('Ошибка при отправке файла:', error);
        // if (error.response && error.response.status == 403) {
        // NotIsAdminUser.value = true;
        // } else {
        // console.error("Unexpected error:", error.message);
        // }
    }
};
</script>

<style>
.create-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 81vh;
  background-color: #d8cef1;
}

.create-form {
  background-color: #462887;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(221, 22, 239, 0.5);
  width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.create-form h2 {
  margin-bottom: 1rem;
}

.create-form input {
  width: 100%;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.create-form input:hover {
  box-shadow: 0 0 10px 7px rgba(221, 22, 239, .5);
}

.create-form input:focus {
  box-shadow: 0 0 10px 10px rgba(221, 22, 239, 1);
  outline: none;
}

.create-form button {
  padding: 0.5rem 1rem;
  background-color: #c5b02b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-form button:hover {
  background-color: #80700e;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>