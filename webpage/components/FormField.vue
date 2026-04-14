<template>
  <div class="form-field">
    <label class="form-field-label">{{ label }}</label>
    <slot />
  </div>
</template>

<script lang="ts">
export default {
  name: "FormField",
  props: {
    label: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-field-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}
</style>
