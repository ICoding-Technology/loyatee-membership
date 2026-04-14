<template>
  <header class="bg-white border-b">
    <UContainer>
      <div class="flex items-center justify-between py-4 relative">
        <!-- User info section -->
        <div class="flex items-center gap-4 ml-4">
          <div
            class="w-10 h-10 bg-blue-200 rounded-full flex items-center justify-center"
          >
            <span class="text-blue-600 text-sm font-semibold">SW</span>
          </div>
          <div>
            <h2 class="text-sm font-semibold text-gray-800">Sowattana</h2>
            <p class="text-gray-500 text-xs">Account ID: <span class="font-number">123456</span></p>
          </div>
        </div>

        <!-- QR icon button on the right -->
        <button
          type="button"
          class="mr-1 inline-flex items-center justify-center rounded-full w-10 h-10 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          @click="handleQrClick"
        >
          <UIcon name="i-heroicons-qr-code" class="w-7 h-7 text-black" />
        </button>
      </div>
    </UContainer>
  </header>
</template>

<script lang="ts">
export default {
  name: "Header",
  props: {
    qrClick: {
      type: Function,
      required: false,
    },
  },
  emits: ["qr-click"],
  methods: {
    handleQrClick() {
      if (this.qrClick) {
        this.qrClick();
      } else {
        this.$emit("qr-click");
      }
    },
  },
};
</script>

<style scoped></style>
