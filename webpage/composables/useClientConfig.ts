interface AppConfig {
  googleClientId: string;
  telegramBotName: string;
}

declare global {
  interface Window {
    __APP_CONFIG__?: AppConfig;
  }
}

/**
 * Reads public config injected at runtime via /config.js (set by the API
 * container from env vars). Falls back to Nuxt's build-time runtimeConfig
 * for local dev where /config.js isn't served.
 */
export const useClientConfig = (): AppConfig => {
  if (typeof window !== "undefined" && window.__APP_CONFIG__) {
    return window.__APP_CONFIG__;
  }
  const { public: pub } = useRuntimeConfig();
  return {
    googleClientId: (pub.googleClientId as string) || "",
    telegramBotName: (pub.telegramBotName as string) || "",
  };
};
