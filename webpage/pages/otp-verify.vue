<template>
  <FormPageLayout>
    <template #header>
      <NavBar title="Verification" />
    </template>

    <h1 class="title">Enter OTP<br />verification code</h1>
    <p class="subtitle">We have sent the code to +855 {{ maskedPhone }}</p>

    <TextField
      v-model="otpCode"
      type="tel"
      placeholder="Enter OTP code"
      :maxlength="6"
      @update:model-value="handleOtpInput"
    />

    <template #bottom>
      <Button :disabled="!isValid || loading" @click="handleVerify">
        {{ loading ? "Verifying..." : "Verify OTP" }}
      </Button>

      <div class="resend-container">
        <p class="resend-text">
          Didn't receive the code?
          <button
            v-if="canResend"
            @click="handleResend"
            class="resend-link"
            type="button"
          >
            Resend
          </button>
          <span v-else class="resend-timer">Resend in <span class="font-number">{{ countdown }}</span>s</span>
        </p>
      </div>
    </template>
  </FormPageLayout>
</template>

<script lang="ts" setup>
if (getAuthToken()) navigateTo("/home");

const route = useRoute();
const router = useRouter();
const api = useApi();
const profileStore = useProfileStore();
const toast = useNotify();
const authRedirect = useAuthRedirect();

const otpCode = ref("");
const countdown = ref(60);
const canResend = ref(false);
const loading = ref(false);
let timerInterval: ReturnType<typeof setInterval> | null = null;

const phoneDigits = computed(() => (route.query.phone as string) || "");
const fullPhone = computed(() => "+855" + phoneDigits.value);

const maskedPhone = computed(() => {
  const phone = phoneDigits.value || "123456789";
  return phone.substring(0, 3) + "***" + phone.substring(6);
});

const isValid = computed(() => otpCode.value.length === 6);

const startCountdown = () => {
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--;
    } else {
      canResend.value = true;
      if (timerInterval) clearInterval(timerInterval);
    }
  }, 1000);
};

const handleOtpInput = () => {
  otpCode.value = otpCode.value.replace(/\D/g, "").slice(0, 6);
};

const handleVerify = async () => {
  if (!isValid.value || loading.value) return;
  loading.value = true;
  try {
    const res = await api.verifyOtp(fullPhone.value, otpCode.value);
    await setAuthToken(res.token);
    const profile = await api.getProfile();
    await profileStore.save(profile.member);
    // New users finish onboarding at /setup-account, which then honors any
    // pending redirect. Existing users resume their redirect immediately.
    router.replace(res.is_new ? "/setup-account" : authRedirect.consume() || "/home");
  } catch (e: any) {
    toast.error(e?.error || "Verification failed. Please try again.");
  } finally {
    loading.value = false;
  }
};

const handleResend = async () => {
  if (!canResend.value) return;
  try {
    const res = await api.requestOtp(fullPhone.value);
    if (res.otp_debug) console.log("[dev] OTP:", res.otp_debug);
    otpCode.value = "";
    countdown.value = 60;
    canResend.value = false;
    startCountdown();
    toast.info("Code sent.");
  } catch (e: any) {
    toast.error(e?.error || "Could not resend OTP.");
  }
};

onMounted(startCountdown);
onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval);
});
</script>

<style scoped>
.title {
  margin: 0 0 12px 0;
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1.3;
}

.subtitle {
  margin: 0 0 40px 0;
  font-size: 14px;
  color: var(--color-text-muted);
}

.resend-container {
  margin-top: 16px;
}

.resend-text {
  font-size: 14px;
  color: var(--color-text-secondary);
  text-align: center;
  margin: 0;
}

.resend-link {
  background: none;
  border: none;
  color: var(--color-primary);
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-left: 4px;
  font-size: 14px;
}

.resend-link:active {
  opacity: 0.7;
}

.resend-timer {
  color: var(--color-text-muted);
  margin-left: 4px;
  font-weight: 600;
}
</style>
