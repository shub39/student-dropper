import cv2
import numpy as np
import os
import shutil
import csv
from picamera2 import Picamera2
from time import sleep
import sys

class FaceEnrollment:
    def __init__(self, roll, name, dept, sem):
        # Constants
        self.COUNT_LIMIT = 30
        self.POS = (30, 60)
        self.FONT = cv2.FONT_HERSHEY_COMPLEX
        self.HEIGHT = 1.5
        self.TEXTCOLOR = (0, 0, 255)
        self.BOXCOLOR = (255, 0, 255)
        self.WEIGHT = 3

        self.FACE_DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.path = 'dataset'
        
        self.roll = roll
        self.name = name
        self.dept = "CSE(DS)"
        self.sem = 3
        self.count = 0
        self.index = 0

    def capture_face(self):
        self.cam = Picamera2()
        self.cam.preview_configuration.main.size = (640, 360)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.controls.FrameRate = 24
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()

        while True:
            frame = self.cam.capture_array()
            cv2.putText(frame, 'Count:' + str(self.count), self.POS, self.FONT, self.HEIGHT, self.TEXTCOLOR, self.WEIGHT)
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.FACE_DETECTOR.detectMultiScale(
                frameGray,      
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), self.BOXCOLOR, 3)
                self.count += 1 

                if not os.path.exists("dataset"):
                    os.makedirs("dataset")
                if not os.path.exists("old_dataset"):
                    os.makedirs("old_dataset")
                
                file_path = os.path.join("dataset", f"{self.roll}.{self.count}.jpg")
                if os.path.exists(file_path):
                    old_file_path = file_path.replace("dataset", "old_dataset")
                    os.rename(file_path, old_file_path)
                
                cv2.imwrite(file_path, frameGray[y:y + h, x:x + w])

            cv2.imshow('FaceCapture', frame)
            key = cv2.waitKey(100) & 0xff

            if key == 27:
                break
            elif key == 113:
                break
            elif self.count >= self.COUNT_LIMIT:
                break

        print("\n[INFO] Exiting Program and cleaning up stuff")
        cv2.destroyAllWindows()
        self.cam.close()

    def save_data(self):
        if self.count < self.COUNT_LIMIT:
            print("[ERROR] Not enough face images captured!")
            return

        with open("studentdata.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([self.index, self.roll, self.name, self.dept, self.sem])
        
        print("[INFO] DATA WRITTEN\n")
