<template>
  <FormPageLayout>
    <template #header>
      <NavBar title="Change Password" />
    </template>

    <div class="form">
      <FormField label="Current Password">
        <TextField
          v-model="currentPassword"
          type="password"
          placeholder="Enter current password"
        />
      </FormField>

      <FormField label="New Password">
        <TextField
          v-model="newPassword"
          type="password"
          placeholder="Enter new password"
        />
      </FormField>

      <FormField label="Confirm Password">
        <TextField
          v-model="confirmPassword"
          type="password"
          placeholder="Confirm new password"
        />
      </FormField>

      <ErrorMessage :message="errorMessage" />
    </div>

    <template #bottom>
      <Button :disabled="!isValid" @click="handleSave">
        Update Password
      </Button>
    </template>
  </FormPageLayout>
</template>

<script setup lang="ts">
if (!getAuthToken()) navigateTo("/login");
</script>

<script lang="ts">
export default {
  data() {
    return {
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
      errorMessage: "",
    };
  },
  computed: {
    isValid(): boolean {
      return (
        this.currentPassword.length > 0 &&
        this.newPassword.length >= 6 &&
        this.confirmPassword.length > 0
      );
    },
  },
  methods: {
    handleSave() {
      if (this.newPassword !== this.confirmPassword) {
        this.errorMessage = "Passwords do not match";
        return;
      }
      this.errorMessage = "";
      console.log("Password changed");
      this.$router.back();
    },
  },
};
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
