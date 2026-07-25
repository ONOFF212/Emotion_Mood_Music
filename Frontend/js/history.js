
document.addEventListener('DOMContentLoaded', async () => {

    Auth.requireAuth();

    const container = document.getElementById('history-container');
    const loader = document.getElementById('loader');

    loader.style.display = 'inline-block';

    try{
        const histories = await API.get('/api/history/');
        loader.style.display = 'none';

        histories.forEach(item => {
            container.innerHTML += `
            <div class="history-row">
                <div class="history-cell">${item.emotion}</div>
                <div class="history-cell">${item.yt_title}</div>
                <div class="history-cell"> <img src="${item.image_path}" alt="Emotion Photo"> </div>
                <div class="history-cell">${item.timestamp}</div>        
            </div>
            `;
        });

    }catch(error){
        loader.style.display = 'none';
        console.error(error);
    }

});