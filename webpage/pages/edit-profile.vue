<template>
  <FormPageLayout>
    <template #header>
      <NavBar title="Edit Profile" />
    </template>

    <div class="avatar-section">
      <div class="avatar-wrapper" @click="browsePhoto">
        <div class="avatar">
          <img
            v-if="avatarUrl"
            :src="avatarUrl"
            alt="Avatar"
            class="avatar-img"
            referrerpolicy="no-referrer"
          />
          <span v-else class="initials">{{ initials }}</span>
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
      <p v-if="accountId" class="account-id">ID: {{ accountId }}</p>
    </div>

    <div class="form">
      <FormField label="First Name">
        <TextField v-model="firstName" placeholder="Enter first name" />
      </FormField>

      <FormField label="Last Name">
        <TextField v-model="lastName" placeholder="Enter last name" />
      </FormField>

      <FormField v-if="phoneLocked || phone" label="Phone">
        <TextField
          v-model="phoneLocal"
          type="tel"
          placeholder="Enter phone number"
          :disabled="phoneLocked"
        >
          <template #prefix>+855</template>
        </TextField>
        <p v-if="phoneLocked" class="field-hint">Used to sign in.</p>
      </FormField>

      <FormField label="Email">
        <TextField
          v-model="email"
          type="email"
          placeholder="Enter email"
          :disabled="emailLocked"
        />
        <p v-if="emailLocked" class="field-hint">Synced from your Google account.</p>
      </FormField>
    </div>

    <template #bottom>
      <Button :disabled="saving" @click="handleSave">
        {{ saving ? "Saving..." : "Save Changes" }}
      </Button>
    </template>
  </FormPageLayout>
</template>

<script lang="ts" setup>
import type { Member } from "~/composables/useApi";

if (!getAuthToken()) navigateTo("/login");

const router = useRouter();
const api = useApi();
const profileStore = useProfileStore();
const toast = useNotify();

const memberId = ref<string | null>(null);
const accountId = ref("");
const signinType = ref<string | undefined>(undefined);
const firstName = ref("");
const lastName = ref("");
const email = ref("");
const phone = ref("");
const avatarUrl = ref("");
const saving = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

const splitName = (name?: string) => {
  const trimmed = (name ?? "").trim();
  if (!trimmed) return { first: "", last: "" };
  const idx = trimmed.indexOf(" ");
  if (idx === -1) return { first: trimmed, last: "" };
  return { first: trimmed.slice(0, idx), last: trimmed.slice(idx + 1).trim() };
};

const preloadAvatar = (url: string) => {
  if (!url) {
    avatarUrl.value = "";
    return;
  }
  const img = new Image();
  img.referrerPolicy = "no-referrer";
  img.onload = () => {
    avatarUrl.value = url;
  };
  img.onerror = () => {
    avatarUrl.value = "";
  };
  img.src = url;
};

const hydrate = (member: Member) => {
  memberId.value = member.id;
  accountId.value = member.account_id ?? "";
  signinType.value = member.signin_type;
  const { first, last } = splitName(member.name);
  firstName.value = first;
  lastName.value = last;
  email.value = member.email ?? "";
  phone.value = member.phone ?? "";
  preloadAvatar(member.avatar_url ?? "");
};

const initials = computed(() => {
  const f = firstName.value?.[0] ?? "";
  const l = lastName.value?.[0] ?? "";
  return (f + l).toUpperCase();
});

const emailLocked = computed(() => signinType.value === "google");

// Phone is the login identity for phone sign-ins, so it's read-only there.
const phoneLocked = computed(() => signinType.value === "phone");

// TextField shows a +855 prefix, so the field edits only the local part.
const phoneLocal = computed({
  get: () => (phone.value.startsWith("+855") ? phone.value.slice(4) : phone.value),
  set: (v: string) => {
    phone.value = v ? `+855${v}` : "";
  },
});

const browsePhoto = () => {
  fileInput.value?.click();
};

const handleFileChange = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    // Avatar upload endpoint not implemented yet
    console.log("Selected file:", file.name);
  }
};

const handleSave = async () => {
  if (saving.value) return;
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
    toast.success("Profile updated.");
    router.back();
  } catch (e: any) {
    toast.error(e?.error || "Could not save changes.");
  } finally {
    saving.value = false;
  }
};

onMounted(async () => {
  const stored = await profileStore.load();
  if (stored) {
    hydrate(stored);
    return;
  }
  try {
    const { member } = await api.getProfile();
    hydrate(member);
    await profileStore.save(member);
  } catch (e: any) {
    toast.error(e?.error || "Could not load profile.");
  }
});
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

.account-id {
  margin: 4px 0 0 0;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
  letter-spacing: 0.5px;
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
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.field-hint {
  margin: 0;
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.4;
}
</style>
