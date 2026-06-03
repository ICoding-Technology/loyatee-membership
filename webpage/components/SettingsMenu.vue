<template>
  <div class="px-5 h-full">
    <!-- Profile Settings section -->
    <section>
      <h2 class="text-sm font-semibold text-[#1F2A3C] my-5 ml-2">
        Profile Settings
      </h2>
      <div
        class="overflow-hidden rounded-lg bg-white border border-gray-200 divide-y divide-gray-100"
      >
        <SettingsMenuItem label="Edit Profile" icon="i-heroicons-user" @click="goToEditProfile" />
        <SettingsMenuItem
          v-if="canChangePassword"
          label="Change password"
          icon="i-heroicons-key"
          @click="goToChangePassword"
        />
      </div>
    </section>

    <!-- Others section -->
    <section>
      <h2 class="text-sm font-semibold text-[#1F2A3C] my-5 ml-2">Others</h2>
      <div
        class="overflow-hidden rounded-lg bg-white border border-gray-200 divide-y divide-gray-100"
      >
        <SettingsMenuItem
          label="Terms &amp; Conditions"
          icon="i-heroicons-book-open"
          @click="goToTerms"
        />
        <SettingsMenuItem
          label="Privacy Policy"
          icon="i-heroicons-document-text"
          @click="goToPrivacy"
        />
      </div>
    </section>

    <!-- Account section -->
    <section>
      <h2 class="text-sm font-semibold text-[#1F2A3C] my-5 ml-2">Account</h2>
      <div
        class="overflow-hidden rounded-lg bg-white border border-gray-200 divide-y divide-gray-100"
      >
        <SettingsMenuItem
          label="Sign Out"
          icon="i-heroicons-arrow-right-on-rectangle"
          danger
          @click="handleSignOut"
        />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const goToEditProfile = () => {
  navigateTo("/edit-profile");
};

const goToChangePassword = () => {
  navigateTo("/change-password");
};

const goToTerms = () => {
  navigateTo("/term");
};

const goToPrivacy = () => {
  navigateTo("/privacy");
};

const profileStore = useProfileStore();
const signinType = ref<string | undefined>(undefined);
const canChangePassword = computed(() => signinType.value !== "google");

onMounted(async () => {
  const stored = await profileStore.load();
  signinType.value = stored?.signin_type;
});

const handleSignOut = async () => {
  await useApi().logout(); // revoke the refresh token server-side (best-effort)
  await clearAuthToken();
  await profileStore.clear();
  navigateTo("/login");
};

</script>
