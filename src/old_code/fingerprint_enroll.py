import csv
import sys
from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint

class FingerprintEnrollment:
    def __init__(self, sensor_port='/dev/ttyUSB0'):
        self.index = 0
        try:
            self.f = PyFingerprint(sensor_port, 57600, 0xFFFFFFFF, 0x00000000)
        except Exception as e:
            try:
                self.f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
            except Exception as e:
                print(f"[ERROR] Failed to initialize fingerprint sensor: {str(e)}")
                sys.exit(1)

    def __str__(self):
        return f"Fingerprint Enrollment - Index: {self.index}, Sensor Initialized: {'Yes' if self.f else 'No'}"

    def capture_fingerprint(self):
        print('\n[INFO] FINGERPRINTS CURRENTLY STORED: ' + str(self.f.getTemplateCount()) + '\n')

        try:
            print('[ACTION] PLACE FINGER...\n')
            sleep(1)

            # Capture fingerprint until a valid fingerprint is detected
            while not self.f.readImage():
                pass

            self.f.convertImage(0x01)
            result = self.f.searchTemplate()
            positionNumber = result[0]

            if positionNumber >= 0:
                print(f'\n[INFO] Fingerprint already exists at #{positionNumber + 1}. Try again? (y/n): ')
                choice = input("[INPUT] Enter your Choice: \n")
                if choice.lower() == 'y':
                    return self.capture_fingerprint()  # Retry
                return None  # Exit if the user doesn't want to retry

            else:
                print('[ACTION] REMOVE FINGER\n')

                while self.f.readImage():
                    pass

                print('[ACTION] PLACE FINGER AGAIN\n')
                sleep(0.5)

                while not self.f.readImage():
                    pass

                self.f.convertImage(0x02)

                if self.f.compareCharacteristics() == 0:
                    print('[E] FINGERPRINTS DON’T MATCH. TRY AGAIN? (y/n)\n')
                    choice = input("Enter your Choice: ")
                    if choice.lower() == "y":
                        return self.capture_fingerprint()
                    return None

                self.f.convertImage(0x02)
                self.f.createTemplate()
                positionNumber = self.f.storeTemplate()
                print('[INFO] FINGERPRINT REGISTERED AT #' + str(positionNumber + 1) + '\n')
                self.index = str(positionNumber + 1)
                return self.index

        except Exception as e:
            print('[E] CAPTURE FINGERPRINT FAILED - ' + str(e) + '\n')
            return None

    def save_data(self, roll, name, dept, sem):
        if self.index == 0:
            print("[ERROR] No fingerprint enrolled. Cannot save data.")
            return

        with open("studentdata.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([self.index, roll, name, dept, sem])
        print("[INFO] DATA WRITTEN\n")
