<template>
  <div class="admin-container">
    <div v-if="NotIsAdminUser">
      <nonadmin></nonadmin> 
    </div>
    <div v-else>
      <AdminHeader></AdminHeader>
      <notificationDiv v-if="notificationFlag != null" :notificationFlag="notificationFlag" ></notificationDiv>
      <h1 class="heading">Заявки</h1>
      <template v-if="bidList[0]?.length">
        <div v-for="bid in bidList[0]" :key="bid.id" class="bid-card">
          <div class="bid-info">
            <!-- <div class="bid-title">{{ bid.title }}</div> -->
            <div class="bid-name">{{ bid.name }}</div>
            <div class="bid-intro">{{ bid.intro_text }}</div>
          </div>
          <div class="bid-buttons">
            <button class="action-button" @click="downloadBid(bid)">скачать</button>
            <button class="action-button" @click="approveBid(bid)">Одобрить</button>
            <button class="action-button" @click="cancelBid(bid)">Отказать</button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
  import axios from 'axios';
  import { url } from '../../MyConstants.vue';
  import nonadmin from '~/components/nonadmin.vue';
  import notificationDiv from './infoNotification.vue'

  definePageMeta({
    middleware: 'auth'
  });

  const bid_url = `${url}/admin/bid-list`;
  const download_url = `${url}/admin/download-file`;
  const approve_url = `${url}/admin/approve-bid`;
  const cancel_url = `${url}/admin/cancel-bid`;
  const response = ref("")
  const NotIsAdminUser = ref(false);
  const bidList = reactive([]);
  const notificationFlag = ref(null);
  // const access_token = useCookie('access_token').value;

  try {
    response.value = await axios.get(bid_url, {
        headers: {
            "Authorization": useCookie('access_token').value
        }
    });
    bidList.push(response.value.data)
    
  } catch (error) {
      console.error("Error fetching bid list:", error);
      if (error.response && error.response.status == 403) {
        NotIsAdminUser.value = true;
      } else {
        console.error("Unexpected error:", error.message);
      }
  }
  
 // скачать статью
  const downloadBid = async (filename) => {
    if (typeof filename.name !== 'string') {
        console.error("filename должен быть строкой");
        return;
    }

    try {
        const res = await axios.post(download_url, {
            filename: filename.name
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
        link.setAttribute('download', filename.name); 
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
            filename: filename.name
        }, {
            headers: {
                'Content-Type': 'application/json',
                "Authorization": useCookie('access_token').value 
            }
        });
        bidList[0] = bidList[0].filter( bid => bid != filename);
        notificationFlag.value = true;
        setTimeout(() => {
          notificationFlag.value = null
        }, 2000);
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
            filename: filename.name
        }, {
            headers: {
                'Content-Type': 'application/json',
                "Authorization": useCookie('access_token').value
            }
        })
        bidList[0] = bidList[0].filter( bid => bid != filename);
        notificationFlag.value = false;
        setTimeout(() => {
          notificationFlag.value = null
        }, 2000);
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
  padding: 1vw;
  font-family: Arial, sans-serif;
}

.heading {
  font-size: 1.5vw;
  text-align: center;
  margin-bottom: 1vw;
  color: #333;
  margin-bottom: 4vw;
}

.bid-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: .4vw;
  padding: .7vw;
  margin-bottom: .7vw;
  box-shadow: 0 .1vw .2vw rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

.bid-info {
  flex-grow: 1;
}

.bid-title {
  /* font-size: 18px; */
  font-size: 1vw;
  font-weight: bold;
  /* margin-bottom: 10px; */
  margin-bottom: 1vw;
}

.bid-name {
  font-size: 1.5vw;
  margin-bottom: .8vw;
}

.bid-intro {
  font-size: .8vw;
  color: #555;
}

.bid-buttons {
  display: flex;
  flex-direction: column;
}

.action-button {
  display: inline-block;
  padding: .4vw 1vw;
  font-size: 1vw;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: .2vw;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: .3vw;
  
}

.action-button:hover {
  background-color: #0056b3;
}

.action-button + .action-button {
  margin-top: .3vw;
}
</style>