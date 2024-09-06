<template>
    <div>
        <myheader></myheader>
        <div class="main-container">
            <div class="search-container">
                <div class="input-wrapper">
                    <input type="text" id="search" v-model="searchQuery" @input="onInput" @focus="showSuggestions" @blur="handleBlur" placeholder="Поиск статей..." autocomplete="off" ref="searchInput">
                    <button type="button" class="cancel-btn" @click="handleCancel">Отменить</button>
                </div>
                <button type="button" class="search-btn" @click="handleSearch">Найти</button>
                <div id="suggestions" :class="{ 'visible': suggestions.length > 0 }" @mousedown="handleSuggestionClick" ref="suggestions">
                    <div v-for="(suggestion, index) in suggestions" 
                         :key="suggestion" 
                         class="suggestion-item" 
                         :class="{ 'active': index === selectedIndex }" 
                         @click="selectSuggestion(suggestion)">
                        {{ suggestion }}
                    </div>
                </div>
            </div>
        </div>      
    </div>
</template>

<script>
import { url } from "../MyConstants.vue"

definePageMeta({
  middleware: 'auth'
});

export default {
    data() {
        return {
            searchQuery: '',
            suggestions: [],
            selectedIndex: -1,
            shouldShowSuggestions: false
        };
    },
    methods: {
        onInput() {
            if (this.searchQuery.length > 2) {
                this.fetchSuggestions(this.searchQuery);
                this.shouldShowSuggestions = true;
            } else {
                this.suggestions = [];
                this.shouldShowSuggestions = false;
            }
        },
        fetchSuggestions(query) {
            let xhr = new XMLHttpRequest();
            xhr.open('GET', `${url}/articles/search-article/?query=${encodeURIComponent(query)}`, true);
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    this.suggestions = JSON.parse(xhr.responseText);
                    this.selectedIndex = -1;
                    this.shouldShowSuggestions = this.suggestions.length > 0;
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
            this.shouldShowSuggestions = false;
        },
        selectSuggestion(suggestion) {
            this.searchQuery = suggestion;
            this.suggestions = [];
            this.shouldShowSuggestions = false;
        },
        handleKeyDown(event) {
            if (this.shouldShowSuggestions && this.suggestions.length > 0) {
                if (event.key === 'ArrowDown') {
                    event.preventDefault();
                    this.selectedIndex = (this.selectedIndex + 1) % this.suggestions.length;
                } else if (event.key === 'ArrowUp') {
                    event.preventDefault();
                    this.selectedIndex = (this.selectedIndex - 1 + this.suggestions.length) % this.suggestions.length;
                } else if (event.key === 'Enter') {
                    event.preventDefault();
                    if (this.selectedIndex >= 0) {
                        this.selectSuggestion(this.suggestions[this.selectedIndex]);
                    }
                }
            }
        },
        showSuggestions() {
            if (this.shouldShowSuggestions) {
                this.$refs.suggestions.style.display = 'block';
            }
        },
        handleBlur() {
            setTimeout(() => {
                this.$refs.suggestions.style.display = 'none';
            }, 100);
        },
        handleSuggestionClick() {
            this.$refs.searchInput.focus();
        }
    },
    mounted() {
        this.$refs.searchInput.focus();
        window.addEventListener('keydown', this.handleKeyDown);
    },
    beforeDestroy() {
        window.removeEventListener('keydown', this.handleKeyDown);
    }
}
</script>

<style scoped>
.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    height: 81vh;
    background-color: #d8cef1;
    padding-top: 20px;
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
    padding: 15px 40px 15px 15px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    font-size: 1.1rem;
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
    padding: 10px 15px;
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
    padding: 15px 25px;
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
    display: none;
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

#suggestions.visible {
    display: block;
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

.suggestion-item.active {
    background-color: #b0a4d8;
    color: #462887;
}
</style>
