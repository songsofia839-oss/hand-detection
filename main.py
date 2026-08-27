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

def finger_is_open(landmarks, tip, joint):
    return landmarks[tip].y < landmarks[joint].y

def count_fingers(landmarks, hand_label):
    index_open = finger_is_open(landmarks, 8, 6)
    middle_open = finger_is_open(landmarks, 12, 10)
    ring_open = finger_is_open(landmarks, 16, 14)
    pinky_open = finger_is_open(landmarks, 20, 18)
    if hand_label == "Right":
        thumb_open = finger_is_open(landmarks, 4, 3)
    elif hand_label == "Left":
        thumb_open = finger_is_open(landmarks, 3, 4)
    count = 0
    if thumb_open:
        count += 1
    if index_open:
        count += 1
    if middle_open:
        count += 1
    if ring_open:
        count += 1
    if pinky_open:
        count += 1
    return count

import math


def calculate_angle(a, b, c):
    """
    Calculate angle ABC using three landmarks.
    """

    angle = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x)
        - math.atan2(a.y - b.y, a.x - b.x)
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle

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
            hand_label = (
                result.handedness[0][0].category_name
            )
            count = count_fingers(hand_landmarks, hand_label)

            cv2.putText(
                frame,
                f"Number: {count}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 255, 0),
                3
            )

    cv2.imshow(
        "Camera",
        frame
    )
    if cv2.waitKey(1) == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
