import queue

from main.face import FaceAttendance

def face_test():
    result = queue.Queue()
    face = FaceAttendance()
    print(face.face_attendance(result))