import type { Member } from "./useApi";

const DB_NAME = "loyatee";
const DB_VERSION = 1;
const STORE = "profile";
const PROFILE_KEY = "current";
const TOKEN_KEY = "auth-token";

const openDb = () =>
  new Promise<IDBDatabase>((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });

const tx = async <T>(
  mode: IDBTransactionMode,
  run: (store: IDBObjectStore) => IDBRequest<T>,
): Promise<T> => {
  const db = await openDb();
  return new Promise<T>((resolve, reject) => {
    const t = db.transaction(STORE, mode);
    const req = run(t.objectStore(STORE));
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
    t.oncomplete = () => db.close();
  });
};

export const useProfileStore = () => ({
  save: (member: Member) =>
    tx("readwrite", (s) => s.put(member, PROFILE_KEY)),

  load: () =>
    tx<Member | undefined>("readonly", (s) => s.get(PROFILE_KEY)),

  clear: () =>
    tx("readwrite", (s) => s.delete(PROFILE_KEY)),

  saveToken: (token: string) =>
    tx("readwrite", (s) => s.put(token, TOKEN_KEY)),

  loadToken: () =>
    tx<string | undefined>("readonly", (s) => s.get(TOKEN_KEY)),

  clearToken: () =>
    tx("readwrite", (s) => s.delete(TOKEN_KEY)),
});
