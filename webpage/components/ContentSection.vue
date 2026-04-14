<template>
  <section class="space-y-2">
    <h2 class="text-sm font-semibold text-gray-900">{{ title }}</h2>
    <p>{{ content }}</p>
  </section>
</template>

<script lang="ts">
export default {
  name: "ContentSection",
  props: {
    title: {
      type: String,
      required: true,
    },
    content: {
      type: String,
      required: true,
    },
  },
};
</script>
