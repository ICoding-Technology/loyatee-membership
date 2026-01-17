<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Header with close button -->
    <PrivacyHeader @close="onClose" />

    <!-- Content -->
    <main class="flex-1">
      <UContainer class="py-6 space-y-6 text-sm text-gray-700">
        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">1. Introduction</h2>
          <p>
            This Privacy Policy explains how we collect, use, disclose, and
            protect your personal information when you use the Loyatee
            membership program and related services.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            2. Information We Collect
          </h2>
          <p>
            We may collect information that you provide directly, such as your
            name, contact details, and account information, as well as
            information generated when you use the program, including
            transaction history and interaction logs.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            3. How We Use Your Information
          </h2>
          <p>
            We use your information to operate and improve the membership
            program, process transactions, personalize your experience,
            communicate with you, and comply with legal obligations.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            4. Sharing of Information
          </h2>
          <p>
            We may share your information with trusted service providers who
            assist us in operating the program, as well as when required by law
            or to protect our rights, users, or the public. We do not sell your
            personal information.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">5. Data Retention</h2>
          <p>
            We retain your information for as long as necessary to fulfill the
            purposes described in this Policy, unless a longer retention period
            is required or permitted by law.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            6. Your Rights & Choices
          </h2>
          <p>
            Depending on your jurisdiction, you may have rights to access,
            correct, or delete your personal information, or to object to or
            restrict certain processing. You can exercise these rights by
            contacting us through the channels provided.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">7. Security</h2>
          <p>
            We implement reasonable technical and organizational measures to
            protect your information from unauthorized access, loss, misuse, or
            alteration. However, no system is completely secure.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            8. Changes to This Policy
          </h2>
          <p>
            We may update this Privacy Policy from time to time. Material
            changes will be notified through the app or other official channels.
            Your continued use of the program after changes become effective
            constitutes acceptance of the updated Policy.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">9. Contact</h2>
          <p>
            If you have any questions about this Privacy Policy or how we handle
            your information, please contact our support team through the app or
            the official support channels provided.
          </p>
        </section>
      </UContainer>
    </main>
  </div>
</template>

<script lang="ts">
export default {
  methods: {
    onClose() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
