<template>
  <div class="flex items-center gap-3">
    <!-- Avatar -->
    <div class="shrink-0">
      <div
        v-if="avatarUrl"
        class="w-11 h-11 rounded-full overflow-hidden bg-gray-200"
      >
        <img :src="avatarUrl" :alt="name" class="w-full h-full object-cover" />
      </div>
      <div
        v-else
        class="w-11 h-11 rounded-full bg-gray-200 flex items-center justify-center text-sm font-semibold text-gray-700"
      >
        {{ initials }}
      </div>
    </div>

    <!-- Name & email -->
    <div class="flex flex-col">
      <span class="text-sm font-semibold text-gray-900 leading-tight">
        {{ name }}
      </span>
      <span class="text-xs text-gray-500 leading-tight">
        {{ email }}
      </span>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: "ProfileInfo",
  props: {
    name: {
      type: String,
      default: "",
    },
    email: {
      type: String,
      default: "",
    },
    avatarUrl: {
      type: String,
      default: "",
    },
  },
  computed: {
    initials(): string {
      if (!this.name) return "";
      const parts = this.name.trim().split(/\s+/);
      const first = parts[0]?.[0] ?? "";
      const last = parts.length > 1 ? parts[parts.length - 1][0] : "";
      return (first + last).toUpperCase();
    },
  },
};
</script>

<style scoped></style>
