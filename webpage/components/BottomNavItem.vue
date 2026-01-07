<template>
    <button type="button"
        class="relative z-10 inline-flex items-center justify-center font-semibold px-3 py-3 text-sm transition-colors"
        :class="active ? 'text-[#3B82F6]' : 'text-gray-500'" @click="$emit('click')">
        <div class="flex items-center justify-center">
            <UIcon :name="icon" class="w-5 h-5 mr-1" />
            <span class="overflow-hidden whitespace-nowrap transition-all duration-200"
                :class="active ? 'max-w-[80px] opacity-100 ml-1' : 'max-w-0 opacity-0 ml-0'">
                {{ label }}
            </span>
        </div>
    </button>
</template>

<script setup lang="ts">
interface Props {
    label: string
    icon: string
    active?: boolean
}

withDefaults(defineProps<Props>(), {
    active: false
})

defineEmits<{ (e: 'click'): void }>()
</script>
