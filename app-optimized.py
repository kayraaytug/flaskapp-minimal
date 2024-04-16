from flask import Flask, Response
import cv2
import time
import os

app = Flask(__name__)

camera = cv2.VideoCapture("/dev/video0")
frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (frame_width, frame_height)

def gen_frames():
    folder = time.strftime("%Y%m%d-%H%M%S")
    while True:
        success, frame = camera.read()
        if not success:
            print("Can't find camera.")
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/stream")
def stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/screenshot")
def take_screenshot():
    folder = time.strftime("%Y%m%d-%H%M%S")
    if not os.path.exists(f"captures/{folder}"):
        os.makedirs(f"captures/{folder}")
    success, frame = camera.read()
    if success:
        cv2.imwrite(f"captures/{folder}/{time.strftime('%Y%m%d-%H%M%S')}.jpg", frame)
    return "Screenshot taken!"

@app.route("/start_record")
def start_record():
    global recording
    recording = True
    global video_writer
    folder = time.strftime("%Y%m%d-%H%M%S")
    if not os.path.exists(f"captures/{folder}"):
        os.makedirs(f"captures/{folder}")
    video_writer = cv2.VideoWriter(f"captures/{folder}/{time.strftime('%Y%m%d-%H%M%S')}.avi",
                                   cv2.VideoWriter_fourcc(*'MJPG'),
                                   20, size)
    return "Recording started!"

@app.route("/stop_record")
def stop_record():
    global recording
    recording = False
    global video_writer
    video_writer.release()
    return "Recording stopped!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
