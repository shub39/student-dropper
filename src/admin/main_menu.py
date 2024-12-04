"""
Script to enroll data and train face dataset
Run this in GUI through VNC or HDMI
"""

import csv
import logging
import os
import shutil

from fingerprint import FingerprintSensor
from face_capture import FaceCaptureTrainer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

MENU_OPTIONS = {
    1: "Capture Student Info",
    2: "Capture Teacher Info",
    3: "Train dataset",
    4: "Exit program",
    5: "Clear database"
}

def main_menu():
    fingerprint = FingerprintSensor()
    face = FaceCaptureTrainer()

    while True:
        print("\n--ADMIN SCRIPT --")
        for key, value in MENU_OPTIONS.items():
            print(f"{key}. {value}")

        option = input("Enter your choice: ")

        if option == "1":
            name = input("Enter Name: ")
            roll = int(input("Enter Roll no: "))
            if fingerprint.capture_fingerprint():
                face.capture_faces(roll)
                write_student_data(fingerprint.index, roll, name)

        if option == "2":
            name = input("Enter name: ")
            subject = input("Enter subject: ")
            roll = int(input("Enter Roll no: "))
            if fingerprint.capture_fingerprint():
                face.capture_faces(roll + 100) # for easier detection
                write_teacher_data(fingerprint.index, roll + 100, name, subject)


        elif option == "3":
            face.train_dataset()

        elif option == "4":
            print("Exiting the program. Goodbye!")
            break

        elif option == "5":
            fingerprint.clear_fingerprints()
            clear_database()

        else:
            print("Invalid choice. Please enter a valid option.")
                  
def write_student_data(index, roll, name):
    with open("studentdata.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([index, roll, name])
    logging.info("Data written")

def write_teacher_data(index, roll, name, subject):
    with open("teacherdata.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([index, roll, name, subject])
    logging.info("Data writter")

def clear_database():
    open("studentdata.csv","w").close()
    open("teacherdata.csv", "w").close()
    try:
        shutil.rmtree("old_dataset")
    except:
        logging.info("No old dataset folder")
    try:
        shutil.rmtree("dataset")
    except:
        logging.info("No dataset folder")

    logging.info("All data cleared successfully")

if __name__ == '__main__':
    main_menu()
