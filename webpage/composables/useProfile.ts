import type { Member, Membership } from "./useApi";

// Live, reactive profile (member + subscribed memberships) backed by the
// /api/profile endpoint. The member is also persisted to IndexedDB via
// useProfileStore so guards/menus can read it synchronously between sessions.
export const useProfile = () => {
  const member = useState<Member | null>("profile-member", () => null);
  const memberships = useState<Membership[]>("profile-memberships", () => []);
  const pending = useState<boolean>("profile-pending", () => false);

  const api = useApi();
  const store = useProfileStore();

  const totalPoints = computed(() =>
    memberships.value.reduce((sum, m) => sum + (m.points ?? 0), 0),
  );

  const fetchProfile = async () => {
    pending.value = true;
    try {
      const data = await api.getProfile();
      member.value = data.member;
      memberships.value = data.memberships ?? [];
      await store.save(data.member);
      return data;
    } finally {
      pending.value = false;
    }
  };

  return { member, memberships, totalPoints, pending, fetchProfile };
};
