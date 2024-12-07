import time
import queue
import logging
import sys

from pyfingerprint.pyfingerprint import PyFingerprint
from display import draw

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class FingerPrintAttendance:
    """class for fingerprint attendance utilities"""
    def __init__(self):
        try:
            self.f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        except Exception as e:
            try:
                self.f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
            except Exception as e:
                logging.error("Can't initialize FingerprintSensor: %s", e)
                sys.exit(1)

    def fingerprint_attendance(self, result_queue: queue.Queue):
        try:
            logging.info("place finger on sensor")

            start_time = time.time()

            while self.f.readImage() == False:
                if time.time() - start_time < 5:
                    pass
                else:
                    logging.info("fingerprint detection timed out")
                    return None


            self.f.convertImage()
            result = self.f.searchImage()

            if result[0] == -1:
                draw(["no match", "try again"], 2)
                logging.info("no match found try again.")
                return None
            else:
                draw(["found fingerprint " + str(result[0])], 1)
                logging.info("found fingerprint " + str(result[0]))
                result_queue.put(("fingerprint", result[0]))
                return result[0]

        except Exception as e:
            draw(["error detecting", "fingerprint"])
            logging.info("error detecting fingerprint %s", e)
            return None