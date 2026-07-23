

class Camera{
    constructor() {
        this.videoElement = document.getElementById('webcam');
        this.snapshotElement = document.getElementById('snapshot')
        this.btnCapture = document.getElementById('class-capture');
        this.btnRetake = document.getElementById('class-Retake');
        this.btnAnalyze = document.getElementById('class-Analyze');
        this.stream = null;
        this.img_to_base64 = null;
    }

    async init() {

        if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
            alert("camera API is not Supported");
            return;
        }
        try{
            this.stream = await navigator.mediaDevices.getUserMedia({
                video:{width:1280, height:720},
                audio:false
            });

            this.videoElement.srcObject = this.stream;
            this.btnCapture.addEventListener('click', () => this.Capture());
            this.btnRetake.addEventListener('click', () => this.Retake());
        }catch(error){
            console.error("Error accessing webcam...", error);
            alert("could not access Webcam.....Please ensure permission are granted.");
        }
    }

    Capture(){
        const canvas = document.createElement('canvas');
        canvas.width = this.videoElement.videoWidth || 1280;
        canvas.height = this.videoElement.videoHeight || 720;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.videoElement, 0, 0, canvas.width, canvas.height);

        this.img_to_base64 = canvas.toDataURL('image/jpg');

        this.snapshotElement.src = this.img_to_base64;
        this.videoElement.classList.add('hidden');
        this.snapshotElement.classList.remove('hidden');
    
        this.btnCapture.classList.add('hidden');
        this.btnRetake.classList.remove('hidden');
        this.btnAnalyze.classList.remove('hidden');
    }

    Retake(){
        this.img_to_base64 = null;
        this.videoElement.classList.remove('hidden');
        this.snapshotElement.classList.add('hidden');

        this.btnCapture.classList.remove('hidden');
        this.btnRetake.classList.add('hidden');
        this.btnAnalyze.classList.add('hidden');
    }

    getBase64Image(){
        return this.img_to_base64;
    }
}