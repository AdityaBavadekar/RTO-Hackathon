import cv2
import flask

CAMERA_INDEX = 0
cam = cv2.VideoCapture(CAMERA_INDEX)

app = flask.Flask(__name__)

@app.route('/video_feed')
def cam_stream():
    def generate():
        while True:
            ret, frame = cam.read()
            if not ret:
                break
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    return flask.Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return flask.render_template('index.html')

app.run(host='0.0.0.0', port=5000)