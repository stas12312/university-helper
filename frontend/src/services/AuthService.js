import http from "../http-common";

class AuthService {
    login(email, password) {
        let bodyFormData = new FormData();
        bodyFormData.append('username', email)
        bodyFormData.append('password', password)
        return http.post("/v1/auth/login", bodyFormData);
    }

    getMe(token) {
        return http.get('/v1/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        })
    }

    register(email, password, verify_uuid, verify_code) {
        return http.post("/v1/auth/register", {
            "email": email,
            "password": password,
            "verify_uuid": verify_uuid,
            "verify_code": verify_code,
        });
    }

    send_code(email) {
        return http.post("/v1/auth/send-code", {
            "email": email
        })
    }
}

export default new AuthService()