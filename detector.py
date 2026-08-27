import cv2
import mediapipe as mp
import math

class HandDetector:
    def __init__(self):
        # Create hand detector
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="hand_landmarker.task"
            ),
            running_mode=VisionRunningMode.IMAGE, num_hands=1
        )

        self.detector = HandLandmarker.create_from_options(options)

    #Functions
    connections = [
        # Thumb
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        # Index finger
        (0, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        # Middle finger
        (0, 9),
        (9, 10),
        (10, 11),
        (11, 12),
        # Ring finger
        (0, 13),
        (13, 14),
        (14, 15),
        (15, 16),
        # Pinky
        (0, 17),
        (17, 18),
        (18, 19),
        (19, 20),
        # Palm connections
        (5, 9),
        (9, 13),
        (13, 17)
    ]

    def draw_connections(self, frame, landmarks):
        h, w, _ = frame.shape
        for start, end in self.connections:
            x1 = int(landmarks[start].x * w)
            y1 = int(landmarks[start].y * h)

            x2 = int(landmarks[end].x * w)
            y2 = int(landmarks[end].y * h)
            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

    def draw_points(self, frame, landmarks):
        h, w, _ = frame.shape
        for point in landmarks:
            x = int(point.x * w)
            y = int(point.y * h)
            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

    def finger_is_open_basic(self, landmarks, tip, joint):
        return landmarks[tip].y < landmarks[joint].y

    def count_fingers(self, landmarks, hand_label):
        index_open = self.is_finger_open(landmarks, 5, 6, 8)
        middle_open = self.is_finger_open(landmarks, 9, 10, 12)
        ring_open = self.is_finger_open(landmarks, 13, 14, 16)
        pinky_open = self.is_finger_open(landmarks, 17, 18, 20)
        if hand_label == "Right":
            thumb_open = self.finger_is_open_basic(landmarks, 3, 4)
        elif hand_label == "Left":
            thumb_open = self.finger_is_open_basic(landmarks, 3, 4)
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

    def calculate_angle(self, a, b, c):
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

    def is_finger_open(self, landmarks, base, joint, tip):
        """
        Determine whether finger opens using calculate_angle function.
        """
        angle = self.calculate_angle(
            landmarks[base],
            landmarks[joint],
            landmarks[tip]
        )
        return angle > 150

    def detect(self, frame):
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
        result = self.detector.detect(mp_image)
        if not result.hand_landmarks:
            return None
        # Get first hand
        landmarks = result.hand_landmarks[0]
        # Get left/right label
        hand_label = result.handedness[0][0].category_name
        # Draw
        self.draw_points(frame,landmarks)
        self.draw_connections(frame,landmarks)
        # Count fingers
        count = self.count_fingers(landmarks,hand_label)
        return count