export default defineNuxtPlugin(async () => {
  await hydrateAuthToken();
});
