<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Header with close button -->
    <TermHeader @close="onClose" />

    <!-- Content -->
    <main class="flex-1">
      <UContainer class="py-6 space-y-6 text-sm text-gray-700">
        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">1. Introduction</h2>
          <p>
            These Terms &amp; Conditions govern your use of the Loyatee
            membership program and related services. By enrolling or continuing
            to use your membership, you agree to be bound by these Terms.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            2. Membership Eligibility
          </h2>
          <p>
            Membership is personal and non-transferable. You must provide
            accurate and complete information when registering and keep your
            details up to date.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">3. Earning Points</h2>
          <p>
            Points are earned on eligible transactions as communicated in the
            program materials. Points have no cash value, are not legal tender,
            and cannot be sold, transferred, or exchanged except as expressly
            permitted.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            4. Redeeming Points
          </h2>
          <p>
            Redemption options, thresholds, and any applicable fees or
            restrictions will be communicated from time to time. We reserve the
            right to change or discontinue rewards or conversion rates at our
            discretion.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            5. Account &amp; Security
          </h2>
          <p>
            You are responsible for maintaining the confidentiality of your
            account details and for all activity that occurs under your
            membership. Notify us promptly if you suspect any unauthorized use.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">
            6. Changes to the Program
          </h2>
          <p>
            We may modify, suspend, or terminate the membership program,
            including these Terms, at any time. Material changes will be
            communicated through the app or other official channels.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">7. Termination</h2>
          <p>
            We may suspend or terminate your membership if you breach these
            Terms, misuse the program, or engage in fraud or abuse. Upon
            termination, unused points may be forfeited in accordance with
            applicable law.
          </p>
        </section>

        <section class="space-y-2">
          <h2 class="text-sm font-semibold text-gray-900">8. Contact</h2>
          <p>
            If you have any questions regarding these Terms &amp; Conditions or
            your membership, please contact our support team through the app or
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
      // Navigate back to the home page when the header close button is clicked
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
