import cv2
import time
from picamera2 import Picamera2
from constants import STUDENT_STRENGTH
import display
import queue
import threading

class FaceAttendance:
    def __init__(self):
        # Constants for Camera
        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8)
        self.recognizer.read('trainer/trainer.yml')
        self.box_color = (255, 0, 255)
        self.cam = Picamera2()
        self.cam.start()

    def face_attendance(self, result_queue: queue.Queue):
        while True:
            frame = self.cam.capture_array()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            faces = self.face_detector.detectMultiScale(
                frame_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            for (x, y, w, h) in faces:
                face_id, confidence = self.recognizer.predict(frame_gray[y:y + h, x:x + w])

                if confidence > 25:
                    print("\n[FAA] Exiting Program and cleaning up stuff")
                    result_queue.put(('face', face_id))
                    return face_id