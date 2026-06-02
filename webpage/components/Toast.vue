<template>
  <Teleport to="body">
    <div class="toast-stack" role="status" aria-live="polite">
      <TransitionGroup name="toast">
        <div
          v-for="item in items"
          :key="item.id"
          class="toast"
          :class="`toast-${item.type}`"
          @click="notify.dismiss(item.id)"
        >
          <UIcon :name="iconFor(item.type)" class="toast-icon" />
          <span class="toast-message">{{ item.message }}</span>
          <button
            type="button"
            class="toast-close"
            aria-label="Dismiss"
            @click.stop="notify.dismiss(item.id)"
          >
            <UIcon name="i-heroicons-x-mark" class="w-4 h-4" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script lang="ts" setup>
import type { NotifyType } from "~/composables/useNotify";

const notify = useNotify();
const items = notify.items;

const iconFor = (type: NotifyType) => {
  if (type === "success") return "i-heroicons-check-circle";
  if (type === "error") return "i-heroicons-x-circle";
  return "i-heroicons-information-circle";
};
</script>

<style scoped>
.toast-stack {
  position: fixed;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: min(420px, calc(100vw - 32px));
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid var(--color-border);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  font-size: 14px;
  font-weight: 500;
  pointer-events: auto;
  cursor: pointer;
}

.toast-icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
}

.toast-message {
  flex: 1;
  line-height: 1.4;
  color: var(--color-text);
}

.toast-close {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 4px;
  color: var(--color-text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
}

.toast-close:hover {
  background: rgba(0, 0, 0, 0.05);
}

.toast-success {
  border-color: #bbf7d0;
  background: #f0fdf4;
}
.toast-success .toast-icon {
  color: #16a34a;
}

.toast-info {
  border-color: #bfdbfe;
  background: #eff6ff;
}
.toast-info .toast-icon {
  color: #2563eb;
}

.toast-error {
  border-color: #fecaca;
  background: #fef2f2;
}
.toast-error .toast-icon {
  color: #dc2626;
}

.toast-enter-active,
.toast-leave-active {
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>
