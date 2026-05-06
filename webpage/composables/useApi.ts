export interface RequestOtpResponse {
  message: string;
  otp_debug?: string;
}

export interface VerifyOtpResponse {
  message: string;
  token: string;
  member: Member;
}

export interface ProfileResponse {
  member: Member;
}

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
  points?: number;
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
  };
};
