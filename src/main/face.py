import cv2
import time
import queue
import threading
import logging

from picamera2 import Picamera2

from display import draw

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class FaceAttendance:
    """class to handle face detection"""
    def __init__(self):
        try:
            self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            self.recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8)
            self.recognizer.read('trainer/trainer.yml')
            self.box_color = (255, 0, 255)
            self.cam = Picamera2()
            self.cam.start()
        except Exception as e:
            logging.info("failed to initialize face class %s", e)

    def face_attendance(self, result_queue: queue.Queue):
        start_time = time.time()

        while time.time() - start_time < 5:
            logging.info("starting face detection")
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

                if time.time() - start_time >= 5:
                    logging.info("face detection timed out")
                    return None

                if confidence > 25:
                    logging.info("exiting face detection")
                    result_queue.put(("face", face_id))
                    return face_id

        logging.info("face detection timed out")
        return None