<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <NavBar :title="storeName" />

    <!-- Balance & Level card -->
    <div class="px-5 pt-4 pb-2">
      <div
        class="rounded-[15px] bg-gradient-to-br from-[#4C86E5] to-[#3B5FD4] shadow-md aspect-video px-5 py-5 flex flex-col justify-center items-center text-center text-white"
      >
        <!-- Balance -->
        <p class="text-xs text-white/60">Total Balance</p>
        <p class="mt-2 text-3xl font-bold font-number">
          {{ totalBalance.toLocaleString() }}
        </p>
        <p class="mt-1 text-xs text-white/60">Points</p>

        <!-- Divider -->
        <div class="h-px bg-white/20 w-full my-4"></div>

        <!-- Validity -->
        <div v-if="isExpired" class="text-red-200 text-xs font-semibold">
          Expired on {{ validUntil }}
        </div>
        <div v-else class="text-white/80 text-xs">
          <span>Valid until: </span>
          <span class="font-semibold text-white">{{ validUntil }}</span>
        </div>

        <!-- Unsubscribe -->
        <button
          type="button"
          class="mt-4 px-4 py-1.5 rounded-full border border-white/30 text-white/80 text-[10px] font-semibold hover:bg-white/10 transition disabled:opacity-40"
          :disabled="unsubscribing || !membership"
          @click="handleUnsubscribe"
        >
          {{ unsubscribing ? "Leaving…" : "Unsubscribe" }}
        </button>
      </div>
    </div>

    <!-- Rewards -->
    <div class="flex-1 flex flex-col bg-gray-100 px-3 pb-3">
      <div class="flex items-center justify-between px-4 pt-4 pb-3">
        <span class="text-xs font-semibold text-slate-900">Rewards</span>
        <span class="text-xs text-slate-400">{{ rewards.length }} available</span>
      </div>

      <div v-if="rewards.length" class="space-y-3 px-3">
        <div
          v-for="reward in rewards"
          :key="reward.id"
          class="rounded-md border border-gray-200 bg-white px-4 py-4 flex items-center gap-3"
        >
          <div
            class="w-10 h-10 rounded-full bg-[#E0EDFF] flex items-center justify-center flex-shrink-0"
          >
            <UIcon name="i-heroicons-gift" class="w-5 h-5 text-[#3B82F6]" />
          </div>
          <div class="flex-1">
            <p class="text-xs font-semibold text-slate-900">{{ reward.name }}</p>
            <p v-if="reward.description" class="text-[10px] text-slate-400">
              {{ reward.description }}
            </p>
            <p class="mt-0.5 text-[10px] text-[#3B82F6] font-semibold font-number">
              {{ reward.points_cost }} pts
            </p>
          </div>
          <button
            type="button"
            class="flex-shrink-0 px-3 py-1.5 rounded-full text-white text-[10px] font-semibold disabled:opacity-40"
            :class="canRedeem(reward) ? 'bg-[#3B82F6]' : 'bg-slate-300'"
            :disabled="!canRedeem(reward) || redeeming === reward.id"
            @click="handleRedeem(reward)"
          >
            {{ redeeming === reward.id ? "…" : "Redeem" }}
          </button>
        </div>
      </div>

      <div v-else class="px-3">
        <div class="rounded-md border border-dashed border-gray-300 bg-white px-4 py-8 text-center">
          <p class="text-xs text-slate-400">No rewards available yet</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { Reward } from "../composables/useApi";

if (!getAuthToken()) navigateTo("/login");

const route = useRoute();
const api = useApi();
const notify = useNotify();
const { memberships, fetchProfile } = useProfile();

const membershipId = computed(() => route.query.id as string | undefined);
const membership = computed(
  () => memberships.value.find((m) => m.id === membershipId.value) ?? null,
);

const storeName = computed(() => membership.value?.store?.name || "Card Detail");
const totalBalance = computed(() => membership.value?.points ?? 0);
const isExpired = computed(() => !!membership.value?.is_expired);

const validUntil = computed(() => {
  const iso = membership.value?.expires_at;
  if (!iso) return "No expiry";
  const d = new Date(iso);
  return Number.isNaN(d.getTime())
    ? "—"
    : d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
});

const rewards = ref<Reward[]>([]);
const redeeming = ref<string | null>(null);
const unsubscribing = ref(false);

const canRedeem = (r: Reward) => !isExpired.value && totalBalance.value >= r.points_cost;

const loadRewards = async (storeId?: string) => {
  if (!storeId) return;
  try {
    rewards.value = await api.getStoreRewards(storeId);
  } catch {
    rewards.value = [];
  }
};

const handleRedeem = async (r: Reward) => {
  if (redeeming.value || !membershipId.value || !canRedeem(r)) return;
  redeeming.value = r.id;
  try {
    await api.redeemReward(membershipId.value, r.id);
    await fetchProfile(); // refresh the balance
    notify.success(`Redeemed ${r.name}.`);
  } catch (e: any) {
    notify.error(e?.error || "Could not redeem this reward.");
  } finally {
    redeeming.value = null;
  }
};

const handleUnsubscribe = async () => {
  if (unsubscribing.value || !membershipId.value) return;
  if (!window.confirm(`Unsubscribe from ${storeName.value}? Your points will be lost.`)) return;
  unsubscribing.value = true;
  try {
    await api.unsubscribe(membershipId.value);
    await fetchProfile();
    notify.success(`Unsubscribed from ${storeName.value}.`);
    navigateTo("/home");
  } catch (e: any) {
    notify.error(e?.error || "Could not unsubscribe.");
    unsubscribing.value = false;
  }
};

// Load rewards once the membership (and its store) is known. Refresh the
// profile first if we landed here directly / on refresh.
watch(() => membership.value?.store?.id, (sid) => loadRewards(sid), { immediate: true });

onMounted(async () => {
  if (!memberships.value.length) await fetchProfile().catch(() => {});
});
</script>
