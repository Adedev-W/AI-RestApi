document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const startCameraButton = document.getElementById('start-camera');
    const testSpoofButton = document.getElementById('test-spoof');
    const verifyIdentityButton = document.getElementById('verify-identity');
    const mainImageUpload = document.getElementById('main-image-upload');
    const spoofResultBox = document.getElementById('spoof-result');
    const verifyResultBox = document.getElementById('verify-result');
    const statusDiv = document.getElementById('status');
    const loader = document.getElementById('loader');

    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
    const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'image/jpg'];

    let stream;

    startCameraButton.addEventListener('click', async () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            statusDiv.textContent = 'Camera Active';
            statusDiv.className = 'status-active';
            testSpoofButton.disabled = false;
            verifyIdentityButton.disabled = false;
        } catch (err) {
            statusDiv.textContent = 'Could not access camera';
            console.error("Camera access error:", err);
        }
    });

    function captureFrame() {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            canvas.toBlob(resolve, 'image/jpeg');
        });
    }

    function showLoader(show) {
        loader.className = show ? '' : 'loader-hidden';
    }
    
    function formatResult(result) {
        return JSON.stringify(result, null, 2);
    }

    testSpoofButton.addEventListener('click', async () => {
        showLoader(true);
        const imageBlob = await captureFrame();
        const formData = new FormData();
        formData.append('file', imageBlob, 'capture.jpg');
        
        try {
            const response = await fetch('/demo/predict_face_spoofing', { method: 'POST', body: formData });
            const result = await response.json();
            spoofResultBox.textContent = formatResult(result);
            spoofResultBox.className = result.label === 'real' ? 'result-box result-success' : 'result-box result-fail';
        } catch (error) {
            spoofResultBox.textContent = `Error: ${error.message}`;
        } finally {
            showLoader(false);
        }
    });

    verifyIdentityButton.addEventListener('click', async () => {
        const mainImageFile = mainImageUpload.files[0];
        if (!mainImageFile) {
            alert('Please upload a Main Image.');
            return;
        }
        if (!ALLOWED_TYPES.includes(mainImageFile.type)) {
            alert(`Invalid file type for Main Image. Allowed: ${ALLOWED_TYPES.join(', ')}`);
            return;
        }
        if (mainImageFile.size > MAX_FILE_SIZE) {
            alert(`Main Image is too large. Max size: ${MAX_FILE_SIZE / 1024 / 1024} MB`);
            return;
        }

        showLoader(true);
        const valImageBlob = await captureFrame();
        const formData = new FormData();
        formData.append('main_image', mainImageFile);
        formData.append('val_image', valImageBlob, 'capture.jpg');
        
        try {
            const response = await fetch('/demo/verify_identity', { method: 'POST', body: formData });
            const result = await response.json();
            verifyResultBox.textContent = formatResult(result);
            const success = result.face_match_passed && result.spoof_check_passed !== false;
            verifyResultBox.className = success ? 'result-box result-success' : 'result-box result-fail';
        } catch (error) {
            verifyResultBox.textContent = `Error: ${error.message}`;
        } finally {
            showLoader(false);
        }
    });
}); 