export interface RequestOtpResponse {
  message: string;
  otp_debug?: string;
}

export interface VerifyOtpResponse {
  message: string;
  token: string;
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
}

export interface Membership {
  id: string;
  member_id: string;
  store_id: string;
  membership_no?: string;
  tier?: string;
  status?: string;
  current_period?: number;
  points: number;
  store?: Store;
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

// Token is persisted in IndexedDB but cached in this module-level ref so the
// synchronous auth guards in page setup blocks can read it without awaiting.
// `hydrateAuthToken()` is called once at app boot from plugins/auth.client.ts.
const _token = ref<string | null>(null);

export const hydrateAuthToken = async () => {
  const stored = await useProfileStore().loadToken();
  _token.value = stored ?? null;
};

export const setAuthToken = async (token: string) => {
  _token.value = token;
  await useProfileStore().saveToken(token);
};

export const getAuthToken = () => _token.value;

export const clearAuthToken = async () => {
  _token.value = null;
  await useProfileStore().clearToken();
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
  member: Member;
}

export interface ApiError {
  error: string;
  status: number;
}

export const useApi = () => {
  const { apiBase } = useClientConfig();

  const call = async <T>(path: string, opts: Parameters<typeof $fetch>[1] = {}): Promise<T> => {
    try {
      return await $fetch<T>(path, { baseURL: apiBase, ...opts });
    } catch (e: any) {
      const err: ApiError = {
        error: e?.data?.error || e?.message || "Network error",
        status: e?.status || e?.statusCode || 0,
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

    getProfile: () => {
      const token = getAuthToken();
      return call<ProfileResponse>("/api/profile", {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
    },

    updateMember: (memberId: string, data: UpdateMemberPayload) => {
      const token = getAuthToken();
      return call<Member>(`/api/members/${memberId}`, {
        method: "PATCH",
        body: data,
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
    },

    // Public store lookup by base64 subscribe token (for the confirmation page).
    getStoreByToken: (token: string) =>
      call<Store>("/api/stores/by-token", { query: { token } }),

    // Subscribe the authenticated member to the store behind the token.
    subscribeToStore: (token: string) => {
      const authToken = getAuthToken();
      return call<Membership>("/api/subscribe", {
        query: { store: token },
        headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
      });
    },

    // Recent activity across all of the member's memberships.
    getMemberTransactions: (memberId: string, limit = 50) => {
      const token = getAuthToken();
      return call<Transaction[]>(`/api/members/${memberId}/transactions`, {
        query: { limit },
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
    },
  };
};
