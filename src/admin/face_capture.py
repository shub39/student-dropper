import os
import logging
import cv2
import numpy as np
from picamera2 import Picamera2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class FaceCaptureTrainer:
    def __init__(self, count_limit=30, dataset_path="dataset", old_dataset_path="old_dataset"):
        self.COUNT_LIMIT = count_limit
        self.dataset_path = dataset_path
        self.old_dataset_path = old_dataset_path
        self.POS = (30, 60)
        self.FONT = cv2.FONT_HERSHEY_COMPLEX
        self.HEIGHT = 1.5
        self.TEXT_COLOR = (0, 0, 255)
        self.BOX_COLOR = (255, 0, 255)
        self.WEIGHT = 3
        self.FACE_DETECTOR = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
        self.cam = Picamera2()
        self.cam.preview_configuration.main.size = (640, 360)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.controls.FrameRate = 24
        self.cam.preview_configuration.align()
        self.cam.configure("preview")

    def capture_faces(self, roll):
        """Capture faces and save them to the dataset."""
        self.cam.start()

        count = 0
        os.makedirs(self.dataset_path, exist_ok=True)
        os.makedirs(self.old_dataset_path, exist_ok=True)

        try:
            while True:
                frame = self.cam.capture_array()
                cv2.putText(frame, f'Count: {count}', self.POS, self.FONT, self.HEIGHT, self.TEXT_COLOR, self.WEIGHT)
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = self.FACE_DETECTOR.detectMultiScale(
                    frame_gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), self.BOX_COLOR, 3)
                    count += 1

                    file_path = os.path.join(self.dataset_path, f"{roll}.{count}.jpg")
                    if os.path.exists(file_path):
                        old_file_path = file_path.replace(self.dataset_path, self.old_dataset_path)
                        os.rename(file_path, old_file_path)

                    cv2.imwrite(file_path, frame_gray[y:y + h, x:x + w])

                cv2.imshow('FaceCapture', frame)
                key = cv2.waitKey(100) & 0xFF

                if key in [27, 113] or count >= self.COUNT_LIMIT:
                    break

        except Exception as e:
            logging.error("Error during face capture: %s", e)

        finally:
            logging.info("Exiting Program and cleaning up resources.")
            cv2.destroyAllWindows()
            if self.cam: self.cam.close()

    def train_dataset(self):
        """Public function that trains the face model"""
        logging.info("Training face model")
        faces, ids = self._getImagesAndLabels(self.dataset_path)
        self._trainRecognizer(faces, ids)
        faces_trained = len(set(ids))
        logging.info("Training complete. Faces trained: %s", faces_trained)

    def _trainRecognizer(self, faces, ids):
        """Trains the recognizer and stores at root/trainer/"""
        self.RECOGNIZER.train(faces, np.array(ids))
        if not os.path.exists("trainer"):
            os.makedirs("trainer")
        self.RECOGNIZER.write('trainer/trainer.yml')

    def _getImagesAndLabels(self, path):
        """Gets info on paths and extract the ids"""
        faceSamples = []
        ids = []

        for file_name in os.listdir(path):
            if file_name.endswith(".jpg"):
                iden = int(file_name.split(".")[0])
                img_path = os.path.join(path, file_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

                faces = self.FACE_DETECTOR.detectMultiScale(img)

                for (x, y, w, h) in faces:
                    faceSamples.append(img[y:y + h, x:x + w])
                    ids.append(iden)
        return faceSamples, ids