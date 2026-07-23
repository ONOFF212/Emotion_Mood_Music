
const BASE_URL = 'http://localhost:8000';

class API{

    static getHeaders(includeAuth=true){
        const headers = {
            'Content-Type': 'application/json'
        };

        if(includeAuth) {
            const token = localStorage.getItem('aura_token');
            if(token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }
        return headers;
    }

    static async request(endpoint, options = {}, retry = false) {
        const url = `${BASE_URL}${endpoint}`;

        try{
            const response = await fetch(url, options);

            if(response.status === 401 && endpoint !== '/api/auth/login'){
                localStorage.removeItem('aura_token');
                window.location.href = 'login.html';
                return null;
            }
            if(!response.ok){
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'API Request Failed');
            }
            return await response.json();
        } catch(error) {
            console.error(`API error(${endpoint}):`, error);
            throw error;
        }
    }

    static async get(endpoint) {
        return this.request(endpoint, {
            method:'GET',
            headers:this.getHeaders()
        });
    }

    static async post(endpoint, data, includeAuth = true){
        return this.request(endpoint, {
            method:'POST',
            headers: this.getHeaders(includeAuth),
            body:JSON.stringify(data)
        });
    }

    
}