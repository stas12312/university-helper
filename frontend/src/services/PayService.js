import http from "../http-common";

class PayService {
    createPay(token, amount) {
        return http.post('/v1/pays',
            {
                'amount': amount
            },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            })
    }
}

export default new PayService()