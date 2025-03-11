import axios from 'axios'
import { API_BADE_URL } from './constants';

const apiInstance = axios.create({
    baseURL:API_BADE_URL,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
        Accept:"application/json"
    }
});

export default apiInstance;