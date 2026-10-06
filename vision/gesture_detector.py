"""
Optional Computer Vision Gesture Detector for GEMMA WORLD
Uses OpenCV to recognize physical player gestures (Open Hand, Thumbs Up, Fist).
Completely optional: Fails gracefully if OpenCV or a webcam is unavailable.
"""
import threading
import time

class GestureDetector:
    def __init__(self):
        self.is_available = False
        self.is_running = False
        self.latest_event = None
        self.thread = None
        self.cap = None

        # Check if cv2 is installed
        try:
            import cv2
            self.cv2 = cv2
            self.is_available = True
        except ImportError:
            self.cv2 = None
            self.is_available = False

    def start(self):
        """Starts background webcam capture if OpenCV is installed."""
        if not self.is_available or self.is_running:
            return False

        try:
            self.cap = self.cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.is_available = False
                return False
            self.is_running = True
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            return True
        except Exception:
            self.is_available = False
            return False

    def stop(self):
        """Stops webcam capture."""
        self.is_running = False
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

    def get_latest_event(self):
        """Pulls and clears the latest detected gesture event."""
        evt = self.latest_event
        self.latest_event = None
        return evt

    def _capture_loop(self):
        """Background thread detecting hand gestures."""
        cv2 = self.cv2
        last_gesture_time = 0.0

        while self.is_running and self.cap:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue

            current_time = time.time()
            if current_time - last_gesture_time < 2.5:
                # Rate limit gesture emissions to once every 2.5 seconds
                time.sleep(0.05)
                continue

            try:
                # Simple contour and defect based analysis
                frame = cv2.flip(frame, 1)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # Skin tone mask in HSV
                lower_skin = (0, 20, 70)
                upper_skin = (25, 255, 255)
                mask = cv2.inRange(hsv, lower_skin, upper_skin)
                mask = cv2.GaussianBlur(mask, (5, 5), 100)

                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    max_contour = max(contours, key=lambda c: cv2.contourArea(c))
                    area = cv2.contourArea(max_contour)

                    if area > 8000:
                        hull = cv2.convexHull(max_contour, returnPoints=False)
                        if len(hull) > 3:
                            defects = cv2.convexityDefects(max_contour, hull)
                            finger_count = 0
                            if defects is not None:
                                for i in range(defects.shape[0]):
                                    s, e, f, d = defects[i, 0]
                                    if d > 12000:  # Deep defect implies separated fingers
                                        finger_count += 1

                            # Gesture categorization
                            detected = None
                            if finger_count >= 4:
                                detected = "open_hand"
                            elif finger_count == 0:
                                detected = "fist"
                            elif finger_count == 1:
                                detected = "thumbs_up"

                            if detected:
                                self.latest_event = {"visual_event": detected}
                                last_gesture_time = current_time

            except Exception:
                pass

            time.sleep(0.06)
