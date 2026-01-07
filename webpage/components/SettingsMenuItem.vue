<template>
    <button type="button"
        class="w-full flex items-center justify-between px-4 py-4 text-left text-sm md:text-base hover:bg-gray-50 transition-colors">
        <div class="flex items-center gap-3">
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-[#E0EDFF]">
                <UIcon :name="icon" class="h-4 w-4 text-[#3B82F6]" />
            </div>
            <span class="font-medium text-sm text-[#1F2A3C]">{{ label }}</span>
        </div>

        <UIcon name="i-heroicons-chevron-right" class="h-4 w-4 text-gray-400" />
    </button>
</template>

<script setup lang="ts">
interface Props {
    label: string
    icon: string
}

defineProps<Props>()
</script>
