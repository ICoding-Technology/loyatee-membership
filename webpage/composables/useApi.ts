export interface RequestOtpResponse {
  message: string;
  otp_debug?: string;
}

export interface VerifyOtpResponse {
  message: string;
  token: string;
  refresh_token: string;
  member: Member;
  is_new: boolean;
}

export interface Store {
  id: string;
  slug?: string;
  name?: string;
  logo_url?: string;
  category?: string;
  status?: string;
  membership_duration_days?: number | null;
}

export interface Membership {
  id: string;
  member_id: string;
  store_id: string;
  membership_no?: string;
  tier?: string;
  status?: string;
  current_period?: number;
  expires_at?: string | null;
  is_expired?: boolean;
  points: number;
  store?: Store;
}

export interface Reward {
  id: string;
  store_id: string;
  name: string;
  description?: string;
  points_cost: number;
  status?: string;
}

export interface Transaction {
  id: string;
  membership_id: string;
  member_id: string;
  store_id: string;
  store_name?: string;
  period: number;
  type: "earn" | "redeem" | "adjust" | "opening";
  side: "Cr" | "Dr";
  amount: number;
  reference?: string;
  created_at: string;
}

export interface ProfileResponse {
  member: Member;
  memberships: Membership[];
}

export type UpdateMemberPayload = Partial<Pick<Member, "name" | "email" | "avatar_url" | "phone">>;

// Tokens are persisted in IndexedDB but cached in module-level refs so the
// synchronous auth guards in page setup blocks can read them without awaiting.
// `hydrateAuthToken()` is called once at app boot from plugins/auth.client.ts.
// The access token is short-lived (1h); the refresh token is swapped for a new
// access token transparently on a 401 (see `call` below).
const _token = ref<string | null>(null);
const _refreshToken = ref<string | null>(null);

export const hydrateAuthToken = async () => {
  const store = useProfileStore();
  const [token, refresh] = await Promise.all([
    store.loadToken(),
    store.loadRefreshToken(),
  ]);
  _token.value = token ?? null;
  _refreshToken.value = refresh ?? null;
};

export const setAuthToken = async (token: string) => {
  _token.value = token;
  await useProfileStore().saveToken(token);
};

export const getAuthToken = () => _token.value;

export const setRefreshToken = async (token: string) => {
  _refreshToken.value = token;
  await useProfileStore().saveRefreshToken(token);
};

export const getRefreshToken = () => _refreshToken.value;

export const clearAuthToken = async () => {
  _token.value = null;
  _refreshToken.value = null;
  const store = useProfileStore();
  await Promise.all([store.clearToken(), store.clearRefreshToken()]);
};

// Single in-flight refresh shared across concurrent 401s, so a burst of
// expired-token requests triggers exactly one /auth/refresh call.
let _refreshing: Promise<boolean> | null = null;

const refreshTokens = (apiBase: string): Promise<boolean> => {
  if (!_refreshToken.value) return Promise.resolve(false);
  if (!_refreshing) {
    _refreshing = $fetch<{ token: string; refresh_token: string }>("/api/auth/refresh", {
      baseURL: apiBase,
      method: "POST",
      body: { refresh_token: _refreshToken.value },
    })
      .then(async (res) => {
        await setAuthToken(res.token);
        await setRefreshToken(res.refresh_token);
        return true;
      })
      .catch(() => false)
      .finally(() => {
        _refreshing = null;
      });
  }
  return _refreshing;
};

export type SigninType = "phone" | "google" | "telegram";

export interface Member {
  id: string;
  account_id?: string;
  signin_type?: SigninType;
  phone?: string;
  name?: string;
  email?: string;
  avatar_url?: string;
  google_id?: string;
  telegram_id?: string;
}

export interface SignInResponse {
  message: string;
  token: string;
  refresh_token: string;
  member: Member;
}

export interface ApiError {
  error: string;
  status: number;
}

export const useApi = () => {
  const { apiBase } = useClientConfig();

  // opts.auth = true → attach the bearer token and, on a 401, transparently
  // refresh it and retry once before surfacing the error.
  const call = async <T>(path: string, opts: any = {}, _retried = false): Promise<T> => {
    const { auth, headers, ...rest } = opts;
    const finalHeaders: Record<string, string> = { ...(headers || {}) };
    if (auth && _token.value) finalHeaders.Authorization = `Bearer ${_token.value}`;

    try {
      return await $fetch<T>(path, { baseURL: apiBase, headers: finalHeaders, ...rest });
    } catch (e: any) {
      const status = e?.status || e?.statusCode || 0;
      if (status === 401 && auth && !_retried && _refreshToken.value) {
        if (await refreshTokens(apiBase)) {
          return call<T>(path, opts, true); // retry with the refreshed token
        }
        // Refresh failed → session is truly over.
        await clearAuthToken();
        if (import.meta.client) navigateTo("/login");
      }
      const err: ApiError = {
        error: e?.data?.error || e?.message || "Network error",
        status,
      };
      throw err;
    }
  };

  return {
    requestOtp: (phone: string) =>
      call<RequestOtpResponse>("/api/auth/request-otp", {
        method: "POST",
        body: { phone },
      }),

    verifyOtp: (phone: string, otp: string) =>
      call<VerifyOtpResponse>("/api/auth/verify-otp", {
        method: "POST",
        body: { phone, otp },
      }),

    signInWithGoogle: (
      creds: { id_token?: string; access_token?: string },
    ) =>
      call<SignInResponse>("/api/auth/google", {
        method: "POST",
        body: creds,
      }),

    signInWithTelegram: (payload: Record<string, unknown>) =>
      call<SignInResponse>("/api/auth/telegram", {
        method: "POST",
        body: payload,
      }),

    // Revoke the refresh token server-side (best-effort) on sign-out.
    logout: () => {
      const refresh = getRefreshToken();
      if (!refresh) return Promise.resolve();
      return call("/api/auth/logout", {
        method: "POST",
        body: { refresh_token: refresh },
      }).catch(() => undefined);
    },

    getProfile: () => call<ProfileResponse>("/api/profile", { auth: true }),

    updateMember: (memberId: string, data: UpdateMemberPayload) =>
      call<Member>(`/api/members/${memberId}`, { method: "PATCH", body: data, auth: true }),

    // Public store lookup by base64 subscribe token (for the confirmation page).
    getStoreByToken: (token: string) =>
      call<Store>("/api/stores/by-token", { query: { token } }),

    // Subscribe the authenticated member to the store behind the token.
    subscribeToStore: (token: string) =>
      call<Membership>("/api/subscribe", { query: { store: token }, auth: true }),

    // Recent activity across all of the member's memberships.
    getMemberTransactions: (memberId: string, limit = 50) =>
      call<Transaction[]>(`/api/members/${memberId}/transactions`, {
        query: { limit },
        auth: true,
      }),

    // Public list of a store's active rewards.
    getStoreRewards: (storeId: string) =>
      call<Reward[]>(`/api/stores/${storeId}/rewards`),

    // Redeem a reward against a membership (debits its points_cost).
    redeemReward: (membershipId: string, rewardId: string) =>
      call(`/api/memberships/${membershipId}/redeem-reward`, {
        method: "POST",
        body: { reward_id: rewardId },
        auth: true,
      }),

    // Leave a store (removes the membership + its ledger).
    unsubscribe: (membershipId: string) =>
      call(`/api/memberships/${membershipId}`, { method: "DELETE", auth: true }),
  };
};
