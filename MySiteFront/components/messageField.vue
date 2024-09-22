<template>
    <div>
        <div class="wrapper">
            <input 
                v-model="input" 
                class="search" 
                type="text" 
                placeholder="сообщение" 
                autocomplete="off"
                @keyup="validateInput"
                @blur="validateInput"
                @input="$emit('update:modelValue', $event.target.value)"
            />
            <div v-if="errors.first_name" class="error">{{ errors.first_name }}</div>
        </div>
    </div>
</template>

<script setup>
    import useFormValidation from "../modules/useFormValidation"

    const input = ref('');
    const { validateNameField, errors} = useFormValidation();
    const validateInput = () => {
        validateNameField('сообщение', input.value);
    }
</script>

<style scoped>
* {
    box-sizing: border-box;
}

.wrapper {
    /* border: 1px solid green; */
    position: relative;
    width: 800px;
    margin-left: 240px;
}

.error {
    width: 220px;
    border: 3px solid red;
    border-radius: 15px;
    height: 76px;
    font-size: 20px;
    color: red;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    right: 0;
    top: 0;
    padding-left: 10px;
}

.search {
    width: 560px;
    height: 76px;
    padding: 15px 40px 15px 35px;
    box-sizing: border-box;
    border: 0px;
    border-radius: 50px;
    background-color: #D9D9D9;
    font-size: 24px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search::placeholder {
    font-size: 24px;
}

</style>