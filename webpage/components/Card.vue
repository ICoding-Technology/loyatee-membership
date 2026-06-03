<template>
    <div
        class="relative w-full aspect-video rounded-[15px] bg-gradient-to-br from-[#4C86E5] to-[#3B5FD4] shadow-md px-4 py-3 md:px-10 md:py-8 overflow-hidden text-white cursor-pointer"
        @click="$router.push(membershipId ? { path: '/card-detail', query: { id: membershipId } } : '/card-detail')">

        <!-- Content -->
        <div class="relative z-10 flex h-full flex-col justify-between">
            <!-- Logo + title -->
            <div class="flex items-center gap-2">
                <!-- Logo -->
                <div class="flex h-14 w-14 items-center justify-center rounded-full bg-white/0">
                    <img src="/img/watermark-logo.svg" alt="Loyatee Logo" class="h-12 w-12 object-contain" />
                </div>

                <!-- Vertical separator -->
                <div class="h-10 w-px bg-white/25"></div>

                <!-- Text -->
                <div class="flex flex-col justify-center ml-2">
                    <h3 class="font-semibold tracking-wide text-sm">{{ title }}</h3>
                    <p class="mt-1 text-white/80 text-xs">{{ subtitle }}</p>
                </div>
            </div>

            <!-- Bottom row: points (left) + expiry/expired (right) -->
            <div class="mt-12 flex items-end justify-between text-white/80 text-xs">
                <div v-if="points !== null">
                    <span class="font-semibold text-white font-number">{{ points.toLocaleString() }}</span>
                    <span> Points</span>
                </div>
                <div v-if="expired" class="font-semibold text-red-200">Expired</div>
                <div v-else-if="validUntil" class="text-right">
                    <span>Valid until </span>
                    <span class="font-semibold text-white">{{ validUntil }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    name: 'Card',
    props: {
        title: {
            type: String,
            default: 'Loyatee'
        },
        subtitle: {
            type: String,
            default: 'Membership'
        },
        validUntil: {
            type: String,
            default: ''
        },
        points: {
            type: Number,
            default: null
        },
        expired: {
            type: Boolean,
            default: false
        },
        membershipId: {
            type: String,
            default: ''
        }
    }
}
</script>

<style scoped></style>
