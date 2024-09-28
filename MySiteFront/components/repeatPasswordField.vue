<template>
    <div>
        <div class="wrapper">
            <input 
                v-model="input" 
                class="search" 
                type="password"
                placeholder="повторите пароль" 
                autocomplete="off"
                @keyup="validateInput"
                @blur="validateInput"
                @input="$emit('update:modelValue', $event.target.value)"
            />
            <div v-if="error" class="error">Пароли должны совпадать</div>
        </div>
    </div>
</template>

<script setup>
    import useFormValidation from "../modules/useFormValidation"
    import { defineProps, watch } from "vue";

    const props = defineProps({
        userPassword: {
            type: String,
            required: true
        }
    })

    const error = ref(false);
    const input = ref('');

    console.log('repeat', String(props.userPassword) == String(input.value));

    if (input.value != props.userPassword) {
        error.value = true;
    }

    watch(input, () => {
        if (input.value != props.userPassword) {
        error.value = true;
    } else {
        error.value = false;
    }}, {deep: true})

    // const { validatePasswordField, errors} = useFormValidation();
    // const validateInput = () => {
    //     validatePasswordField('password', input.value);
    // }
</script>

<style scoped>
* {
    box-sizing: border-box;
}

.wrapper {
    position: relative;
    width: 55.5vw;
    margin-left: 16.5vw;
}

.error {
    width: 15.2vw;
    border: .3vw solid red;
    border-radius: 1vw;
    height: 5.3vw;
    font-size: 1.5vw;
    color: red;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    right: 0;
    top: 0;
    padding-left: .8vw;
}

.search {
  width: 39vw;
  /* height: 16vh; */
  padding: 1.7vw 9vw 1.7vw 2.5vw;
  box-sizing: border-box;
  border: 0px;
  border-radius: 5vw;
  background-color: #D9D9D9;
  font-size: 2vw;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search::placeholder {
    font-size: 1.6vw;
}

</style>