<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <NavBar title="Terms & Conditions" />

    <main class="flex-1">
      <UContainer class="py-6 space-y-6 text-sm text-gray-700">
        <ContentSection
          title="1. Introduction"
          content="These Terms & Conditions govern your use of the Loyatee membership program and related services. By enrolling or continuing to use your membership, you agree to be bound by these Terms."
        />
        <ContentSection
          title="2. Membership Eligibility"
          content="Membership is personal and non-transferable. You must provide accurate and complete information when registering and keep your details up to date."
        />
        <ContentSection
          title="3. Earning Points"
          content="Points are earned on eligible transactions as communicated in the program materials. Points have no cash value, are not legal tender, and cannot be sold, transferred, or exchanged except as expressly permitted."
        />
        <ContentSection
          title="4. Redeeming Points"
          content="Redemption options, thresholds, and any applicable fees or restrictions will be communicated from time to time. We reserve the right to change or discontinue rewards or conversion rates at our discretion."
        />
        <ContentSection
          title="5. Account & Security"
          content="You are responsible for maintaining the confidentiality of your account details and for all activity that occurs under your membership. Notify us promptly if you suspect any unauthorized use."
        />
        <ContentSection
          title="6. Changes to the Program"
          content="We may modify, suspend, or terminate the membership program, including these Terms, at any time. Material changes will be communicated through the app or other official channels."
        />
        <ContentSection
          title="7. Termination"
          content="We may suspend or terminate your membership if you breach these Terms, misuse the program, or engage in fraud or abuse. Upon termination, unused points may be forfeited in accordance with applicable law."
        />
        <ContentSection
          title="8. Contact"
          content="If you have any questions regarding these Terms & Conditions or your membership, please contact our support team through the app or the official support channels provided."
        />
      </UContainer>
    </main>
  </div>
</template>

<script lang="ts">
export default {};
</script>
