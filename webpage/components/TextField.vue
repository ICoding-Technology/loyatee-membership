<template>
  <div class="textfield-wrapper" :class="{ focused: isFocused, disabled }">
    <span v-if="$slots.prefix" class="textfield-prefix">
      <slot name="prefix" />
    </span>
    <input
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      :maxlength="maxlength"
      :readonly="disabled"
      class="textfield-input"
      @input="
        $emit('update:modelValue', ($event.target as HTMLInputElement).value)
      "
      @focus="isFocused = true"
      @blur="isFocused = false"
    />
  </div>
</template>

<script lang="ts">
export default {
  props: {
    modelValue: {
      type: String,
      default: "",
    },
    type: {
      type: String,
      default: "text",
    },
    placeholder: {
      type: String,
      default: "",
    },
    maxlength: {
      type: [String, Number],
      default: undefined,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      isFocused: false,
    };
  },
};
</script>

<style scoped>
.textfield-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 1.5px solid var(--color-border);
  border-radius: 5px;
  transition: border-color 0.2s;
}

.textfield-wrapper.focused {
  border-color: var(--color-primary);
}

.textfield-wrapper.disabled {
  background: var(--color-disabled-bg, #f3f4f6);
  cursor: not-allowed;
}

.textfield-wrapper.disabled .textfield-input {
  color: var(--color-text-secondary);
  cursor: not-allowed;
}

.textfield-prefix {
  color: var(--color-text-muted);
  font-size: 14px;
  font-weight: 500;
  flex-shrink: 0;
}

.textfield-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  background: transparent;
}

.textfield-input::placeholder {
  color: var(--color-placeholder);
  font-weight: 400;
}
</style>
