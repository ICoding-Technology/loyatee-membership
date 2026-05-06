<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <NavBar title="Card Detail" />

    <!-- Balance & Level card -->
    <div class="px-5 pt-4 pb-2">
      <div
        class="rounded-[15px] bg-gradient-to-br from-[#4C86E5] to-[#3B5FD4] shadow-md aspect-video px-5 py-5 flex flex-col justify-center items-center text-center text-white"
      >
        <!-- Balance -->
        <p class="text-xs text-white/60">Total Balance</p>
        <p class="mt-2 text-3xl font-bold font-number">
          {{ totalBalance.toLocaleString() }}
        </p>
        <p class="mt-1 text-xs text-white/60">Points</p>

        <!-- Divider -->
        <div class="h-px bg-white/20 w-full my-4"></div>

        <!-- Validity -->
        <div class="text-white/80 text-xs">
          <span>Valid until: </span>
          <span class="font-semibold text-white">{{ validUntil }}</span>
        </div>

        <!-- Unsubscribe -->
        <button
          type="button"
          class="mt-4 px-4 py-1.5 rounded-full border border-white/30 text-white/80 text-[10px] font-semibold hover:bg-white/10 transition"
        >
          Unsubscribe
        </button>
      </div>
    </div>

    <!-- Rewards -->
    <div class="flex-1 flex flex-col bg-gray-100 px-3 pb-3">
      <div class="flex items-center justify-between px-4 pt-4 pb-3">
        <span class="text-xs font-semibold text-slate-900">Rewards</span>
        <span class="text-xs text-slate-400"
          >{{ rewards.length }} available</span
        >
      </div>

      <div class="space-y-3 px-3">
        <div
          v-for="reward in rewards"
          :key="reward.id"
          class="rounded-md border border-gray-200 bg-white px-4 py-4 flex items-center gap-3"
        >
          <div
            class="w-10 h-10 rounded-full bg-[#E0EDFF] flex items-center justify-center flex-shrink-0"
          >
            <UIcon name="i-heroicons-gift" class="w-5 h-5 text-[#3B82F6]" />
          </div>
          <div class="flex-1">
            <p class="text-xs font-semibold text-slate-900">
              {{ reward.name }}
            </p>
            <p class="mt-0.5 text-[10px] text-[#3B82F6] font-semibold font-number">
              {{ reward.points }} pts
            </p>
          </div>
          <button
            type="button"
            class="flex-shrink-0 px-3 py-1.5 rounded-full bg-[#3B82F6] text-white text-[10px] font-semibold"
          >
            Redeem
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
if (!getAuthToken()) navigateTo("/login");
</script>

<script lang="ts">
export default {
  data() {
    return {
      validUntil: "12 July 2023",
      totalBalance: 200,
      rewards: [
        {
          id: 1,
          name: "Free Coffee",
          description: "Redeem at any outlet",
          points: 50,
        },
        {
          id: 2,
          name: "10% Discount",
          description: "Valid on next purchase",
          points: 100,
        },
        {
          id: 3,
          name: "Free Delivery",
          description: "One-time free delivery",
          points: 80,
        },
        {
          id: 4,
          name: "Birthday Voucher",
          description: "Special birthday treat",
          points: 150,
        },
        {
          id: 5,
          name: "VIP Lounge Access",
          description: "1 hour lounge access",
          points: 200,
        },
      ],
    };
  },
};
</script>
