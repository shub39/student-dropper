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


MENU_OPTIONS = {
    1: "Capture Info",
    2: "Train dataset",
    3: "Exit program",
    4: "Clear database"
}

def main_menu():
    fingerprint = FingerprintSensor()
    face = FaceCaptureTrainer()

    while True:
        print("\n--ADMIN SCRIPT --")
        for key, value in MENU_OPTIONS.items():
            print(f"{key}. {value}")

        option = int(input("Enter your choice: "))

        if option == 1:
            name = input("Enter Name: ")
            roll = int(input("Enter Roll no: "))
            if fingerprint.capture_fingerprint():
                face.capture_faces(roll)
                write_data(fingerprint.index, roll, name)

        elif option == 2:
            face.train_dataset()

        elif option == 3:
            print("Exiting the program. Goodbye!")
            break

        elif option == 4:
            fingerprint.clear_fingerprints()
            clear_database()

        else:
            print("Invalid choice. Please enter a valid option.")
                  
def write_data(index, roll, name):
    with open("studentdata.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([index, roll, name])
    logging.info("Data written")

def clear_database():
    file1 = open('studentdata.csv','w')
    file1.close()
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
