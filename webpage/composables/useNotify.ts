export type NotifyType = "success" | "info" | "error";

export interface NotifyItem {
  id: number;
  type: NotifyType;
  message: string;
  timeoutMs: number;
}

const items = ref<NotifyItem[]>([]);
let nextId = 1;
const timers = new Map<number, ReturnType<typeof setTimeout>>();

const dismiss = (id: number) => {
  const t = timers.get(id);
  if (t) {
    clearTimeout(t);
    timers.delete(id);
  }
  items.value = items.value.filter((i) => i.id !== id);
};

const add = (type: NotifyType, message: string, timeoutMs = 3000) => {
  const id = nextId++;
  items.value.push({ id, type, message, timeoutMs });
  if (timeoutMs > 0) {
    timers.set(
      id,
      setTimeout(() => dismiss(id), timeoutMs),
    );
  }
  return id;
};

export const useNotify = () => ({
  items,
  dismiss,
  add,
  success: (message: string, timeoutMs?: number) => add("success", message, timeoutMs),
  info: (message: string, timeoutMs?: number) => add("info", message, timeoutMs),
  error: (message: string, timeoutMs?: number) => add("error", message, timeoutMs ?? 5000),
});
