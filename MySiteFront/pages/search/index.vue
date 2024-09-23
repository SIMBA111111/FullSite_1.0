<template>
    <div>
      <myheader></myheader>
      <div class="main-container">
        <div class="hr"></div>
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
                width="35"
                height="35"
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
                width="30"
                height="30"
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
  //       console.log('Items', items.value);
  //   } catch (err) {
  //       console.log(err);
  //   }
  // }

  const onChangeSearchInput = (event) => {
    searchQuery.query = event.target.value
    console.log( 'Input', searchQuery.query);
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
  height: 100vh;
  background-color: #191919;
  padding-top: 20px;
}

.hr {
  width: 90%;
  height: 5px;
  border-radius: 0%;
  background-color: #fff;
  margin-bottom: 40px;
  clip-path: polygon(60% 0%, 60% 0%, 100% 100%, 0% 100%);
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
  width: 560px;
  height: 76px;
  padding: 15px 40px 15px 35px;
  box-sizing: border-box;
  border: 0px;
  border-radius: 50px;
  background-color: #9b9b9b;
  font-size: 24px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

#search::placeholder {
  font-size: 25px;
}

#search:focus {
  box-shadow: 0 0 8px rgba(70, 40, 135, 0.5);
  border-color: #462887;
  outline: none;
}

.btn {
  position: absolute;
  transform: translateY(-50%);
  background: #d9d9d9;
  /* padding: 10px 15px; */
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.cancel {
  right: 105px;
  top: 50%;
  border-radius: 50%;
  width: 45px;
  height: 45px;
}

.search {
  right: 50px;
  top: 50%;
  border-radius: 50%;
  width: 45px;
  height: 45px;
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
