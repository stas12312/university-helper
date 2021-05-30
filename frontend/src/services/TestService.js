import http from "../http-common";

class TestService {
    getAllTests(token) {
        return http.get('/v1/tests', {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        })
    }

    getTest(token, test_id) {
        return http.get(`/v1/tests/${test_id}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        })
    }

    createTest(token, test_id) {
        console.log(token)
        return http.post('/v1/tests', {
            external_id: test_id,
        }, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
    }

    payTest(token, test_id) {
        return http.post(`/v1/tests/${test_id}/pay`,{}, {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        })
    }

    getQuestions(token, test_id) {
        return http.get(`/v1/tests/${test_id}/questions`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            }
        )
    }
}

export default new TestService();