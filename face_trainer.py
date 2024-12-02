import cv2
import numpy as np
import os

class FaceRecognitionTrainer:
    def __init__(self, dataset_path='dataset', trainer_path='trainer', face_cascade_path='haarcascade_frontalface_default.xml'):
        self.dataset_path = dataset_path
        self.trainer_path = trainer_path
        self.face_cascade_path = face_cascade_path
        self.face_detector = cv2.CascadeClassifier(self.face_cascade_path)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def get_images_and_labels(self):
        face_samples = []
        ids = []

        for file_name in os.listdir(self.dataset_path):
            if file_name.endswith(".jpg"):
                id = int(file_name.split(".")[0])
                img_path = os.path.join(self.dataset_path, file_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

                faces = self.face_detector.detectMultiScale(img)
                for (x, y, w, h) in faces:
                    face_samples.append(img[y:y+h, x:x+w])
                    ids.append(id)

        return face_samples, ids

    def train_recognizer(self, faces, ids):
        self.recognizer.train(faces, np.array(ids))
        if not os.path.exists(self.trainer_path):
            os.makedirs(self.trainer_path)
        self.recognizer.write(os.path.join(self.trainer_path, 'trainer.yml'))
        print(f"[INFO] Model trained and saved at {os.path.join(self.trainer_path, 'trainer.yml')}")

    def train_face_model(self):
        print(f"[INFO] Training face model using dataset from {self.dataset_path}")
        faces, ids = self.get_images_and_labels()
        self.train_recognizer(faces, ids)
        faces_trained = len(set(ids))
        print(f"[INFO] {faces_trained} faces trained.\n")
