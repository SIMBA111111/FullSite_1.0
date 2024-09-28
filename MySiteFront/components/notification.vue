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
  border: .3vw solid green;
  border-radius: 3vw;
  padding: 1.5vw;
  background-color: rgb(92, 199, 92);
  box-shadow: 0px 0px 3vw .1vw green;
  position: absolute;
  top: 9vw;
  right: 3.5vw;
}

.notification span {
  color: #fff;
  font-size: 1.8vw;
  font-weight: bold;
}

</style>