<template>
    <div class="w-full overflow-x-clip px-5 pb-7 pt-5 bg-white">
        <UCarousel v-if="memberships.length" v-slot="{ item }" :items="memberships" align="center" :ui="{
            viewport: 'overflow-visible',
            container: '-ms-4',
            item: 'basis-[99%] sm:basis-[76%] lg:basis-[62%] ps-4',
            dots: 'mt-3 flex justify-center gap-2',
            dot: 'size-2 rounded-full bg-gray-300 data-[state=active]:bg-[#3B82F6]'
        }" dots>
            <Card :title="item.store?.name || 'Membership'" :subtitle="tierLabel(item.tier)" :points="item.points"
                :valid-until="formatExpiry(item.expires_at)" :expired="item.is_expired" :membership-id="item.id" />
        </UCarousel>

        <!-- Empty state: not subscribed to any store yet. Matches a card's footprint. -->
        <div v-else
            class="w-full aspect-video rounded-[15px] border border-dashed border-gray-300 bg-gray-50 flex flex-col items-center justify-center text-center px-5">
            <img src="/img/logo.svg" alt="" class="w-24 h-auto mb-4 grayscale opacity-40" />
            <p class="text-sm font-semibold text-gray-700">No memberships yet</p>
            <p class="mt-1 text-xs text-gray-400">Subscribe to a store to start earning points.</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Membership } from "../composables/useApi";
import Card from "./Card.vue";

withDefaults(defineProps<{ memberships?: Membership[] }>(), {
    memberships: () => [],
});

const tierLabel = (tier?: string) =>
    tier ? tier.charAt(0).toUpperCase() + tier.slice(1) : "Membership";

const formatExpiry = (iso?: string | null) => {
    if (!iso) return "";
    const d = new Date(iso);
    return Number.isNaN(d.getTime())
        ? ""
        : d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
};
</script>
