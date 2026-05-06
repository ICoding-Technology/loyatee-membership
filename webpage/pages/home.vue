<template>
    <div class="bg-white flex flex-col overflow-x-hidden">
        <!-- Sticky header at the very top -->
        <div class="sticky top-0 z-30 bg-white">
            <Header @qr-click="openMyQr" />
        </div>
        <BottomNavigation>
            <template #home>

                <div class="flex flex-col bg-gray-100">
                    <!-- Membership card scrolls normally under the header -->
                    <MembershipCard />

                    <!-- TotalPoint sticks just below the header -->
                    <div class="z-20 bg-white">
                        <TotalPoint :current="200" :total="1000" />
                    </div>

                    <!-- Transaction list scrolls behind the sticky sections -->
                    <TransactionList />
                </div>
            </template>

            <template #settings>
                <SettingsMenu />
            </template>
        </BottomNavigation>
        <!-- MyQR action sheet -->
        <MyQR v-model="showMyQr" />
    </div>
</template>

<script setup lang="ts">
if (!getAuthToken()) navigateTo("/login");
</script>

<script lang="ts">
export default {
    data() {
        return {
            showMyQr: false,
        };
    },
    methods: {
        openMyQr() {
            this.showMyQr = true;
        },
    },
};
</script>
