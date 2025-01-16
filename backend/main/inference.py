import tensorflow as tf
import numpy as np
import base64
import json
from PIL import Image
import io
import os
import cv2
from .models import IncidentType

LABELS_PATH = "models/metadata.json"
MODEL_PATH= "models/main_model.tflite"
labels, model = None, None
LABEL_TO_INCIDENT_TYPE = {
    "No_CrossMarker": IncidentType.RED_CLOTH_WITHOUT_REFLECTOR,
    "Has_CrossMarker": IncidentType.REFLECTOR_WITH_RED_CLOTH,
}

def init_load_model():
    global labels, model
    print("Loading model...")
    model = tf.keras.models.load_model(MODEL_PATH)    
    with open(LABELS_PATH, "r") as file:
        labels = json.load(file)['labels']
    print("Model loaded")

def read_vin(base_64_img):
    try:
        import cv2
        from matplotlib import pyplot as plt
        import numpy as np
        import imutils
        import easyocr
        print("Reading VIN...")
        img = preprocess_image(base_64_img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(bfilter, 30, 200)
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        (x, y) = np.where(mask==255)
        (x1,y1) = (np.min(x), np.min(y))
        (x2,y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        print("VIN Result:", result)
        if result:
            return str(result[0])
    except Exception as e:
        print("Error reading VIN:", e)
    
    return None

def preprocess_image(base64_img):
    try:
        base64_img = base64_img.split(",")[1]
        img = base64.b64decode(base64_img)
        img = Image.open(io.BytesIO(img))
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        return False, img

    except Exception as e:
        error_string = (f"Error in preprocessing image: {e}")
        print(error_string)
        return True, error_string

class ModelPredictionResponse:
    def __init__(self, predictions, max_predicted_label, error=None):
        self.predictions = predictions
        self.max_predicted_label = max_predicted_label
        self.error = error

    def to_dict(self):
        return {
            "predictions": self.predictions,
            "max_predicted_label": self.max_predicted_label,
            "error": self.error,
        }

def predict(frame) -> ModelPredictionResponse:
    try:
        print("Predicting...")
        err, data = preprocess_image(frame)
        if err:
            return ModelPredictionResponse(data, None, data)
        output = model.predict(data)[0].tolist()
        predictions = {labels[i]:x for i, x in enumerate((output))}
        max_predicted_label = max(predictions, key=predictions.get)
        print("Predictions: ", output)
        return ModelPredictionResponse(predictions, max_predicted_label)
    
    except Exception as e:
        print("Error predicting: ", e)
        return ModelPredictionResponse(None, None, str(e))
        
class PredictIncidentTypeResponse:
    def __init__(self, predictions_metadata, incident_type:IncidentType, predicted):
        self.predictions_metadata = predictions_metadata
        self.incident_type = incident_type
        self.predicted = predicted

    def to_dict(self):
        return {
            "predictions_metadata": self.predictions_metadata,
            "incident_type": self.incident_type,
            "predicted": self.predicted,
        }

def predict_incident_type(frame) -> PredictIncidentTypeResponse:
    predictions = predict(frame)
    if predictions.error or not predictions.predictions:
        # No predictions
        return None
    
    print("Predictions: ", predictions.predictions)
    
    if round(predictions.predictions['Has_CrossMarker'], 2) == round(predictions.predictions['No_CrossMarker'], 2):
        return PredictIncidentTypeResponse(predictions.to_dict(), IncidentType.REFLECTOR_WITH_RED_CLOTH, True)
    
    incident_type = LABEL_TO_INCIDENT_TYPE[predictions.max_predicted_label]    
    return PredictIncidentTypeResponse(predictions.to_dict(), incident_type, True)
    

init_load_model()