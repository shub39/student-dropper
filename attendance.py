import threading
import queue
from face import FaceAttendance
from fingerprint import FingerprintAttendance
from miscellaneous import show_data
from subject_select import SubjectSelect, subject

result_queue = queue.Queue()

'''
def attendance(result_queue):
    face_thread = threading.Thread(target=FaceAttendance().face_attendance, args=(result_queue,))
    fingerprint_thread = threading.Thread(target=FingerprintAttendance().fingerprint_attendance, args=(result_queue,))

    face_thread.start()
    fingerprint_thread.start()

    result_type, result_value = result_queue.get()

    print(f"[A] First to finish: {result_type} with value: {result_value}")
    if result_type == 'fingerprint':
        pass
    else:
        pass
'''

def attendance():

    if subject == "":
        if not SubjectSelect(): return

    def fingerprint_thread():
        FingerprintAttendance().fingerprint_attendance

    def face_thread():
        FaceAttendance().face_attendance

    thread1 = threading.Thread(target=face_thread)
    thread2 = threading.Thread(target=fingerprint_thread)

    thread1.start()
    thread2.start()

    result_type, result_value = result_queue.get()

    print(f"[A] First to finish: {result_type} with value: {result_value}")

    if result_type == 'fingerprint':
        write_data(index=result_value)
    else:
        write_data(roll=result_value)

attendance()
