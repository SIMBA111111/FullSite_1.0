<template>
    <div class="notification">
        <span>{{ notificationMessage }}</span>
    </div>
</template>


<script setup>
import { defineProps } from 'vue'; 
 
const props = defineProps({
  notificationMessage: {
        type: String
    }
})

</script>


<style scoped>

.notification {
  border: 4px solid green;
  border-radius: 50px;
  padding: 20px;
  background-color: rgb(92, 199, 92);
  box-shadow: 0px 0px 25px 1px green;
  position: absolute;
  top: 100px;
  right: 50px;
}

.notification span {
  color: #fff;
  font-size: 24px;
  font-weight: bold;
}

</style>