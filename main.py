import cv2
import mediapipe as mp

connections = [
    # Thumb
    (0,1),
    (1,2),
    (2,3),
    (3,4),
    # Index finger
    (0,5),
    (5,6),
    (6,7),
    (7,8),
    # Middle finger
    (0,9),
    (9,10),
    (10,11),
    (11,12),
    # Ring finger
    (0,13),
    (13,14),
    (14,15),
    (15,16),
    # Pinky
    (0,17),
    (17,18),
    (18,19),
    (19,20),
    # Palm connections
    (5,9),
    (9,13),
    (13,17)
]
def draw_connections(frame, landmarks):
    h,w,_ = frame.shape
    for start,end in connections:
        x1 = int(landmarks[start].x*w)
        y1 = int(landmarks[start].y*h)

        x2 = int(landmarks[end].x*w)
        y2 = int(landmarks[end].y*h)
        cv2.line(
            frame,
            (x1,y1),
            (x2,y2),
            (255,0,0),
            2
        )
def draw_points(frame, landmarks):
    h,w,_ = frame.shape
    for point in landmarks:
        x = int(point.x*w)
        y = int(point.y*h)
        cv2.circle(
            frame,
            (x,y),
            5,
            (0,255,0),
            -1
        )

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
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            draw_points(frame, hand_landmarks)
            draw_connections(frame,hand_landmarks)
    cv2.imshow(
        "Camera",
        frame
    )
    if cv2.waitKey(1) == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
