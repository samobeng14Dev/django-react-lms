import axios from 'axios';
import { getRefreshedToken, isAccessTokenExpired, setAuthUser } from "./auth";
import { API_BASE_URL } from './constants';
import Cookies from 'js-cookie';

const useAxios = () => {
    const accessToken = Cookies.get("access_token");

    const axiosInstance = axios.create({
        baseURL: API_BASE_URL,
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {},
    });

    axiosInstance.interceptors.request.use(async (req) => {
        const accessToken = Cookies.get("access_token"); // Ensure latest token is used

        if (!accessToken || !isAccessTokenExpired(accessToken)) {
            req.headers.Authorization = `Bearer ${accessToken}`;
            return req;
        }

        try {
            const response = await getRefreshedToken();
            if (response) {
                setAuthUser(response.access, response.refresh);
                req.headers.Authorization = `Bearer ${response.access}`;
            }
        } catch (error) {
            console.error("Token refresh failed:", error);
        }

        return req;
    });

    return axiosInstance;
};

export default useAxios;
