<template>
  <Teleport to="body">
    <transition name="myqr-fade">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-40 flex flex-col justify-end bg-black/40"
        @click.self="close"
      >
        <transition name="myqr-slide-up" appear>
          <div
            class="bg-white rounded-t-2xl shadow-xl p-5 pt-4 max-h-[80vh] w-full mx-auto"
          >
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-sm font-semibold text-gray-900">My QR Code</h2>
              <button
                type="button"
                class="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-gray-100 text-gray-500"
                @click="close"
              >
                <span class="sr-only">Close</span>
                <span class="text-xl leading-none">&times;</span>
              </button>
            </div>

            <div class="flex flex-col items-center justify-center py-4">
              <div
                class="w-40 h-40 rounded-2xl border border-gray-200 flex items-center justify-center bg-gray-50"
              >
                <!-- Placeholder QR area -->
                <UIcon
                  name="i-heroicons-qr-code"
                  class="w-16 h-16 text-gray-400"
                />
              </div>
              <p class="mt-4 text-xs text-gray-500 text-center">
                Present this QR code at participating stores to earn or redeem
                points.
              </p>
            </div>
          </div>
        </transition>
      </div>
    </transition>
  </Teleport>
</template>

<script lang="ts">
export default {
  name: "MyQR",
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  methods: {
    close() {
      this.$emit("update:modelValue", false);
    },
  },
};
</script>

<style scoped>
.myqr-fade-enter-active,
.myqr-fade-leave-active {
  transition: opacity 0.2s ease-out;
}

.myqr-fade-enter-from,
.myqr-fade-leave-to {
  opacity: 0;
}

.myqr-slide-up-enter-active,
.myqr-slide-up-leave-active {
  transition: transform 0.3s ease-out, opacity 0.3s ease-out;
}

.myqr-slide-up-enter-from,
.myqr-slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
