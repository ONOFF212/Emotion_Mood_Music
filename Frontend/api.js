
const BASE_URL = 'http://localhost:8000';

class API{

    static getHeaders(includeAuth=true){
        const headers = {
            'Content-Type': 'application/json'
        };
        return headers;
    }

    static async request(endpoint, options = {}) {
        const url = `${BASE_URL}${endpoint}`;

        try{
            const response = await fetch(url, options);

            if(!response.ok){
                throw new Error(errorData.detail || 'API Request Failed');
            }
            return await response.json();
        } catch(error) {
            throw error;
        }
    }


    static async post(endpoint, data, includeAuth = true){
        return this.request(endpoint, {
            method:'POST',
            Headers: this.getHeaders(includeAuth),
            body:JSON.stringify(data)
        });
    }

    
}