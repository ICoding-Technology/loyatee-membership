<template>
  <FormPageLayout>
    <template #header>
      <NavBar title="Edit Profile" />
    </template>

    <div class="avatar-section">
      <div class="avatar-wrapper" @click="browsePhoto">
        <div class="avatar">
          <span class="initials">{{ initials }}</span>
        </div>
        <div class="browse-icon">
          <UIcon name="i-heroicons-camera" class="w-3.5 h-3.5 text-white" />
        </div>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleFileChange"
        />
      </div>
      <p class="phone-label">+855 {{ phone || "—" }}</p>
    </div>

    <div class="form">
      <FormField label="First Name">
        <TextField v-model="firstName" placeholder="Enter first name" />
      </FormField>

      <FormField label="Last Name">
        <TextField v-model="lastName" placeholder="Enter last name" />
      </FormField>

      <FormField label="Email">
        <TextField v-model="email" type="email" placeholder="Enter email" />
      </FormField>
    </div>

    <template #bottom>
      <Button @click="handleSave"> Save Changes </Button>
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
      firstName: "Sowattana",
      lastName: "",
      email: "",
      phone: "123456789",
    };
  },
  computed: {
    initials(): string {
      const first = this.firstName?.[0] ?? "";
      const last = this.lastName?.[0] ?? "";
      return (first + last).toUpperCase();
    },
  },
  methods: {
    browsePhoto() {
      (this.$refs.fileInput as HTMLInputElement).click();
    },
    handleFileChange(event: Event) {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (file) {
        console.log("Selected file:", file.name);
      }
    },
    handleSave() {
      console.log("Profile saved:", {
        firstName: this.firstName,
        lastName: this.lastName,
        email: this.email,
      });
      this.$router.back();
    },
  },
};
</script>

<style scoped>
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 32px;
}

.phone-label {
  margin: 10px 0 0 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--color-primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
}

.browse-icon {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

.initials {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-primary);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
