
import os 
import cv2
from deepface import DeepFace

def detect_emotion(image_path:str) ->str:

    try:
        result = DeepFace.analyze(
            img_path=image_path,
            actions=['emotion'],
            detector_backend='retinaface',
            enforce_detection=True
        )

        if isinstance(result, list):
            result = result[0]

        face_result = result
        emotion = face_result["dominant_emotion"]
        confidence = face_result["emotion"][emotion]
        print("Dominant:", result["dominant_emotion"])
        print (f"Accuracy: {confidence:.2f}%" )

        return emotion
        
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return None