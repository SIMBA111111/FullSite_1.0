<template>
  <div>
    <myheader></myheader>
    <div class="main-container">
      <div class="search-container">
        <div class="input-wrapper">
          <input
            type="text"
            id="search"
            v-model="searchQuery"
            @input="onInput"
            @focus="showSuggestions"
            @blur="handleBlur"
            placeholder="Поищем..."
            autocomplete="off"
            ref="searchInput"
          />
          <button type="button" class="cancel btn" @click="handleCancel">
            <svg
              width="3.6vw"
              height="3vw"
              viewBox="0 0 16 16"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M4.11 2.697L2.698 4.11 6.586 8l-3.89 3.89 1.415 1.413L8 9.414l3.89 3.89 1.413-1.415L9.414 8l3.89-3.89-1.415-1.413L8 6.586l-3.89-3.89z"
                fill="#000"
              ></path>
            </svg>
          </button>
          <button type="button" class="search btn" @click="handleSearch">
            <svg
              width="3.6vw"
              height="2.7vw"
              viewBox="0 0 16 16"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M9.591 9.591a4 4 0 10-5.657-5.657 4 4 0 005.657 5.657zm1.06-6.717a5.502 5.502 0 01.915 6.57l2.732 2.733a1.5 1.5 0 11-2.121 2.12l-2.732-2.73a5.5 5.5 0 111.207-8.692z"
                fill="#000"
              ></path>
            </svg>
          </button>
        </div>
        <div
          id="suggestions"
          :class="{ visible: suggestions.length > 0 }"
          @mousedown="handleSuggestionClick"
          ref="suggestions"
        >
          <div
            v-for="(suggestion, index) in suggestions"
            :key="suggestion"
            class="suggestion-item"
            :class="{ active: index === selectedIndex }"
            @click="selectSuggestion(suggestion)"
          >
            {{ suggestion }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { url } from "../MyConstants.vue";



export default {
  
  data() {
    return {
      searchQuery: "",
      suggestions: [],
      selectedIndex: -1,
      shouldShowSuggestions: false,
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
      xhr.open(
        "GET",
        `${url}/articles/search-article/?query=${encodeURIComponent(query)}`,
        true
      );
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
        alert("Введите больше 2 символов для поиска.");
      }
    },
    handleCancel() {
      this.searchQuery = "";
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
        if (event.key === "ArrowDown") {
          event.preventDefault();
          this.selectedIndex =
            (this.selectedIndex + 1) % this.suggestions.length;
        } else if (event.key === "ArrowUp") {
          event.preventDefault();
          this.selectedIndex =
            (this.selectedIndex - 1 + this.suggestions.length) %
            this.suggestions.length;
        } else if (event.key === "Enter") {
          event.preventDefault();
          if (this.selectedIndex >= 0) {
            this.selectSuggestion(this.suggestions[this.selectedIndex]);
          }
        }
      }
    },
    showSuggestions() {
      if (this.shouldShowSuggestions) {
        this.$refs.suggestions.style.display = "block";
      }
    },
    handleBlur() {
      setTimeout(() => {
        // this.$refs.suggestions.style.display = 'none';
      }, 100);
    },
    handleSuggestionClick() {
      this.$refs.searchInput.focus();
    },
  },
  mounted() {
    this.$refs.searchInput.focus();
    window.addEventListener("keydown", this.handleKeyDown);
    
    definePageMeta({
      middleware: 'auth'
    });
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this.handleKeyDown);
  },
};
</script>

<style scoped>
.html{
  padding: 0px;
  margin: 0px;
}

.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  background-color: #191919;
  padding-top: 0px;
}



.search-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 58.5vw;
  position: relative;
}

.input-wrapper {
  position: relative;
  flex-grow: 1;
}

#search {
  width: 55.1vw;
  /* height: 16vh; */
  padding: 2.2vw 9vw 2.2vw 2.5vw;
  box-sizing: border-box;
  border: 0px;
  border-radius: 5vw;
  background-color: #9b9b9b;
  font-size: 2vw;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

#search::placeholder {
  font-size: 2vw;
}

#search:focus {
  box-shadow: 0 0 0.5vw rgba(70, 40, 135, 0.5);
  border-color: #462887;
  outline: none;
}

.btn {
  position: absolute;
  transform: translateY(-50%);
  background: #d9d9d9;
  border: none;
  border-radius: 1vw;
  color: white;
  cursor: pointer;
  font-size: 1vw;
  transition: background 0.3s ease;
}

.cancel {
  right: 8.2vw;
  top: 3.4vw;
  border-radius: 50%;
  width: 3.5vw;
  height: 3.5vw;
}

.search {
  right: 3.9vw;
  top: 3.4vw;
  border-radius: 50%;
  width: 3.5vw;
  height: 3.5vw;;
}
</style>
