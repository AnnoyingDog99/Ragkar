import cv2
import urllib.request
import numpy as np

def mjpeg_stream():
    vcap = cv2.VideoCapture("http://192.168.0.107/cam.mjpeg")
    while True:
        success, frame = vcap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpeg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def rtsp_stream():
    vcap = cv2.VideoCapture("rtsp://192.168.0.107:8554/mjpeg/1")
    while True:
        success, frame = vcap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpeg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def jpg_stream():
    while True:
        img_response=urllib.request.urlopen('http://192.168.0.107/cam.jpg')
        img_np=np.array(bytearray(img_response.read()),dtype=np.uint8)
        img=cv2.imdecode(img_np,-1)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
