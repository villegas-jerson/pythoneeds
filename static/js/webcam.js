<script>
document.addEventListener("DOMContentLoaded", function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const snapshot = document.getElementById('snapshot');
    const photo_data = document.getElementById('photo_data');

    // Request webcam access
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Error accessing webcam: ", err);
            alert("Cannot access webcam. Make sure your browser has permission and use HTTPS or localhost.");
        });

    // Capture snapshot
    window.capturePhoto = function() {
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL('image/png'); // Base64
        snapshot.src = dataURL; // Show captured image
        photo_data.value = dataURL; // Send to server
    };
});
</script>
