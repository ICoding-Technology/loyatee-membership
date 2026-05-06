<template>
  <header class="bg-white border-b">
    <UContainer>
      <div class="flex items-center justify-between py-4 relative">
        <!-- User info section -->
        <div class="flex items-center gap-4 ml-4">
          <div
            class="w-10 h-10 bg-blue-200 rounded-full flex items-center justify-center overflow-hidden"
          >
            <img
              v-if="member?.avatar_url && !avatarFailed"
              :src="member.avatar_url"
              :alt="displayName"
              referrerpolicy="no-referrer"
              class="w-full h-full object-cover"
              @error="avatarFailed = true"
            />
            <span v-else class="text-blue-600 text-sm font-semibold">{{ initials }}</span>
          </div>
          <div>
            <h2 class="text-sm font-semibold text-gray-800">{{ displayName }}</h2>
            <p class="text-gray-500 text-xs">
              Account ID: <span class="font-number">{{ member?.account_id || "—" }}</span>
            </p>
          </div>
        </div>

        <!-- QR icon button on the right -->
        <button
          type="button"
          class="mr-1 inline-flex items-center justify-center rounded-full w-10 h-10 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          @click="$emit('qr-click')"
        >
          <UIcon name="i-heroicons-qr-code" class="w-7 h-7 text-black" />
        </button>
      </div>
    </UContainer>
  </header>
</template>

<script setup lang="ts">
import type { Member } from "../composables/useApi";

defineEmits(["qr-click"]);

const profileStore = useProfileStore();
const member = ref<Member | null>(null);
const avatarFailed = ref(false);

const displayName = computed(() => {
  const m = member.value;
  if (!m) return "Guest";
  return m.name || m.email || m.phone || "Member";
});

const initials = computed(() => {
  const name = displayName.value;
  const parts = name.trim().split(/\s+/);
  const first = parts[0]?.[0] ?? "";
  const last = parts.length > 1 ? parts[parts.length - 1][0] : "";
  return (first + last).toUpperCase() || "?";
});

onMounted(async () => {
  const stored = await profileStore.load();
  if (stored) member.value = stored;
});
</script>

<style scoped></style>
