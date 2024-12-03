import cv2
import numpy as np
import os
import shutil
import csv
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import evdev
import sys
import subprocess
from time import sleep
from clear_database import clear_database
from face_trainer import FaceRecognitionTrainer
from fingerprint_enroll import FingerprintEnrollment
from face_enroll import FaceEnrollment

class Admin:
    def display_menu(self):
        print("\n---------------------------- MAIN MENU ---------------------------------")
        print("1. Capture Student Info")
        print("2. Capture Teacher Info")
        print("3. Train Face Models")
        print("4. Exit")
        print("5. Clear Database")
        print("------------------------------------------------------------------------")
        
    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")
            if choice == '4':
                print("[INFO] Exiting the program. Goodbye!")
                break
            elif choice == '1':
                name = input("[INPUT] Enter Name: ")
                roll = input("[INPUT] Enter Roll no: ")
                dept = "DS"
                sem = 3
                fingerprint_class = FingerprintEnrollment()
                fingerprint_class.capture_fingerprint()
                face_class = FaceEnrollment(roll, name, dept, sem)
                face_class.capture_face()
                self.write_student_data(roll, name, dept, sem)
            elif choice == '2':
                name = input("[INPUT] Enter Name: ")
                roll = input("[INPUT] Enter Roll no: ")
                subject = input("[INPUT] Enter Subject Code: ")
                dept = "DS"
                sem = 3
                fingerprint_class = FingerprintEnrollment()
                fingerprint_class.capture_fingerprint()
                face_class = FaceEnrollment(roll, name, dept, sem) # diff database
                face_class.capture_face()
                self.write_teacher_data(roll, name, subject)
            elif choice == '3':
                FaceRecognitionTrainer.train_face_model()
            elif choice == '5':
                clear_database()
    
    def write_student_data(self, roll, name, dept, sem):
        with open("studentdata.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([roll, name, dept, sem])
        print("[INFO] Data saved successfully.")
        
    def write_teacher_data(self, roll, name, subject):
        roll = str(int(roll) + 100)
        with open("teacherdata.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([roll, name, subject])
        print("[INFO] Data saved successfully.")


if __name__ == '__main__':
    admin_run = Admin()
    admin_run.run()
