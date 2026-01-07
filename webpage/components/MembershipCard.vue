<template>
    <div class="w-full overflow-x-clip px-5 pb-7 pt-5 bg-white">
        <UCarousel v-slot="{ item }" :items="cards" align="center" :ui="{
            viewport: 'overflow-visible',
            container: '-ms-4',
            item: 'basis-[99%] sm:basis-[76%] lg:basis-[62%] ps-4',
            dots: 'mt-3 flex justify-center gap-2',
            dot: 'size-2 rounded-full bg-gray-300 data-[state=active]:bg-[#3B82F6]'
        }" dots>
            <Card :title="item.title" :subtitle="item.subtitle" :valid-until="item.validUntil" />
        </UCarousel>
    </div>
</template>

<script lang="ts">
import Card from './Card.vue'

export default {
    name: 'MembershipCard',
    components: {
        Card
    },
    data() {
        return {
            cards: [
                {
                    title: 'Loyatee',
                    subtitle: 'Membership',
                    validUntil: '12 July 2023'
                },
                {
                    title: 'Loyatee',
                    subtitle: 'Premium',
                    validUntil: '31 Dec 2025'
                },
                {
                    title: 'Loyatee',
                    subtitle: 'VIP',
                    validUntil: '15 March 2026'
                },
                {
                    title: 'Loyatee',
                    subtitle: 'Gold',
                    validUntil: '20 June 2026'
                },
                {
                    title: 'Loyatee',
                    subtitle: 'Platinum',
                    validUntil: '10 August 2026'
                }
            ]
        }
    }
}
</script>
