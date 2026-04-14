<template>
  <p v-if="message" class="error-message">{{ message }}</p>
</template>

<script lang="ts">
export default {
  name: "ErrorMessage",
  props: {
    message: {
      type: String,
      default: "",
    },
  },
};
</script>

<style scoped>
.error-message {
  color: var(--color-error);
  font-size: 14px;
  text-align: center;
  margin: 10px 0 0 0;
}
</style>
