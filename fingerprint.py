import time
from pyfingerprint.pyfingerprint import PyFingerprint
import display
import queue

class FingerprintAttendance:
    def __init__(self):
        try:
            self.f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        except Exception as e:
            try:
                self.f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
            except Exception as e:
                print(f"[E] CANT INITIALISE SENSOR: {str(e)}")
    
    def fingerprint_attendance(self, result_queue: queue.Queue):
        time_tuple = time.localtime()
        samay = time.strftime('%H:%M', time_tuple)

        try:
            display.draw(["PLACE FINGER", "Subject", "Date"])
            print('\n[FA] PLACE FINGER...')
            while (self.f.readImage() == False):
                pass

            self.f.convertImage()
            result = self.f.searchTemplate()

            if result[0] == -1:
                display.draw(["NO MATCH", "TRY AGAIN"])
                print('[FA] NO MATCH TRY AGAIN' + '\n')
                time.sleep(2)
                return self.fingerprint_attendance(result_queue)
            else:
                display.draw(["FOUND FINGERPRINT "+ str(result[0] + 1)])
                print('[FA] FOUND FINGERPRINT ' + str(result[0] + 1) + '\n')
                result_queue.put(('fingerprint', result[0] + 1))
                time.sleep(1)
                return result[0] + 1

        except Exception as e:
            display.draw(["ERROR DETECTING", "FINGERPRINT"])
            print("[E] ERROR DETECTING FINGERPRINT", e)

