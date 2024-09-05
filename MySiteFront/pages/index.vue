<template>
    <div>
        <myheader></myheader>
        <div class="main-container">
            <div class="search-container">
                <div class="input-wrapper">
                    <input type="text" id="search" v-model="searchQuery" @input="onInput" placeholder="Поиск статей..." autocomplete="off" ref="searchInput">
                    <button type="button" class="cancel-btn" @click="handleCancel">Отменить</button>
                </div>
                <button type="button" class="search-btn" @click="handleSearch">Найти</button>
                <div id="suggestions">
                    <div v-for="suggestion in suggestions" :key="suggestion" class="suggestion-item" @click="selectSuggestion(suggestion)">
                        {{ suggestion }}
                    </div>
                </div>
            </div>
        </div>      
    </div>
</template>

<script>
import {url} from "../MyConstants.vue"

definePageMeta({
  middleware: 'auth'
});

export default {
    data() {
        return {
            searchQuery: '',
            suggestions: []
        };
    },
    methods: {
        onInput() {
            if (this.searchQuery.length > 2) {
                this.fetchSuggestions(this.searchQuery);
            } else {
                this.suggestions = [];
            }
        },
        fetchSuggestions(query) {
            let xhr = new XMLHttpRequest();
            xhr.open('GET', `${url}/articles/search-article/?query=${encodeURIComponent(query)}`, true);
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    this.suggestions = JSON.parse(xhr.responseText);
                }
            };
            xhr.send();
        },
        handleSearch() {
            if (this.searchQuery.length > 2) {
                this.fetchSuggestions(this.searchQuery);
            } else {
                alert('Введите больше 2 символов для поиска.');
            }
        },
        handleCancel() {
            this.searchQuery = '';
            this.suggestions = [];
        },
        selectSuggestion(suggestion) {
            this.searchQuery = suggestion;
            this.suggestions = [];
        }
    },
    mounted() {
        this.$refs.searchInput.focus(); // Устанавливаем фокус на поле ввода при монтировании компонента
    }
}
</script>

<style scoped>
.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Прижимаем к верху */
    height: 81vh;
    background-color: #d8cef1;
    padding-top: 20px; /* Добавляем отступ сверху для пространства */
}

.search-container {
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 600px;
    position: relative;
}

.input-wrapper {
    position: relative;
    flex-grow: 1;
}

#search {
    width: 100%;
    padding: 15px 40px 15px 15px; /* Увеличенный padding для высоты инпута */
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    font-size: 1.1rem; /* Увеличенный размер шрифта */
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

#search:focus { 
    box-shadow: 0 0 8px rgba(70, 40, 135, 0.5);
    border-color: #462887;
    outline: none;
}

.cancel-btn {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    padding: 10px 15px; /* Увеличенный padding для высоты кнопки */
    background: #c5b02b;
    border: none;
    border-radius: 4px;
    color: white;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background 0.3s ease;
}

.cancel-btn:hover {
    background: #80700e;
}

.search-btn {
    padding: 15px 25px; /* Увеличенный padding для высоты кнопки */
    margin-left: 10px;
    background-color: #462887;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.search-btn:hover {
    background-color: #3a1a6b;
}

#suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 4px;
    max-height: 200px;
    overflow-y: auto;
    background-color: white;
    z-index: 1000;
    box-sizing: border-box;
    transition: box-shadow 0.3s ease;
}

.suggestion-item {
    padding: 10px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
    background-color: #ffffff;
    border-bottom: 1px solid #ddd;
}

.suggestion-item:hover {
    background-color: #d8cef1;
    color: #462887;
    box-shadow: 0 2px 5px rgba(70, 40, 135, 0.3);
}

.suggestion-item:active {
    background-color: #b0a4d8;
    box-shadow: inset 0 0 5px rgba(70, 40, 135, 0.5);
}
</style>
