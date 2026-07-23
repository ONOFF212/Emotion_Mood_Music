

document.addEventListener('DOMContentLoaded', async() => {

    const camera = new Camera();
    try{
        await camera.init();
    }catch(error) {
        console.error("Failed to start the camera::", error);
    }

    const btnAnalyze = document.getElementById('class-Analyze');
    const loader = document.getElementById('loader');
    const emptyState = document.getElementById('empty-states');
    const musicResult = document.getElementById('music-result');

    const emotionBadge = document.getElementById('detected_emotion');
    const trackTitle = document.getElementById('track-title');
    const ytPlayer = document.getElementById('Youtube-player');

    btnAnalyze.addEventListener('click', async () => {
        const base64Image = camera.getBase64Image();

        btnAnalyze.disabled = true;
        btnAnalyze.innerText = "Analyzing.....";
        emptyState.classList.add('hidden');
        musicResult.classList.add('hidden');
        loader.style.display = 'inline-block';
        
        try{
            const data = await API.post('/api/emotion/detect/base64', {
                img : base64Image
            });

            emotionBadge.innerText = data.emotion;
            loader.style.display = 'none';
            musicResult.classList.remove('hidden');
        }catch(error) {
            alert('Failed to Analyze the Emotion ' + error.message);
            loader.style.display = 'none';
            emptyState.classList.remove('hidden');
        }finally{
            btnAnalyze.disabled = false;
            btnAnalyze.innerText = 'Analyze Emotion';
        }

    });
});