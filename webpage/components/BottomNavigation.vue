<template>
    <div class=" bg-gray-100">
        <!-- Main content area between header (top) and bottom nav -->
        <div class="overflow-y-auto pb-20 ">
            <transition name="slide-horizontal" mode="out-in">
                <div :key="activeTabKey">
                    <!-- Render the slot matching the active tab key -->
                    <slot :name="activeTabKey" />
                </div>
            </transition>
        </div>

        <!-- Bottom navigation bar fixed to the bottom of the viewport -->
        <nav class="fixed inset-x-0 bottom-0 border-t border-gray-200 bg-white backdrop-blur-sm">
            <div class="max-w-md mx-auto px-4 py-3">
                <div class="relative flex bg-white rounded-full p-1">
                    <!-- Animated active tab background pill -->
                    <div class="absolute inset-y-1 w-1/2 rounded-full px-5 transition-transform duration-300 ease-out"
                        :style="{ transform: `translateX(${activeIndex * 100}%)` }">
                        <div class="bg-[#E0EDFF] h-full w-full rounded-full"></div>
                    </div>

                    <!-- Tabs -->
                    <BottomNavItem v-for="(tab, index) in tabs" :key="tab.key" class="flex-1" :label="tab.label"
                        :icon="tab.icon" :active="activeIndex === index" @click="selectTab(index)" />
                </div>
            </div>
        </nav>
    </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BottomNavItem from './BottomNavItem.vue'

const route = useRoute()
const router = useRouter()

const tabs = [
    { key: 'home', label: 'Home', icon: 'i-heroicons-home' },
    { key: 'settings', label: 'Settings', icon: 'i-heroicons-cog-6-tooth' }
] as const

const initialTab = tabs.findIndex(t => t.key === route.query.tab)
const activeIndex = ref(initialTab >= 0 ? initialTab : 0)
const activeTabKey = computed(() => tabs[activeIndex.value]?.key ?? 'home')

function selectTab(index: number) {
    if (index === activeIndex.value) return
    activeIndex.value = index
    router.replace({ query: { ...route.query, tab: tabs[index].key } })
}
</script>

<style scoped>
.slide-horizontal-enter-active,
.slide-horizontal-leave-active {
    transition: transform 0.25s ease, opacity 0.25s ease;
}

.slide-horizontal-enter-from {
    opacity: 0;
    transform: translateX(16px);
}

.slide-horizontal-enter-to {
    opacity: 1;
    transform: translateX(0);
}

.slide-horizontal-leave-from {
    opacity: 1;
    transform: translateX(0);
}

.slide-horizontal-leave-to {
    opacity: 0;
    transform: translateX(-16px);
}
</style>
