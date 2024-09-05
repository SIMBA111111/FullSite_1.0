<template>
  <div class="admin-container">
    <div v-if="NotIsAdminUser">
      <nonadmin></nonadmin> 
    </div>
    <div v-else>
      <AdminHeader></AdminHeader>
      <h1 class="heading">Заявки</h1>
      <div v-for="bid in bidList" :key="bid.id" class="bid-card">
        <div class="bid-info">
          <!-- <div class="bid-title">{{ bid.title }}</div> -->
          <div class="bid-name">{{ bid.name }}</div>
          <div class="bid-intro">{{ bid.intro_text }}</div>
        </div>
        <div class="bid-buttons">
          <button class="action-button" @click="downloadBid(bid.name)">скачать</button>
          <button class="action-button" @click="approveBid(bid.name)">Одобрить</button>
          <button class="action-button" @click="cancelBid(bid.name)">Отказать</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import axios from 'axios';
  import { url } from '../../MyConstants.vue';
  import nonadmin from '~/components/nonadmin.vue';

  definePageMeta({
    middleware: 'auth'
  });

  const bid_url = `${url}/admin/bid-list`;
  const download_url = `${url}/admin/download-file`;
  const approve_url = `${url}/admin/approve-bid`;
  const cancel_url = `${url}/admin/cancel-bid`;
  const response = ref("")
  const NotIsAdminUser = ref(false);
  // const access_token = useCookie('access_token').value;

  try {
    response.value = await axios.get(bid_url, {
        headers: {
            "Authorization": useCookie('access_token').value
        }
    });
  } catch (error) {
      console.error("Error fetching bid list:", error);
      if (error.response && error.response.status == 403) {
        NotIsAdminUser.value = true;
      } else {
        console.error("Unexpected error:", error.message);
      }
  }
  console.log("response.value - ", response);
  
  const bidList = ref(response.value.data)
 
 // скачать статью
  const downloadBid = async (filename) => {
    if (typeof filename !== 'string') {
        console.error("filename должен быть строкой");
        return;
    }

    try {
        const res = await axios.post(download_url, {
            filename: filename
        }, {
            headers: {
                'Content-Type': 'application/json',
                "Authorization": useCookie('access_token').value
            },
            responseType: 'blob'
        });
         
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename); 
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error("Error downloading file:", error);
        if (error.response && error.response.status == 403) {
          NotIsAdminUser.value = true;
        } else {
          console.error("Unexpected error:", error.message);
        }
    }
};

// одобрить статью
const approveBid = async (filename) => {
  try {
        const res = await axios.post(approve_url, {
            filename: filename
        }, {
            headers: {
                'Content-Type': 'application/json',
                "Authorization": useCookie('access_token').value 
            }
        });
    } catch (error) {
        console.error("Error approve bid:", error);
        if (error.response && error.response.status == 403) {
          NotIsAdminUser.value = true;
        } else {
          console.error("Unexpected error:", error.message);
        }
    }
};


// удалить статью
const cancelBid = async (filename) => {
  try { 
        const res = await axios.post(cancel_url, {
            filename: filename
        }, {
            headers: {
                'Content-Type': 'application/json',
                "Authorization": useCookie('access_token').value
            }
        });
    } catch (error) {
        console.error("Error approve bid:", error);
        if (error.response && error.response.status == 403) {
        NotIsAdminUser.value = true;
        } else {
        console.error("Unexpected error:", error.message);
        }
    }
};

</script>
  
<style scoped>
.admin-container {
  max-width: 90%;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.heading {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.bid-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

.bid-info {
  flex-grow: 1;
}

.bid-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.bid-name {
  font-size: 16px;
  margin-bottom: 10px;
}

.bid-intro {
  font-size: 14px;
  color: #555;
}

.bid-buttons {
  display: flex;
  flex-direction: column;
}

.action-button {
  display: inline-block;
  padding: 8px 12px;
  font-size: 14px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 5px;
  
}

.action-button:hover {
  background-color: #0056b3;
}

.action-button + .action-button {
  margin-top: 5px;
}
</style>