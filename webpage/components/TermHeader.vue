<template>
  <header class="sticky top-0 z-30 bg-white border-b">
    <UContainer>
      <div class="flex items-center justify-between py-4">
        <h1 class="text-base font-semibold text-gray-800">
          Terms &amp; Conditions
        </h1>

        <button
          type="button"
          class="inline-flex items-center justify-center w-9 h-9 rounded-full border border-gray-200 text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition"
          @click="handleClose"
        >
          <span class="sr-only">Close</span>
          <span class="text-lg leading-none">&times;</span>
        </button>
      </div>
    </UContainer>
  </header>
</template>

<script lang="ts">
export default {
  name: "TermHeader",
  emits: ["close"],
  methods: {
    handleClose() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
