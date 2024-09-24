<template>
    <div>
        <myheader></myheader>
        <div class="create-container">
            <div class="create-form">    
                <form class="form" @submit.prevent="handleSubmit">
                    <label class="input-file">
                        <input ref="file" id="file" name="file" type="file" @change="handleFileChange" />
                        <span> {{ fileName || 'Здесь поле выбора файла' }}</span>
                      </label>
                    <div>
                        <input class="search" v-model="title" name="title" type="text" placeholder="Название статьи" />
                    </div>
                    <div>
                        <input class="search" v-model="introText" name="introText" type="text" placeholder="Завлекающий текст"/>
                    </div>
                    <div class="btn-wrapper">
                      <button class="btn" type="submit">Отправить</button>
                    </div>
                  </form>
            </div>
        </div>
        <div style="color: red;font-size: 30px;">{{ error }}</div>

        <notification
          :notificationMessage="notificationMessage"
          v-if="notificationMessage"
        />
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { url } from '../../MyConstants.vue';
import notification from '../../components/notification.vue';

definePageMeta({
  middleware: 'auth'
});


const fileName = ref('');
const title = ref('');
const introText = ref('');

const fileData = ref(null);
const notificationMessage = ref('');
const error = ref('');


const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]; // Получаем выбранный файл
    console.log("selectedFile - ", selectedFile);
    
    if (selectedFile) {
        fileName.value = selectedFile.name; // Устанавливаем имя выбранного файла
        fileData.value = selectedFile; // Сохраняем файл в переменной
    } else {
        fileName.value = ''; // Очищаем, если файл не выбран
        fileData.value = null; // Очищаем переменную с файлом
    }
};

const handleSubmit = async () => {

    if (!fileData.value) {
        alert('Пожалуйста, выберите файл.');
        return;
    }

    const formData = new FormData();
    formData.append('file_data', fileData.value);
    formData.append('title', title.value);
    formData.append('intro_text', introText.value);

    try {
        console.log("fileData - ", fileData.value);
        const response = await axios.post(`${url}/articles/create`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': useCookie('access_token').value
            }
        });
        if (response.status == 201) {
          title.value = '';
          introText.value = '';
          fileName.value = '';
          notificationMessage.value = 'Статья добавлена'
          setTimeout(() => notificationMessage.value = '', 3000)
        }
        console.log('Ответ сервера:', response.data);
        // alert('Файл успешно отправлен.');
    } catch (error) {
        console.error('Ошибка при отправке файла:', error);
        error.value = 'Ошибка при отправке файла';
        // if (error.response && error.response.status == 403) {
        // NotIsAdminUser.value = true;
        // } else {
        // console.error("Unexpected error:", error.message);
        // }
    }
};
</script>

<style scoped>
.create-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  background-color: #191919;
  padding-top: 20px;
}

.hr {
    width: 90%;
    height: 5px;
    background-color: #fff;
    margin-bottom: 40px;
    /* padding: 2px; */
    clip-path: polygon(60% 0%, 60% 0%, 100% 100%, 0% 100%);
}

.create-form {
  background-color: transparent;
  padding: 2rem;
  border-radius: 8px;
  width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.create-form h2 {
  margin-bottom: 1rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 21px;
}

.input-file {
	position: relative;
	display: inline-block;
}
.input-file span {
	position: relative;
	display: inline-block;
	cursor: pointer;
	outline: none;
	text-decoration: none;
	font-size: 24px;
	vertical-align: middle;
	color: rgb(255 255 255);
	text-align: center;
	border-radius: 4px;
	background-color: transparent;
	line-height: 22px;
	height: 50px;
	padding: 12px 20px 10px;
	box-sizing: border-box;
	border: none;
	margin: 0;
	transition: background-color 0.2s;
}
.input-file input[type=file] {
	position: absolute;
	z-index: -1;
	opacity: 0;
	display: block;
	width: 0;
	height: 0;
}
 
/* Focus */
.input-file input[type=file]:focus + span {
	box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}
 
/* Hover/active */
.input-file:hover span {
	background-color: #D9D9D9;
  color: #191919;
}
.input-file:active span {
	background-color: #D9D9D9;
  color: #191919;
}
 
/* Disabled */
.input-file input[type=file]:disabled + span {
	background-color: #eee;
}

.search {
    width: 560px;
    height: 76px;
    padding: 15px 40px 15px 35px;
    box-sizing: border-box;
    border: 0px;
    border-radius: 50px;
    background-color: #D9D9D9;
    font-size: 24px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search::placeholder {
    font-size: 24px;
}

.btn {
  width: 273px;
  height: 70px;
  background-color: #909090;
  color: #fff;
  font-size: 32px;
  border-radius: 50px;
  border: none;
}

.btn-wrapper {
  width: 560px;
  height: 70px;
  display: flex;
  justify-content: center;
}


.create-form button:hover {
  background-color: #80700e;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
