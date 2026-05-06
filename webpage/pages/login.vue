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

      <!-- Phone field -->
      <div class="phone-section">
        <TextField
          v-model="phoneNumber"
          type="tel"
          placeholder="Enter phone number"
          :maxlength="9"
          @update:model-value="handlePhoneInput"
        >
          <template #prefix>+855</template>
        </TextField>
        <ErrorMessage :message="errorMessage" />
      </div>

      <!-- Buttons -->
      <div class="bottom-section">
        <Button :disabled="!isValid || loading" @click="handleSignIn">
          {{ loading ? "Sending..." : "Sign In" }}
        </Button>

        <div class="divider">
          <span>or continue with</span>
        </div>

        <div class="social-buttons">
          <button
            v-if="googleClientId"
            type="button"
            class="btn-google"
            :disabled="googleLoading"
            @click="handleGoogleSignIn"
          >
            <svg class="btn-google-icon" viewBox="0 0 18 18" aria-hidden="true">
              <path fill="#4285F4" d="M17.64 9.2c0-.64-.06-1.25-.16-1.84H9v3.48h4.84a4.14 4.14 0 0 1-1.79 2.72v2.26h2.9c1.7-1.57 2.69-3.88 2.69-6.62z"/>
              <path fill="#34A853" d="M9 18c2.43 0 4.46-.8 5.95-2.18l-2.9-2.26c-.8.54-1.83.86-3.05.86-2.34 0-4.32-1.58-5.03-3.7H.96v2.33A9 9 0 0 0 9 18z"/>
              <path fill="#FBBC05" d="M3.97 10.72A5.4 5.4 0 0 1 3.68 9c0-.6.1-1.18.29-1.72V4.95H.96A9 9 0 0 0 0 9c0 1.45.35 2.83.96 4.05l3.01-2.33z"/>
              <path fill="#EA4335" d="M9 3.58c1.32 0 2.51.45 3.44 1.35l2.58-2.58A9 9 0 0 0 9 0 9 9 0 0 0 .96 4.95l3.01 2.33C4.68 5.16 6.66 3.58 9 3.58z"/>
            </svg>
            <span>{{ googleLoading ? "Signing in..." : "Continue with Google" }}</span>
          </button>

          <div ref="telegramBtnRef" class="social-btn-wrap"></div>

          <p v-if="!googleClientId && !telegramBotName" class="social-hint">
            Set <code>NUXT_PUBLIC_GOOGLE_CLIENT_ID</code> and <code>NUXT_PUBLIC_TELEGRAM_BOT_NAME</code> to enable social sign-in.
          </p>
        </div>

        <p class="signup-text">
          Don't have an account?
          <a href="#" @click.prevent="goToRegister">Sign up</a>
        </p>

        <p class="terms-text">
          By continuing, you agree to Loyatee's<br />
          <a href="/term">Terms of Service</a> and <a href="/privacy">Privacy Policy</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
if (getAuthToken()) navigateTo("/home");

const router = useRouter();
const api = useApi();
const profileStore = useProfileStore();
const { public: { googleClientId, telegramBotName } } = useRuntimeConfig();

const phoneNumber = ref("");
const errorMessage = ref("");
const loading = ref(false);
const telegramBtnRef = ref<HTMLElement | null>(null);
const googleLoading = ref(false);
let googleTokenClient: any = null;

const isValid = computed(() => phoneNumber.value.length >= 8);

const handlePhoneInput = () => {
  phoneNumber.value = phoneNumber.value.replace(/\D/g, "").slice(0, 9);
  if (phoneNumber.value.startsWith("0")) {
    errorMessage.value = "Phone number cannot start with 0";
    phoneNumber.value = phoneNumber.value.replace(/^0+/, "");
  } else {
    errorMessage.value = "";
  }
};

const handleSignIn = async () => {
  if (!isValid.value || loading.value) return;
  errorMessage.value = "";
  loading.value = true;
  const fullPhone = "+855" + phoneNumber.value;
  try {
    const res = await api.requestOtp(fullPhone);
    if (res.otp_debug) console.log("[dev] OTP:", res.otp_debug);
    router.push({ path: "/otp-verify", query: { phone: phoneNumber.value } });
  } catch (e: any) {
    errorMessage.value = e?.error || "Could not send OTP. Please try again.";
  } finally {
    loading.value = false;
  }
};

const goToRegister = () => router.push("/register");

// --- Google Sign-In (custom button → OAuth token popup) ---
const initGoogle = () => {
  const w = window as any;
  if (!googleClientId || !w.google?.accounts?.oauth2) return;
  googleTokenClient = w.google.accounts.oauth2.initTokenClient({
    client_id: googleClientId,
    scope: "openid email profile",
    callback: async (resp: { access_token?: string; error?: string }) => {
      googleLoading.value = false;
      if (resp.error || !resp.access_token) {
        errorMessage.value = resp.error || "Google sign-in cancelled.";
        return;
      }
      try {
        const res = await api.signInWithGoogle({ access_token: resp.access_token });
        await setAuthToken(res.token);
        const profile = await api.getProfile();
        await profileStore.save(profile.member);
        router.push("/home");
      } catch (e: any) {
        errorMessage.value = e?.error || "Google sign-in failed.";
      }
    },
  });
};

const handleGoogleSignIn = () => {
  errorMessage.value = "";
  if (!googleTokenClient) {
    errorMessage.value = "Google sign-in is still loading — try again.";
    return;
  }
  googleLoading.value = true;
  googleTokenClient.requestAccessToken({ prompt: "select_account" });
};

// --- Telegram Sign-In ---
// Telegram's widget injects its own iframe button next to the <script> tag.
// We append the script into our container ref so the iframe lands there.
const initTelegram = () => {
  if (!telegramBotName || !telegramBtnRef.value) return;

  (window as any).onTelegramAuth = async (user: Record<string, unknown>) => {
    errorMessage.value = "";
    try {
      const res = await api.signInWithTelegram(user);
      await setAuthToken(res.token);
      const profile = await api.getProfile();
      await profileStore.save(profile.member);
      router.push("/home");
    } catch (e: any) {
      errorMessage.value = e?.error || "Telegram sign-in failed.";
    }
  };

  const script = document.createElement("script");
  script.async = true;
  script.src = "https://telegram.org/js/telegram-widget.js?22";
  script.setAttribute("data-telegram-login", telegramBotName);
  script.setAttribute("data-size", "large");
  script.setAttribute("data-onauth", "onTelegramAuth(user)");
  script.setAttribute("data-request-access", "write");
  telegramBtnRef.value.appendChild(script);
};

onMounted(() => {
  if (googleClientId) {
    const start = Date.now();
    const tryInit = () => {
      if ((window as any).google?.accounts?.id) {
        initGoogle();
      } else if (Date.now() - start < 5000) {
        setTimeout(tryInit, 100);
      }
    };
    tryInit();
  }

  initTelegram();
});
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
  margin-top: 48px;
}

.logo {
  width: 96px;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(65, 105, 225, 0.2));
}

.brand-name {
  margin: 20px 0 0 0;
  font-size: 26px;
  font-weight: 700;
  color: var(--color-primary);
}

.brand-tagline {
  margin: 6px 0 0 0;
  font-size: 13px;
  color: var(--color-text-muted);
  text-align: center;
  line-height: 1.5;
}

.phone-section {
  width: 100%;
  margin-top: 32px;
}

.bottom-section {
  margin-top: auto;
  width: 100%;
  padding-bottom: calc(20px + env(safe-area-inset-bottom));
}

.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0 16px;
  color: var(--color-text-muted);
  font-size: 12px;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

.social-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-google {
  width: 100%;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: 5px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, box-shadow 0.15s;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.btn-google:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #d4d8de;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.btn-google:active:not(:disabled) {
  background: #f3f4f6;
  box-shadow: none;
}

.btn-google:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-google-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.social-btn-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
  min-height: 40px;
}

.social-hint {
  font-size: 12px;
  color: var(--color-text-muted);
  text-align: center;
  margin: 0;
  line-height: 1.5;
}

.social-hint code {
  background: #f5f5f5;
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 11px;
}

.signup-text {
  margin: 16px 0 0 0;
  font-size: 14px;
  color: var(--color-text-secondary);
  text-align: center;
}

.signup-text a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  margin-left: 4px;
}

.terms-text {
  margin-top: 16px;
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
