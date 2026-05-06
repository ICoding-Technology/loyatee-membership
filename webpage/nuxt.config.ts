// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  ssr: false,
  devtools: { enabled: false },
  modules: ["@nuxt/ui", "vue3-carousel-nuxt"],
  css: ["~/assets/css/main.css"],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:5001",
      googleClientId: process.env.NUXT_PUBLIC_GOOGLE_CLIENT_ID || "",
      telegramBotName: process.env.NUXT_PUBLIC_TELEGRAM_BOT_NAME || "",
    },
  },
  app: {
    head: {
      link: [
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&family=Quicksand:wght@300..700&display=swap",
        },
      ],
      script: [
        { src: "https://accounts.google.com/gsi/client", async: true, defer: true },
      ],
    },
  },
});
