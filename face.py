import cv2
import numpy as np
from picamera2 import Picamera2

font = cv2.FONT_HERSHEY_COMPLEX
font_scale = 0.8
font_thickness = 2
box_color = (0, 0, 255)
name_color = (255, 255, 255)
conf_color = (255, 255, 0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8)
recognizer.read('trainer/trainer.yml')

names = [str(i) for i in range(1, 61)]

cam = Picamera2()
cam.start()



def face_recognition():
    detected = False
	while not detected:
		frame = cam.capture_array()
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

		# Detect faces in the frame
		faces = face_detector.detectMultiScale(
			frame_gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30)
		)

		print(f"Number of faces detected: {len(faces)}")

		for (x, y, w, h) in faces:
			name_pos = (x + 5, y - 5)
			conf_pos = (x + 5, y + h + 20)
			cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 3)
			id, confidence = recognizer.predict(frame_gray[y:y + h, x:x + w])

			if id >= len(names) or id < 0:
				id = "unknown"
            confidence = "N/A"
			else:
				confidence = f"{100 - confidence:.0f}%"
				print(f"ID: {id}, Confidence: {confidence}")
				print("\n [INFO] Exiting Program and cleaning up stuff")
				detected = True
				cam.stop()