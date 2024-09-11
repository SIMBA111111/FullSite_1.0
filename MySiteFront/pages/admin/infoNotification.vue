<template>
    <div :class='notificationFlag ? "yes" : "no" '>
        <p v-if="notificationFlag">Статья одобрена</p>
        <p v-else>Статья отклонена</p>
    </div>
</template>

<script setup>

    const props = defineProps({
        notificationFlag: {
            type: Boolean
        }
    });

    const text = ref('Статья отклонена');

</script>

<style scoped>

div {
    border: 1px solid lightgray;
    border-radius: 10px;
    width: 130px;
    height: 50px;
    display: flex;
    align-content: center;
    justify-content: center;
    position: absolute;
    right: 30px;
}

.no {
    background-color: lightcoral;
}

.yes {
    background-color: lightgreen;

}

p {
    font-size: 14px;
    color: black;
    margin: auto;
}

</style>