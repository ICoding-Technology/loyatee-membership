<template>
    <div class="w-full flex flex-col">
        <div class=" bg-gray-100 px-3 pb-3 flex flex-col">
            <!-- Header -->
            <div class="flex items-center justify-between px-4 pt-4 pb-3">
                <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-slate-900">Transactions</span>
                </div>
                <span class="text-xs text-slate-400">Last 30 days</span>
            </div>

            <!-- List -->
            <div class="space-y-3 px-3">
                <TransactionItem v-for="tx in transactions" :key="tx.id" :title="tx.title" :date="tx.date"
                    :amount="tx.amount" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import TransactionItem from './TransactionItem.vue'

const transactions = [
    {
        id: 1,
        title: 'Earned point',
        date: '12 July 2023',
        amount: 20
    }
]
</script>

<style scoped></style>
