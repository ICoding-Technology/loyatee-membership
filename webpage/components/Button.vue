<template>
  <button
    class="btn"
    :class="{ disabled: disabled }"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script lang="ts">
export default {
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["click"],
};
</script>

<style scoped>
.btn {
  width: 100%;
  height: 48px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn:active:not(:disabled) {
  opacity: 0.8;
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
