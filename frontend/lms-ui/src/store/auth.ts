import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";

// Define the type for user data
interface UserData {
    user_id: string | null;
    username: string | null;
}

// Define the type for the Zustand store
interface AuthStore {
    allUserData: UserData | null;
    loading: boolean;
    user: () => UserData | null;
    setUser: (user: UserData | null) => void;
    setLoading: (loading: boolean) => void;
    isLoggedIn: () => boolean;
}

const useAuthStore = create<AuthStore>((set, get) => ({
    allUserData: null,
    loading: false,

    user: () => get().allUserData,

    setUser: (user: UserData | null) => set({ allUserData: user }),
    setLoading: (loading) => set({ loading }),
    isLoggedIn: () => get().allUserData !== null,
}));

if (import.meta.env.DEV) {
    mountStoreDevtool("AuthStore", useAuthStore);
}

export { useAuthStore };
