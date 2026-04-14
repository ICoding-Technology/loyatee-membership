<template>
    <div class="rounded-md border border-gray-200 bg-white px-4 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div
                class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
                :class="amount > 0 ? 'bg-emerald-50' : 'bg-red-50'"
            >
                <UIcon
                    :name="amount > 0 ? 'i-heroicons-arrow-down-left' : 'i-heroicons-arrow-up-right'"
                    class="w-4 h-4"
                    :class="amount > 0 ? 'text-emerald-500' : 'text-red-500'"
                />
            </div>
            <div>
                <p class="text-xs font-semibold text-slate-900">{{ title }}</p>
                <p class="mt-1 text-[10px] text-slate-400">{{ date }}</p>
            </div>
        </div>
        <div class="text-right text-xs">
            <p :class="amount > 0 ? 'text-emerald-500' : 'text-red-500'">
                <span class="font-number">{{ amount > 0 ? '+' : '-' }} {{ Math.abs(amount) }}</span>
                <span> points</span>
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
