<template>
  <FormPageLayout>
    <template #header>
      <NavBar title="Sign Up" />
    </template>

    <h1 class="title">Enter your<br />mobile number</h1>
    <p class="subtitle">We will send you confirmation code</p>

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

    <template #bottom>
      <Button :disabled="!isValid || loading" @click="handleNext">
        {{ loading ? "Sending..." : "Get OTP Verification" }}
      </Button>

      <p class="terms-text">
        By continuing, you agree to our<br />
        <a href="#">Terms & Conditions</a> and <a href="#">Privacy Policy</a>
      </p>
    </template>
  </FormPageLayout>
</template>

<script lang="ts" setup>
if (getAuthToken()) navigateTo("/home");

const router = useRouter();
const api = useApi();

const phoneNumber = ref("");
const errorMessage = ref("");
const loading = ref(false);

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

const handleNext = async () => {
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

.terms-text {
  margin-top: 20px;
  font-size: 12px;
  color: var(--color-text-muted);
  text-align: center;
  line-height: 1.5;
}

.terms-text a {
  color: var(--color-primary);
  text-decoration: none;
}
</style>
