// Remembers where to send the user after they finish authenticating, so a
// flow that starts on a gated page (e.g. /subscribe?store=...) can resume
// there once login/signup completes. Backed by sessionStorage so it survives
// the multi-step login → otp → setup-account hops within the tab.
const KEY = "post-auth-redirect";

export const useAuthRedirect = () => {
  const set = (path: string) => {
    // Only internal paths — guard against open-redirect.
    if (import.meta.client && path && path.startsWith("/")) {
      sessionStorage.setItem(KEY, path);
    }
  };

  const consume = (): string | null => {
    if (!import.meta.client) return null;
    const value = sessionStorage.getItem(KEY);
    if (value) sessionStorage.removeItem(KEY);
    return value;
  };

  return { set, consume };
};
