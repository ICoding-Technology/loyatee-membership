<template>
  <div class="w-full px-7 pb-5 pt-3 border-b border-gray-200">
    <div>
      <!-- Header row -->
      <div class="flex items-baseline justify-between">
        <div>
          <p class="text-sm font-semibold text-slate-900">Total Balance</p>
          <p class="mt-1 text-xs text-slate-400">
            <span class="font-number">{{ total - current }}</span> more points
            to claim reward
          </p>
        </div>
        <div class="text-right">
          <p class="text-lg font-semibold text-[#3B82F6] font-number">
            {{ current.toLocaleString() }}
          </p>
          <p class="mt-1 text-xs text-slate-400">Points</p>
        </div>
      </div>

      <!-- Progress bar -->
      <div class="mt-4 h-1.5 w-full rounded-full bg-slate-200 overflow-hidden">
        <div
          class="h-full rounded-full bg-[#3B82F6] transition-all duration-300"
          :style="{ width: computedPercent + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  current: number;
  total: number;
}>();

const computedPercent = computed(() => {
  if (!props.total || props.total <= 0) return 0;
  const value = (props.current / props.total) * 100;
  return Math.max(0, Math.min(100, Math.round(value)));
});
</script>

<style scoped></style>
