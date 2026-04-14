<template>
  <div class="form-page">
    <slot name="header" />
    <div class="form-page-content">
      <div class="form-page-container">
        <slot />
        <div class="form-page-bottom">
          <slot name="bottom" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: "FormPageLayout",
};
</script>

<style scoped>
.form-page {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  min-height: 100vh;
  min-height: 100dvh;
}

.form-page-content {
  flex: 1;
  display: flex;
  justify-content: center;
}

.form-page-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.form-page-bottom {
  margin-top: auto;
  padding-bottom: calc(20px + env(safe-area-inset-bottom));
}
</style>
