<template>
    <div class="numpad">
        <div class="numpad-grid">
            <button v-for="num in [1, 2, 3, 4, 5, 6, 7, 8, 9]" :key="num" @click="$emit('input', num.toString())"
                class="numpad-button" type="button">
                {{ num }}
            </button>
            <div class="numpad-spacer"></div>
            <button @click="$emit('input', '0')" class="numpad-button" type="button">
                0
            </button>
            <button @click="$emit('delete')" class="numpad-button delete-button" type="button">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path>
                    <line x1="18" y1="9" x2="12" y2="15"></line>
                    <line x1="12" y1="9" x2="18" y2="15"></line>
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
defineEmits<{
    input: [value: string]
    delete: []
}>()
</script>

<style scoped>
.numpad {
    width: 100%;
    margin-top: 10px;
}

.numpad-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.numpad-button {
    background: #f5f5f5;
    border: none;
    border-radius: 8px;
    padding: 10px;
    font-size: 20px;
    font-weight: 500;
    color: #333;
    cursor: pointer;
    transition: background-color 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 50px;
}

.numpad-button:active {
    background-color: #e0e0e0;
}

.numpad-spacer {
    background: transparent;
    border: none;
    pointer-events: none;
}

.delete-button {
    color: #999;
}

.delete-button svg {
    width: 24px;
    height: 24px;
}
</style>
