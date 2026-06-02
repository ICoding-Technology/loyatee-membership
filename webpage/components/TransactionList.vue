<template>
    <div class="w-full flex flex-col">
        <div class=" bg-gray-100 px-3 pb-3 flex flex-col">
            <!-- Header -->
            <div class="flex items-center justify-between px-4 pt-4 pb-3">
                <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-slate-900">Transactions</span>
                </div>
                <span class="text-xs text-slate-400">Recent activity</span>
            </div>

            <!-- List -->
            <div v-if="rows.length" class="space-y-3 px-3">
                <TransactionItem v-for="tx in rows" :key="tx.id" :title="tx.title" :date="tx.date"
                    :amount="tx.amount" />
            </div>

            <!-- Empty state -->
            <div v-else class="px-3">
                <div class="rounded-md border border-dashed border-gray-300 bg-white px-4 py-8 text-center">
                    <p class="text-xs text-slate-400">{{ loading ? "Loading…" : "No transactions yet" }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Transaction } from "../composables/useApi";
import TransactionItem from "./TransactionItem.vue";

const api = useApi();
const { member } = useProfile();

const loading = ref(true);
const rows = ref<{ id: string; title: string; date: string; amount: number }[]>([]);

const fmtDate = (iso: string) => {
    const d = new Date(iso);
    return Number.isNaN(d.getTime())
        ? ""
        : d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
};

const toRow = (tx: Transaction) => {
    const store = tx.store_name || "store";
    const earned = tx.side === "Cr";
    return {
        id: tx.id,
        title: `${earned ? "Earned at" : "Redeemed at"} ${store}`,
        date: fmtDate(tx.created_at),
        // Cr (earn) is positive, Dr (redeem) negative — drives the +/- styling.
        amount: earned ? tx.amount : -tx.amount,
    };
};

const load = async (memberId: string) => {
    loading.value = true;
    try {
        const data = await api.getMemberTransactions(memberId);
        rows.value = data.map(toRow);
    } catch {
        rows.value = [];
    } finally {
        loading.value = false;
    }
};

// The profile loads asynchronously on the home page; fetch once the member id
// is available (and refetch if it changes).
watch(() => member.value?.id, (id) => { if (id) load(id); }, { immediate: true });
</script>

<style scoped></style>
