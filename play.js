const camera = document.getElementById("camera");
const startButton = document.getElementById("start-camera");
const stopButton = document.getElementById("stop-camera");

const status = document.getElementById("status");
const cameraMessage = document.getElementById("camera-message");
const result = document.getElementById("result");

let stream = null;


// =========================
// START CAMERA
// =========================

async function startCamera() {

    try {

        stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        camera.srcObject = stream;

        cameraMessage.style.display = "none";

        status.textContent = "Camera is running";

        result.textContent = "—";

    } catch (error) {

        console.error("Camera error:", error);

        status.textContent = "Unable to access camera";

        cameraMessage.textContent =
            "Please allow camera access.";

        cameraMessage.style.display = "block";
    }
}


// =========================
// STOP CAMERA
// =========================

function stopCamera() {

    if (stream) {

        stream.getTracks().forEach(track => {
            track.stop();
        });

        stream = null;
    }

    camera.srcObject = null;

    cameraMessage.textContent = "Camera is not running";
    cameraMessage.style.display = "block";

    status.textContent = "Camera is off";

    result.textContent = "—";
}


// =========================
// BUTTON EVENTS
// =========================

startButton.addEventListener("click", startCamera);

stopButton.addEventListener("click", stopCamera);