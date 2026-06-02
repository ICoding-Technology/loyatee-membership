<template>
  <FormPageLayout>
    <template #header>
      <NavBar title="Set up account" :back="false" />
    </template>

    <h1 class="title">Welcome!<br />Tell us about you</h1>
    <p class="subtitle">Just a few details so we can personalise your experience.</p>

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
      <Button :disabled="!isValid || saving" @click="handleContinue">
        {{ saving ? "Saving..." : "Continue" }}
      </Button>
    </template>
  </FormPageLayout>
</template>

<script lang="ts" setup>
if (!getAuthToken()) navigateTo("/login");

const router = useRouter();
const api = useApi();
const profileStore = useProfileStore();
const toast = useNotify();
const authRedirect = useAuthRedirect();

const memberId = ref<string | null>(null);
const firstName = ref("");
const lastName = ref("");
const email = ref("");
const saving = ref(false);

const isValid = computed(
  () => firstName.value.trim().length > 0 && lastName.value.trim().length > 0,
);

const handleContinue = async () => {
  if (!isValid.value || saving.value) return;
  if (!memberId.value) {
    toast.error("Profile not loaded yet.");
    return;
  }
  saving.value = true;
  const name = [firstName.value.trim(), lastName.value.trim()]
    .filter(Boolean)
    .join(" ");
  try {
    const updated = await api.updateMember(memberId.value, {
      name,
      email: email.value.trim(),
    });
    await profileStore.save(updated);
    toast.success("Account ready.");
    router.replace(authRedirect.consume() || "/home");
  } catch (e: any) {
    toast.error(e?.error || "Could not save your details.");
  } finally {
    saving.value = false;
  }
};

onMounted(async () => {
  const stored = await profileStore.load();
  if (!stored) {
    try {
      const { member } = await api.getProfile();
      memberId.value = member.id;
      await profileStore.save(member);
    } catch (e: any) {
      toast.error(e?.error || "Could not load profile.");
    }
    return;
  }
  memberId.value = stored.id;
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
  margin: 0 0 32px 0;
  font-size: 14px;
  color: var(--color-text-muted);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
