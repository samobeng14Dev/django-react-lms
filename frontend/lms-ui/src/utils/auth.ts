import { useAuthStore } from "../store/auth";
import apiInstance from "./axios";
import jwt_decode from "jwt-decode";
import Swal from "sweetalert2";
import Cookies from "js-cookie";

interface UserData {
    user_id: string;
    username: string;
}

interface RegisterPayload {
    full_name: string;
    email: string;
    password1: string;
    password2: string;
}

interface LoginPayload {
    email: string;
    password: string;
}

interface SetUserPayload {
    access_token: string;
    refresh_token: string;
}

export const login = async ({ email, password }: LoginPayload) => {
    try {
        const { data, status } = await apiInstance.post("user/token/", { email, password });

        if (status === 200) {
            await setAuthUser(data.access, data.refresh);
            Swal.fire("Success", "Login Successful", "success");
        }
        return { data, error: null };
    } catch (error) {
        return {
            data: null,
            error: (error as any).response?.data?.detail || "Something went wrong",
        };
    }
};

export const register = async ({ full_name, email, password1, password2 }: RegisterPayload) => {
    try {
        const { data } = await apiInstance.post("user/register/", {
            full_name,
            email,
            password1,
            password2,
        });

        // Automatically log in user
        await login({ email, password: password1 });
        Swal.fire("Success", "Registration Successful", "success");
        return { data, error: null };
    } catch (error) {
        return {
            data: null,
            error: (error as any).response?.data?.detail || "Something went wrong",
        };
    }
};

export const logout = () => {
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");

    // Set user to null instead of an empty object
    useAuthStore.getState().setUser(null);

    Swal.fire("Logged Out", "You have been logged out", "info");
};

// aims to set the authenticated user by managing access and refresh tokens
export const setUser = async (): Promise<SetUserPayload | null> => {
    let access_token = Cookies.get("access_token") ?? "";
    let refresh_token = Cookies.get("refresh_token") ?? "";

    if (!access_token || !refresh_token) {
        // Swal.fire("Error", "Tokens do not exist", "error");
        useAuthStore.getState().setUser(null); // Clear user state
        return null;
    }

    if (isAccessTokenExpired(access_token)) {
        const response = await getRefreshedToken();
        if (!response) {
            useAuthStore.getState().setUser(null); // Ensure user state is cleared on failure
            return null;
        }
        access_token = response.access;
        refresh_token = response.refresh;
    }

    if (access_token && refresh_token) {
        await setAuthUser(access_token, refresh_token);
    } else {
        useAuthStore.getState().setUser(null);
        Swal.fire("Error", "Failed to set user", "error");
    }
    return { access_token, refresh_token };
};
// responsible for setting the authenticated user's state in the application
export const setAuthUser = async (access_token: string = "", refresh_token: string = "") => {
    if (!access_token || !refresh_token) {
        useAuthStore.getState().setUser(null);
        return;
    }

    Cookies.set("access_token", access_token, { expires: 1, secure: true });
    Cookies.set("refresh_token", refresh_token, { expires: 7, secure: true });

    try {
        const decodedToken = jwt_decode<UserData>(access_token);
        useAuthStore.getState().setUser(decodedToken);
    } catch (error) {
        console.error("Error decoding token:", error);
        useAuthStore.getState().setUser(null);
    }
};

export const getRefreshedToken = async () => {
    const refresh_token = Cookies.get("refresh_token") ?? "";
    if (!refresh_token) {
        Swal.fire("Error", "Refresh token is missing", "error");
        return null;
    }

    try {
        const response = await apiInstance.post("token/refresh/", { refresh: refresh_token });

        if (response.data.access && response.data.refresh) {
            await setAuthUser(response.data.access, response.data.refresh);
        }

        return response.data;
    } catch (error) {
        Swal.fire("Error", "Failed to refresh token", "error");
        return null;
    }
};

export const isAccessTokenExpired = (access_token: string) => {
    try {
        const decodedToken: any = jwt_decode(access_token);
        return decodedToken.exp < Date.now() / 1000;
    } catch (error) {
        console.error("Failed to decode access token:", error);
        return true;
    }
};
