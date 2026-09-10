const camera = document.getElementById("camera");
const startButton = document.getElementById("start-camera");
const stopButton = document.getElementById("stop-camera");

const status = document.getElementById("status");
const cameraMessage = document.getElementById("camera-message");
const result = document.getElementById("result");

const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");

const detectionOverlay =
    document.getElementById("detection-overlay");

let stream = null;
let detectionInterval = null;


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

        // Wait until video dimensions are available
        camera.addEventListener("loadedmetadata", () => {

            canvas.width = camera.videoWidth;
            canvas.height = camera.videoHeight;

            startDetection();

        }, { once: true });

    } catch (error) {

        console.error("Camera error:", error);

        status.textContent = "Unable to access camera";

        cameraMessage.textContent =
            "Please allow camera access.";

        cameraMessage.style.display = "block";
    }
}


// =========================
// DETECTION
// =========================

function startDetection() {

    // Run detection every 100 milliseconds
    detectionInterval = setInterval(() => {

        sendFrame();

    }, 100);

}


async function sendFrame() {

    if (!stream) {
        return;
    }

    // Copy current video frame to canvas
    context.drawImage(
        camera,
        0,
        0,
        canvas.width,
        canvas.height
    );

    // Convert canvas to JPEG
    canvas.toBlob(async (blob) => {

        if (!blob) {
            return;
        }

        const formData = new FormData();

        formData.append(
            "image",
            blob,
            "frame.jpg"
        );

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/detect",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();
            console.log("Backend response:", data);

            // Display detected number
            if (data.number === null) {
                result.textContent = "—";
            } else {
                result.textContent = data.number;
            }

            // Display annotated image
            detectionOverlay.src =
                "data:image/jpeg;base64," + data.image;

        } catch (error) {

            console.error(
                "Detection error:",
                error
            );

            status.textContent =
                "Unable to connect to backend";

        }

    }, "image/jpeg");

}


// =========================
// STOP CAMERA
// =========================

function stopCamera() {

    // Stop webcam
    if (stream) {

        stream.getTracks().forEach(track => {
            track.stop();
        });

        stream = null;
    }

    // Stop detection requests
    if (detectionInterval) {

        clearInterval(detectionInterval);

        detectionInterval = null;
    }

    camera.srcObject = null;

    detectionOverlay.src = "";

    cameraMessage.textContent =
        "Camera is not running";

    cameraMessage.style.display = "block";

    status.textContent =
        "Camera is off";

    result.textContent = "—";
}


// =========================
// BUTTONS
// =========================

startButton.addEventListener(
    "click",
    startCamera
);

stopButton.addEventListener(
    "click",
    stopCamera
);