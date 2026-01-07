<template>
    <div class="rounded-md border border-gray-200 bg-white px-4 py-4 flex items-center justify-between">
        <div>
            <p class="text-xs font-semibold text-slate-900">{{ title }}</p>
            <p class="mt-1 text-[10px] text-slate-400">{{ date }}</p>
        </div>
        <div class="text-right text-xs">
            <p :class="amount > 0 ? 'text-emerald-500' : 'text-red-500'">
                {{ amount > 0 ? '+' : '-' }} {{ Math.abs(amount) }}
                <span>points</span>
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    title: string
    date: string
    amount: number
}>()

const { title, date, amount } = props
</script>

<style scoped></style>
