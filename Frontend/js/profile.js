


document.addEventListener('DOMContentLoaded', async() => {
    
    Auth.requireAuth();

    const Load = document.getElementById('loader');
    const Profile_Info = document.getElementById('profile_id');
    const btnLogout = document.getElementById('logout_btn');

    Load.style.display = 'inline-block';
    
    try{
        const user = await API.get('/api/profile/');
        
        document.getElementById('proof-username').innerText = user.username || 'N/A';
        document.getElementById('proof-email').innerText  = user.email || 'N/A';
        document.getElementById('proof-joined').innerText = new Date(user.created_at).toLocaleDateString();

        const emotion = await API.get('/api/profile/emotion-summary');

        console.log("Emotion response:", emotion);

        
        document.getElementById('happy-percent').innerText = emotion.Happy + "%";
        document.getElementById('sad-percent').innerText = emotion.Sad + "%";
        document.getElementById('angry-percent').innerText = emotion.Angry + "%";
        document.getElementById('neutral-percent').innerText = emotion.Neutral + "%";
        document.getElementById('fear-percent').innerText = emotion.Fear + "%";
        document.getElementById('surprise-percent').innerText = emotion.Surprise + "%";
        document.getElementById('disgust-percent').innerText = emotion.Disgust + "%";

        Load.style.display = 'none';
        Profile_Info.classList.remove('hidden');

    }catch(error) {
        Load.style.display = 'none';
        alert('Failed to load profile. Please log in again');
        //Auth.logout();
    }

    btnLogout.addEventListener('click', () => {
        Auth.logout();
    });

});