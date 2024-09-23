<template>
    <div class="notification">
        <span>{{ spanMessage }}</span>
    </div>
</template>


<script setup>
import { defineProps } from 'vue'; 
 
const props = defineProps({
    spanMessage: {
        type: String
    }
})

</script>


<style scoped>

.notification {
  border: 4px solid green;
  border-radius: 50px;
  padding: 20px;
  background-color: rgb(117, 251, 117);
  box-shadow: 0px 0px 30px 1px green;
}

.notification span {
  color: #fff;
  font-size: 24px;
  font-weight: bold;
}

</style>