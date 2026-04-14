<template>
  <button
    type="button"
    class="w-full flex items-center justify-between px-4 py-4 text-left text-sm md:text-base hover:bg-gray-50 transition-colors"
    @click="onClick"
  >
    <div class="flex items-center gap-3">
      <div
        class="flex h-8 w-8 items-center justify-center rounded-full"
        :class="danger ? 'bg-red-50' : 'bg-[#E0EDFF]'"
      >
        <UIcon :name="icon" class="h-4 w-4" :class="danger ? 'text-red-500' : 'text-[#3B82F6]'" />
      </div>
      <span class="font-semibold text-sm" :class="danger ? 'text-red-500' : 'text-[#1F2A3C]'">{{ label }}</span>
    </div>

    <UIcon name="i-heroicons-chevron-right" class="h-4 w-4 text-gray-400" />
  </button>
</template>

<script setup lang="ts">
interface Props {
  label: string;
  icon: string;
  danger?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  danger: false,
});
const emit = defineEmits<{ (e: "click"): void }>();

const onClick = () => {
  emit("click");
};
</script>
