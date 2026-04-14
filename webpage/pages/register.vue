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
      <Button :disabled="!isValid" @click="handleNext">
        Get OTP Verification
      </Button>

      <p class="terms-text">
        By continuing, you agree to our<br />
        <a href="#">Terms & Conditions</a> and <a href="#">Privacy Policy</a>
      </p>
    </template>
  </FormPageLayout>
</template>

<script lang="ts">
export default {
  data() {
    return {
      phoneNumber: "",
      errorMessage: "",
    };
  },
  computed: {
    isValid(): boolean {
      return this.phoneNumber.length >= 8;
    },
  },
  methods: {
    handlePhoneInput() {
      this.phoneNumber = this.phoneNumber.replace(/\D/g, "").slice(0, 9);

      if (this.phoneNumber.startsWith("0")) {
        this.errorMessage = "Phone number cannot start with 0";
        this.phoneNumber = this.phoneNumber.replace(/^0+/, "");
      } else {
        this.errorMessage = "";
      }
    },
    handleNext() {
      if (this.isValid) {
        console.log("Phone number submitted:", "+855" + this.phoneNumber);
        this.$router.push({
          path: "/otp-verify",
          query: { phone: this.phoneNumber },
        });
      }
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
