import logging
from pyfingerprint.pyfingerprint import PyFingerprint
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class FingerprintSensor:
    def __init__(self):
        """Initialize the fingerprint sensor."""
        try:
            self.f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        except Exception as e:
            try:
                self.f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
            except Exception as e:
                logging.error("Can't initialize FingerprintSensor: %s", e)
                sys.exit(1)

        self.index = 0
        logging.info("Fingerprint sensor initialized successfully.")

    def capture_fingerprint(self):
        """Capture a fingerprint and store it if it's unique."""
        logging.info("Starting fingerprint capture process.")
        logging.info("Number of stored fingerprints: %d", self.f.getTemplateCount())

        try:
            logging.info("Please place your finger on the sensor.")
            while not self.f.readImage():
                pass

            self.f.convertImage(0x01)
            result = self.f.searchTemplate()
            position_number = result[0]

            if position_number >= 0:
                logging.warning("Fingerprint already exists at position #%d.", position_number + 1)
                return self._retry_capture()

            logging.info("Remove your finger.")
            while self.f.readImage():
                pass

            logging.info("Place your finger again.")
            while not self.f.readImage():
                pass

            self.f.convertImage(0x02)

            if self.f.compareCharacteristics() == 0:
                logging.warning("Fingerprints do not match.")
                return self._retry_capture()

            self.f.createTemplate()
            self.index = self.f.storeTemplate()
            logging.info("Fingerprint stored successfully at position #%d.", self.index + 1)
            return True

        except Exception as e:
            logging.error("Error during fingerprint capture: %s", e)
            return self._retry_capture()

    def clear_fingerprints(self):
        """Clear all fingerprints stored in the database."""
        try:
            self.f.clearDatabase()
            logging.info("All fingerprints cleared successfully.")
        except Exception as e:
            logging.error("Failed to clear fingerprints: %s", e)

    def _retry_capture(self):
        """Ask the user if they want to retry the fingerprint capture."""
        choice = input("Do you want to try again? (y/n): ").strip().lower()
        if choice == "y":
            return self.capture_fingerprint()
        else:
            logging.info("Fingerprint capture process aborted by the user.")
            return False
