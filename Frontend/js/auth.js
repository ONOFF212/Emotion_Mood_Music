

class Auth{

    static async login(username, password) {
        try{
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers:{
                    'Content-Type' : 'application/x-www.form-urlencoded'
                },
                body:formData
            });

            if(!response.ok) {
                throw new Error('Login Failed');
            }
            return true;
        } catch(error){
            console.error("Login Error:", error);
            return false;
        }
    }
}