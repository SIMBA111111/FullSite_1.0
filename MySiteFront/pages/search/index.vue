<template>
    <div>
      <myheader></myheader>
      <div class="main-container">
        <!-- <div class="hr"></div> -->
        <div class="search-container">
          <div class="input-wrapper">
            <input
                v-model="searchQuery.query"
                @input="onChangeSearchInput"
              type="text"
              id="search"
              placeholder="Поищем..."
              autocomplete="off"
              ref="searchInput"
            />
            <button @click="onClearInput" type="button" class="cancel btn">
              <svg
                width="3.6vw"
                height="3vw"
                viewBox="0 0 17 15"
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
            <button type="button" class="search btn">
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
        </div>

        <articlesList
            :query="searchQuery.query"
        />

      </div>
    </div>
</template>

<script setup>
    import axios from "axios";
    import { url } from "../MyConstants.vue";
    import { watch } from "vue";


    import articlesList from "~/components/articlesList.vue";

  definePageMeta({ 
    middleware: "auth",
  });

   
  const searchQuery = reactive({
    query: ''
  });


  const items = ref([]);

  // const fetchItems = async () => {
  //   try {
  //       const { data } = await axios(`${url}/articles/search-article?query=${searchQuery.query}`)
  //       items.value = data;

  //   } catch (err) {

  //   }
  // }

  const onChangeSearchInput = (event) => {
    searchQuery.query = event.target.value

  }

  const onClearInput = () => {
    searchQuery.query = ''
  }

  // watch(() => searchQuery.query, () => fetchItems())

</script>




<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
  background-color: #191919;
  padding-top: 20px;
  padding-top: 3vw;
}

.search-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 58.5vw;
  position: relative;
  margin-bottom: 3vw;
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
