<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <NavBar title="Privacy Policy" />

    <main class="flex-1">
      <UContainer class="py-6 space-y-6 text-sm text-gray-700">
        <ContentSection
          title="1. Introduction"
          content="This Privacy Policy explains how we collect, use, disclose, and protect your personal information when you use the Loyatee membership program and related services."
        />
        <ContentSection
          title="2. Information We Collect"
          content="We may collect information that you provide directly, such as your name, contact details, and account information, as well as information generated when you use the program, including transaction history and interaction logs."
        />
        <ContentSection
          title="3. How We Use Your Information"
          content="We use your information to operate and improve the membership program, process transactions, personalize your experience, communicate with you, and comply with legal obligations."
        />
        <ContentSection
          title="4. Sharing of Information"
          content="We may share your information with trusted service providers who assist us in operating the program, as well as when required by law or to protect our rights, users, or the public. We do not sell your personal information."
        />
        <ContentSection
          title="5. Data Retention"
          content="We retain your information for as long as necessary to fulfill the purposes described in this Policy, unless a longer retention period is required or permitted by law."
        />
        <ContentSection
          title="6. Your Rights & Choices"
          content="Depending on your jurisdiction, you may have rights to access, correct, or delete your personal information, or to object to or restrict certain processing. You can exercise these rights by contacting us through the channels provided."
        />
        <ContentSection
          title="7. Security"
          content="We implement reasonable technical and organizational measures to protect your information from unauthorized access, loss, misuse, or alteration. However, no system is completely secure."
        />
        <ContentSection
          title="8. Changes to This Policy"
          content="We may update this Privacy Policy from time to time. Material changes will be notified through the app or other official channels. Your continued use of the program after changes become effective constitutes acceptance of the updated Policy."
        />
        <ContentSection
          title="9. Contact"
          content="If you have any questions about this Privacy Policy or how we handle your information, please contact our support team through the app or the official support channels provided."
        />
      </UContainer>
    </main>
  </div>
</template>

<script lang="ts">
export default {};
</script>
