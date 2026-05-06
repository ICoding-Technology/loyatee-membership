<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Top navigation bar with back button -->
    <NavBar title="Transaction Detail" />
    <ProfileInfo name="Ava Martinez" email="fitava.martinez@gmail.com" />
    <!-- Content -->
    <main class="flex-1">
      <UContainer class="py-6 space-y-6 text-sm text-gray-700">
        <!-- Membership overview card -->
        <section>
          <div
            class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 flex flex-col gap-4"
          >
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-sm font-semibold text-gray-900">
                  Membership overview
                </h2>
                <p class="text-xs text-gray-500 mt-0.5">
                  You are progressing through the loyalty levels.
                </p>
              </div>
              <span
                class="inline-flex items-center rounded-full bg-blue-50 px-3 py-1 text-[11px] font-medium text-blue-600"
              >
                3 levels • 8 rewards
              </span>
            </div>

            <!-- Levels progress -->
            <div class="grid grid-cols-3 gap-3 mt-1">
              <div class="flex flex-col items-start gap-1">
                <span class="text-[11px] uppercase tracking-wide text-gray-400">
                  Current level
                </span>
                <span class="text-sm font-semibold text-gray-900">Silver</span>
                <span class="text-[11px] text-gray-500">1,200 pts</span>
              </div>
              <div class="flex flex-col items-start gap-1">
                <span class="text-[11px] uppercase tracking-wide text-gray-400">
                  Next level
                </span>
                <span class="text-sm font-semibold text-gray-900">Gold</span>
                <span class="text-[11px] text-gray-500">800 pts to go</span>
              </div>
              <div class="flex flex-col items-start gap-1">
                <span class="text-[11px] uppercase tracking-wide text-gray-400">
                  Total rewards
                </span>
                <span class="text-sm font-semibold text-gray-900">8</span>
                <span class="text-[11px] text-gray-500">3 unused</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Rewards list -->
        <section class="space-y-3">
          <h3
            class="text-xs font-semibold text-gray-500 uppercase tracking-wide"
          >
            Available rewards
          </h3>
          <div class="space-y-2">
            <div
              class="flex items-center justify-between rounded-xl bg-white border border-gray-100 px-4 py-3"
            >
              <div class="flex flex-col">
                <span class="text-sm font-medium text-gray-900">
                  10% off next purchase
                </span>
                <span class="text-[11px] text-gray-500">
                  Expires in 5 days • Gold &amp; above
                </span>
              </div>
              <span
                class="text-[11px] font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full"
              >
                Ready to use
              </span>
            </div>

            <div
              class="flex items-center justify-between rounded-xl bg-white border border-gray-100 px-4 py-3"
            >
              <div class="flex flex-col">
                <span class="text-sm font-medium text-gray-900">
                  Free drink voucher
                </span>
                <span class="text-[11px] text-gray-500">
                  Valid any day • Silver &amp; above
                </span>
              </div>
              <span
                class="text-[11px] font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-full"
              >
                2 left
              </span>
            </div>
          </div>
        </section>
      </UContainer>
    </main>
  </div>
</template>

<script setup lang="ts">
if (!getAuthToken()) navigateTo("/login");
</script>
