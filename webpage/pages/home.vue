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
                    <MembershipCard :memberships="memberships" />

                    <!-- TotalPoint sticks just below the header -->
                    <div class="z-20 bg-white">
                        <TotalPoint :current="totalPoints" :total="pointsGoal" />
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

const showMyQr = ref(false);
const openMyQr = () => (showMyQr.value = true);

const { memberships, totalPoints, fetchProfile } = useProfile();
const notify = useNotify();

// Next 1,000-point milestone, used for the progress bar in TotalPoint.
const pointsGoal = computed(
    () => Math.max(1000, Math.ceil((totalPoints.value || 1) / 1000) * 1000),
);

onMounted(async () => {
    try {
        await fetchProfile();
    } catch (e: any) {
        notify.error(e?.error || "Could not load your profile");
    }
});
</script>
