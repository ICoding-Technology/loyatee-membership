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

    <ErrorMessage :message="errorMessage" />

    <template #bottom>
      <Button :disabled="!isValid" @click="handleVerify">
        Verify OTP
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

<script lang="ts">
export default {
  data() {
    return {
      otpCode: "",
      errorMessage: "",
      countdown: 60,
      canResend: false,
      timerInterval: null as number | null,
    };
  },
  computed: {
    maskedPhone(): string {
      const phone = (this.$route.query.phone as string) || "123456789";
      return phone.substring(0, 3) + "***" + phone.substring(6);
    },
    isValid(): boolean {
      return this.otpCode.length === 6;
    },
  },
  mounted() {
    this.startCountdown();
  },
  beforeUnmount() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
  },
  methods: {
    handleOtpInput() {
      this.otpCode = this.otpCode.replace(/\D/g, "").slice(0, 6);
      this.errorMessage = "";
    },
    handleVerify() {
      if (this.isValid) {
        console.log("OTP submitted:", this.otpCode);
        this.$router.push("/home");
      }
    },
    handleResend() {
      if (this.canResend) {
        console.log("Resending OTP...");
        this.otpCode = "";
        this.errorMessage = "";
        this.countdown = 60;
        this.canResend = false;
        this.startCountdown();
      }
    },
    startCountdown() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
      }
      this.timerInterval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          this.canResend = true;
          if (this.timerInterval) {
            clearInterval(this.timerInterval);
          }
        }
      }, 1000) as unknown as number;
    },
  },
};
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
