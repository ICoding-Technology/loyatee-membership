<template>
    <div class="px-5 h-full">
        <!-- Profile Settings section -->
        <section>
            <h2 class="text-sm font-semibold text-[#1F2A3C] my-5 ml-2">Profile Settings</h2>
            <div class="overflow-hidden rounded-lg bg-white border border-gray-200 divide-y divide-gray-100">
                <SettingsMenuItem label="Edit Profile" icon="i-heroicons-user" />
                <SettingsMenuItem label="Change password" icon="i-heroicons-key" />
            </div>
        </section>

        <!-- Others section -->
        <section>
            <h2 class="text-sm font-semibold text-[#1F2A3C] my-5 ml-2">Others</h2>
            <div class="overflow-hidden rounded-lg bg-white border border-gray-200 divide-y divide-gray-100">
                <SettingsMenuItem label="Terms &amp; Conditions" icon="i-heroicons-book-open" />
                <SettingsMenuItem label="Privacy Policy" icon="i-heroicons-document-text" />
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import SettingsMenuItem from './SettingsMenuItem.vue'
</script>
