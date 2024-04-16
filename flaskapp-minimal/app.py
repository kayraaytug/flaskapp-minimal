
from flask import Flask, render_template, request, url_for, redirect, Response, jsonify
from flask_socketio import SocketIO, emit
import cv2
import time
import os
from flask_cors import CORS, cross_origin


dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app)

screenshot = False
record = False
folder = str()
flag = True
file_path = ''

camera = cv2.VideoCapture(0)
frame_width = int(camera.get(3))
frame_height = int(camera.get(4))
size = (frame_width, frame_height)

################### FUNCTIONS ###################
def gen_frames():

    global folder, record, screenshot, flag

    timestr = time.strftime("%Y%m%d-%H%M%S")
    folder = str(timestr)

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            print("Can't find camera.")
            break

        else:
            if screenshot:
                if not os.path.exists('captures/' + folder):
                    os.mkdir('captures/' + folder)
                timestr = time.strftime("%Y%m%d-%H%M%S")
                cv2.imwrite('captures/' + folder + "/" + timestr + ".jpg", frame)
                screenshot = False
            if record:
                if flag:
                    if not os.path.exists('captures/' + folder):
                        os.mkdir('captures/' + folder)
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    video = cv2.VideoWriter('captures/' + folder + "/" + timestr + '.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         20, size)
                    flag = False
                video.write(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

################### ROUTES ###################
@app.route("/stream")
def stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/screenshot")
def screenshot():
    global screenshot
    screenshot = True

@app.route("/start_record")
def start_record():
    global record
    record = True

@app.route("/stop_record")
def stop_record():
    global record, flag
    record = False
    flag = True
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
