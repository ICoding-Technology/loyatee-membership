<template>
  <FormPageLayout>
    <template #header>
      <NavBar title="Subscribe" :back="false" />
    </template>

    <!-- Loading store info -->
    <div v-if="loading" class="state">
      <div class="spinner"></div>
      <p class="state-text">Loading store…</p>
    </div>

    <!-- Invalid link / store not found -->
    <div v-else-if="error" class="state">
      <UIcon name="i-heroicons-exclamation-triangle" class="state-icon" />
      <p class="state-text">{{ error }}</p>
    </div>

    <!-- Confirmation -->
    <div v-else-if="store" class="confirm">
      <div class="logo-wrap">
        <img v-if="store.logo_url" :src="store.logo_url" :alt="store.name" class="logo-img" />
        <span v-else class="logo-fallback">{{ initial }}</span>
      </div>

      <h1 class="store-name">{{ store.name }}</h1>
      <p v-if="store.category" class="store-category">{{ store.category }}</p>

      <p class="prompt">
        Subscribe to this store to collect points and rewards.
      </p>
    </div>

    <template #bottom>
      <Button
        v-if="store && !error"
        :disabled="subscribing"
        @click="handleSubscribe"
      >
        {{ subscribing ? "Subscribing…" : isLoggedIn ? "Subscribe" : "Sign in to subscribe" }}
      </Button>
    </template>
  </FormPageLayout>
</template>

<script lang="ts" setup>
import type { Store } from "../composables/useApi";

const route = useRoute();
const api = useApi();
const toast = useNotify();
const authRedirect = useAuthRedirect();
const { fetchProfile } = useProfile();

// The link uses ?store=<base64>; accept ?shop= as an alias too.
const token = computed(
  () => (route.query.store as string) || (route.query.shop as string) || "",
);
const isLoggedIn = computed(() => !!getAuthToken());

const store = ref<Store | null>(null);
const loading = ref(true);
const error = ref("");
const subscribing = ref(false);

const initial = computed(() => store.value?.name?.trim()?.[0]?.toUpperCase() ?? "?");

const handleSubscribe = async () => {
  if (subscribing.value || !store.value) return;

  // Gate the action on auth: remember this page and route through login first.
  if (!isLoggedIn.value) {
    authRedirect.set(route.fullPath);
    navigateTo("/login");
    return;
  }

  subscribing.value = true;
  try {
    await api.subscribeToStore(token.value);
    await fetchProfile().catch(() => {});
    toast.success(`Subscribed to ${store.value.name}.`);
    navigateTo("/home");
  } catch (e: any) {
    toast.error(e?.error || "Could not subscribe. Please try again.");
  } finally {
    subscribing.value = false;
  }
};

onMounted(async () => {
  if (!token.value) {
    error.value = "This subscription link is invalid.";
    loading.value = false;
    return;
  }
  try {
    store.value = await api.getStoreByToken(token.value);
  } catch (e: any) {
    error.value =
      e?.status === 404 ? "This store no longer exists." : "This subscription link is invalid.";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  text-align: center;
}

.state-text {
  font-size: 14px;
  color: var(--color-text-muted);
}

.state-icon {
  width: 40px;
  height: 40px;
  color: var(--color-error, #ef4444);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.confirm {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 8px;
}

.logo-wrap {
  width: 88px;
  height: 88px;
  border-radius: 24px;
  background: #eef2fb;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin-bottom: 12px;
  box-shadow: 0 4px 16px rgba(65, 105, 225, 0.15);
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.logo-fallback {
  font-size: 36px;
  font-weight: 700;
  color: var(--color-primary);
}

.store-name {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text, #1f2a3c);
}

.store-category {
  margin: 0;
  font-size: 13px;
  color: var(--color-text-muted);
  text-transform: capitalize;
}

.prompt {
  margin: 16px 0 0 0;
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  max-width: 280px;
}
</style>
