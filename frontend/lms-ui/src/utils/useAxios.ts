import axios from "axios";
import Cookies from "js-cookie";
import { getRefreshedToken, isAccessTokenExpired, setAuthUser } from "./auth";
import { API_BASE_URL } from "./constants";

const useAxios = () => {
    const axiosInstance = axios.create({
        baseURL: API_BASE_URL,
    });

    axiosInstance.interceptors.request.use(async (req) => {
        let accessToken = Cookies.get("access_token");

        if (accessToken && !isAccessTokenExpired(accessToken)) {
            req.headers.Authorization = `Bearer ${accessToken}`;
            return req;
        }

        try {
            const response = await getRefreshedToken();
            if (!response) {
                return Promise.reject("Failed to refresh token");
            }
            
            setAuthUser(response.access, response.refresh);
            Cookies.set("access_token", response.access); // Ensure updated token is stored
            Cookies.set("refresh_token",response.refresh)
            req.headers.Authorization = `Bearer ${response.access}`;
        } catch (error) {
            console.error("Token refresh failed:", error);
            return Promise.reject(error);
        }

        return req;
    });

    return axiosInstance;
};

export default useAxios;
