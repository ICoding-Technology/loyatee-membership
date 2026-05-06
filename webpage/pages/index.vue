<template>
  <div class="splash-screen">
    <div class="content">
      <div class="logo">
        <img src="/img/logo.svg" alt="Logo" />
      </div>
      <div class="loading">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
onMounted(() => {
  setTimeout(() => {
    navigateTo(getAuthToken() ? '/home' : '/login')
  }, 2000)
})
</script>

<style scoped>
.splash-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #fff;
}

.content {
  margin-top: -150px;
  text-align: center;
}

.logo {
  margin-bottom: 50px;
}

.logo img {
  width: 120px;
  height: auto;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

.loading {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.dot {
  width: 12px;
  height: 12px;
  background-color: rgb(56, 119, 207);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.7;
  }

  40% {
    transform: translateY(-20px);
    opacity: 1;
  }
}
</style>
