<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Logo -->
      <div class="logo-section">
        <img src="/img/logo.svg" alt="Loyatee Logo" class="logo" />
      </div>

      <!-- Brand -->
      <h1 class="brand-name">Loyatee</h1>
      <p class="brand-tagline">Your loyalty, your rewards.<br />All in one place.</p>

      <!-- Buttons -->
      <div class="bottom-section">
        <Button @click="goToRegister">
          Let's get started
        </Button>

        <button type="button" class="btn-outline" @click="goToHome">
          I already have an account
        </button>

        <p class="terms-text">
          By continuing, you agree to Loyatee's<br />
          <a href="/term">Terms of Service</a> and <a href="/privacy">Privacy Policy</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  methods: {
    goToRegister() {
      this.$router.push("/register");
    },
    goToHome() {
      this.$router.push("/home");
    },
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  background: #ffffff;
  min-height: 100vh;
  min-height: 100dvh;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  min-height: 100dvh;
}

.logo-section {
  margin-top: 80px;
}

.logo {
  width: 120px;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(65, 105, 225, 0.2));
}

.brand-name {
  margin: 32px 0 0 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--color-primary);
}

.brand-tagline {
  margin: 12px 0 0 0;
  font-size: 14px;
  color: var(--color-text-muted);
  text-align: center;
  line-height: 1.5;
}

.bottom-section {
  margin-top: auto;
  width: 100%;
  padding-bottom: calc(20px + env(safe-area-inset-bottom));
}

.btn-outline {
  width: 100%;
  height: 48px;
  background: transparent;
  color: var(--color-text);
  border: 1.5px solid var(--color-border);
  border-radius: 5px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 12px;
  transition: background 0.2s;
}

.btn-outline:active {
  background: #f5f5f5;
}

.terms-text {
  margin-top: 20px;
  font-size: 12px;
  color: var(--color-text-muted);
  text-align: center;
  line-height: 1.5;
}

.terms-text a {
  color: var(--color-text);
  font-weight: 600;
  text-decoration: underline;
}
</style>
