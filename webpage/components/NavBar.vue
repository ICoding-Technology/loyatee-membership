<template>
  <header class="sticky top-0 z-30 bg-white border-b">
    <UContainer>
      <div class="flex items-center gap-3 py-4">
        <button
          type="button"
          class="inline-flex items-center justify-center w-7 h-7 rounded-full border border-gray-200 text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition"
          @click="onClose"
        >
          <UIcon name="i-heroicons-chevron-left" class="w-4 h-4" />
        </button>

        <h1 class="text-sm font-semibold text-gray-800 truncate">
          {{ title }}
        </h1>
      </div>
    </UContainer>
  </header>
</template>

<script lang="ts">
export default {
  name: "NavBar",
  props: {
    title: {
      type: String,
      default: "Detail",
    },
  },
  methods: {
    onClose() {
      if (this.$router) {
        this.$router.back();
      }
    },
  },
};
</script>

<style scoped></style>
