import cv2
import requests
import time
import base64

CAMERA_INDEX = 0
RTSP_URL = None
# RTSP_URL = "https://192.168.58.157:8090"
# RTSP_URL = "rstp://192.168.58.157:8090/"
# RTSP_URL = "rtsp://192.168.58.87:8554/stream"
# cam = cv2.VideoCapture(RTSP_URL)
cam = cv2.VideoCapture(CAMERA_INDEX)

def generate():
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        # cv2.imshow('frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        
        base64_str = base64.b64encode(jpeg.tobytes()).decode('utf-8')
        data_uri = f"data:image/jpeg;base64,{base64_str}"
        yield data_uri

for frame in generate():
    data = {
        "incident_location": "123 Main St, Springfield",
        "incident_lat": 37.7749,
        "incident_long": -122.4194,
        "incident_image": frame,
        "incident_camera_metadata": {
            "camera_id": "CAM12345",
            "resolution": "1920x1080",
            "frame_rate": "30fps",
            "orientation": "landscape"
        }
    }
    res = requests.post("http://192.168.58.4:8000/api/record_incident", data=data).json()
    print("Sent", res)
    time.sleep(1)