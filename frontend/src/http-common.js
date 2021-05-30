import axios from "axios";

const apiClient = axios.create({
    baseURL: "https://university-helper.ru/api",
    headers: {
        "Content-type": "application/json",
    }
})

export default apiClient;
