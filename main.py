import cv2
from detector import HandDetector

detector = HandDetector()
camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()
    if not success:
        break
    # Detect hand
    count = detector.detect(frame)
    if count == None:
        text = "No hand detected"
    else:
        text = f"Number : {count}"
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow(
        "Hand Detection",
        frame
    )
    if cv2.waitKey(1) == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
