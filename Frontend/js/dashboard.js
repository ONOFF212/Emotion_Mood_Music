

document.addEventListener('DOMContentLoaded', async() => {

    const camera = new Camera();
    try{
        await camera.init();
    }catch(error) {
        console.error("Failed to start the camera::", error);
    }

    const btnAnalyze = document.getElementById('class-Analyze');
    const loader = document.getElementById('loader');
    const emptyState = document.getElementById('empty-state');
    const musicResult = document.getElementById('music-result');

    const emotionBadge = document.getElementById('detected-emotion');
    const trackTitle = document.getElementById('track-title');
    const ytPlayer = document.getElementById('youtube-player');

    const languageSelect = document.getElementById('language');

    const playlistItems = document.getElementById('playlist-items');

    btnAnalyze.addEventListener('click', async () => {
        const base64Image = camera.getBase64Image();

        const language = languageSelect.value;

        btnAnalyze.disabled = true;
        btnAnalyze.innerText = "Analyzing.....";
        emptyState.classList.add('hidden');
        musicResult.classList.add('hidden');
        loader.style.display = 'inline-block';
        
        try{
            const data = await API.post('/api/emotion/detect/base64', {
                img : base64Image,
                language:language
            });

            emotionBadge.innerText = data.emotion;
            // trackTitle.innerText = data.yt_title;
            // ytPlayer.src = data.yt_embed_url + "&autoplay=1";

            if (data.videos && data.videos.length > 0) {
                trackTitle.innerText = data.videos[0].title;
                ytPlayer.src = data.videos[0].embed_url + "&autoplay=1";

                playlistItems.innerHTML = "";
                data.videos.forEach(video => {
                    const song = document.createElement("div");
                    song.className = "playlist-song";
                    song.innerText = video.title;

                    song.addEventListener("click", () => {
                        trackTitle.innerText = video.title;
                        ytPlayer.src = video.embed_url + "&autoplay=1";
                    });
                    playlistItems.appendChild(song);
                });
            }
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