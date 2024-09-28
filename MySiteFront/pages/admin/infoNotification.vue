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
    border: .3vw solid lightgray;
    border-radius: 2.5vw;
    width: 10vw;
    height: 5vw;
    display: flex;
    align-content: center;
    justify-content: center;
    position: absolute;
    top: 6vw;
    right: 2vw;
}

.no {
    background-color: lightcoral;
}

.yes {
    background-color: lightgreen;

}

p {
    font-size: 1vw;
    color: black;
    margin: auto;
}

</style>