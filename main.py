import cv2
import mediapipe as mp


# Create hand detector
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.IMAGE
)

detector = HandLandmarker.create_from_options(options)
camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()
    if not success:
        break
    # Convert BGR -> RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )
    # Convert image for MediaPipe
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )
    # Detect hand
    result = detector.detect(mp_image)
    print(result)
    cv2.imshow(
        "Camera",
        frame
    )
    if cv2.waitKey(1) == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()