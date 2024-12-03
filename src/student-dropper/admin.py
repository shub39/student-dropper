"""
Script to enroll data and train face dataset
Run this in GUI through VNC or HDMI
"""

import csv
import os
import shutil
import sys
from time import sleep

import cv2
import numpy as np
from picamera2 import Picamera2
from pyfingerprint.pyfingerprint import PyFingerprint

from constants import DEPT, SEM

# Constants
COUNT_LIMIT = 30
POS = (30, 60)
FONT = cv2.FONT_HERSHEY_COMPLEX
HEIGHT = 1.5
TEXT_COLOR = (0, 0, 255)
BOX_COLOR = (255, 0, 255)
WEIGHT = 3
FACE_DETECTOR = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
PATH = "dataset"

# Student Details
NAME = ""
ROLL = 0
INDEX = 0

# Try to initialise the Fingerprint Sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    try:
        f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
    except Exception as e:
        print("Can't Initialise fingerprint sensor: ", e)
        sys.exit(1)

def main_menu():
    global NAME, ROLL
    while True:
        print("\n--ADMIN SCRIPT --")
        print("1. Capture Info")
        print("2. Train Image Dataset")
        print("3. Exit Program")
        print("4. Clear Database")
        print("---\n")

        option = int(input("\n[INPUT] Enter Your Choice: "))

        if option == 1:
            NAME = input("[INPUT] Enter Name: ")
            ROLL = int(input("[INPUT] Enter Roll no: "))
            if capture_fingerprint() is not None:
                capture_face()
                write_data()

        elif option == 2:
            train_dataset()

        elif option == 3:
            print("\n[BYE] Exiting the program. Goodbye!")
            break

        elif option ==4:
            clear_database()

        else:
            print("\n[E] Invalid choice. Please enter a valid option.\n")
                  
def capture_fingerprint():
    global ROLL, NAME, INDEX
    print('\n[INFO] FINGERPRINTS CURRENTLY STORED: ' + str(f.getTemplateCount()))
    
    try:
        print('[ACTION] PLACE FINGER...\n')
        sleep(1)
        
        while not f.readImage(): pass
        
        f.convertImage(0x01)

        result = f.searchTemplate()
        position_number = result[0]
        
        if position_number >= 0:
            print('\n[INFO] Already exists at #' + str(position_number + 1) + ' Try Again (y/n): ')
            choice = input("[INPUT] Enter your Choice: \n")
            if choice == "y":
                return capture_fingerprint()
            else:
                return None
        
        else:
            print('[ACTION] REMOVE FINGER\n')

            while f.readImage():
                pass
            
            print('[ACTION] PLACE FINGER AGAIN\n')
            sleep(0.5)
            
            while not f.readImage():
                pass
            
            f.convertImage(0x02)
            
            if f.compareCharacteristics() == 0:
                print('[E] FINGERPRINTS DONT MATCH. TRY AGAIN? (y/n)\n')
                choice = input("Enter your Choice: ")
                if choice == "y":
                    return capture_fingerprint()
                else:
                    return None
            
            f.convertImage(0x02)
            f.createTemplate()
            position_number = f.storeTemplate()
            print('[INFO] FINGERPRINT REGISTERED AT #' + str(position_number + 1) + '\n')
            INDEX = str(position_number + 1)
            return 1

    except Exception as e:
        print('[E] CAPTURE FINGERPRINT FAILED - ' + str(e) + '\n')
        print("[E] TRY AGAIN? (y/n)")
        choice = input("[INPUT] Enter Your Choice: ")
        if choice == "y":
            return capture_fingerprint()
        else:
            return None

def write_data():
    global ROLL, NAME, INDEX

    with open("studentdata.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([INDEX, ROLL, NAME, DEPT, SEM])
    
    ROLL = 0
    INDEX = 0
    NAME = ""
    
    print("[INFO] DATA WRITTEN\n")

def train_dataset():
    print(f"\n[INFO] TRAINING FACE MODEL\n")
    faces, ids = getImagesAndLabels(PATH)
    trainRecognizer(faces, ids)
    faces_trained = len(set(ids))
    print(f"\n[INFO] {faces_trained} FACES TRAINED.\n")
    
def getImagesAndLabels(path):
    faceSamples = []
    ids = []

    for file_name in os.listdir(path):
        if file_name.endswith(".jpg"):
            id = int(file_name.split(".")[0])
            img_path = os.path.join(path, file_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            faces = FACE_DETECTOR.detectMultiScale(img)

            for (x, y, w, h) in faces:
                faceSamples.append(img[y:y+h, x:x+w])
                ids.append(id)

    return faceSamples, ids

def clear_database():
    f.clearDatabase()
    file1 = open('studentdata.csv','w')
    file1.close()
    try:
        shutil.rmtree("old_dataset")
    except OSError as e:
        print("[INFO] NO OLD DATASET FOLDER")
    try:
        shutil.rmtree("dataset")
    except OSError as e:
        print("[INFO] NO DATASET FOLDER")
    print('[INFO] ALL DATA CLEARED\n')
    sleep(2)

def trainRecognizer(faces, ids):
    RECOGNIZER.train(faces, np.array(ids))
    if not os.path.exists("trainer"):
        os.makedirs("trainer")
    RECOGNIZER.write('trainer/trainer.yml')

def capture_face():
    global ROLL
    cam = Picamera2()
    cam.preview_configuration.main.size = (640, 360)
    cam.preview_configuration.main.format = "RGB888"
    cam.preview_configuration.controls.FrameRate = 24
    cam.preview_configuration.align()
    cam.configure("preview")
    cam.start()
    count = 0

    while True:
        frame = cam.capture_array()
        cv2.putText(frame, 'Count:' + str(int(count)), POS, FONT, HEIGHT, TEXT_COLOR, WEIGHT)
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_DETECTOR.detectMultiScale(
            frameGray,      
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), BOX_COLOR, 3)
            count += 1 

            if not os.path.exists("dataset"):
                os.makedirs("dataset")
            if not os.path.exists("old_dataset"):
                os.makedirs("old_dataset")
            file_path = os.path.join("dataset", f"{ROLL}.{count}.jpg")
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
        elif count >= COUNT_LIMIT: 
            break

    print("\n[INFO] Exiting Program and cleaning up stuff")
    cv2.destroyAllWindows()
    cam.close()
    
if __name__ == '__main__':
    main_menu()
