from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import tempfile
import os

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def detect_objects():
    # Get the video file from the request
    video_file = request.files['video']
    data = request.json
    
    # Read the video file
    video = cv2.VideoCapture(video_file)
    yolo_model = YOLO(data['weight_path'])

    results = []
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        # Process each frame
        result= yolo_model(frame)
        results.append(result)
    
    # Release the video capture
    video.release()
    
    return jsonify(results)

@app.route('/train', methods=['POST'])
def train_model():

    yaml_dir = 'yaml_files'
    if not os.path.exists(yaml_dir):
        os.makedirs(yaml_dir)
    # Get the YAML file for training
    yaml_file = request.files['config_path']
    
    # Save the YAML file to the location
    yaml_path = os.path.join(yaml_dir, yaml_file.filename)
    yaml_file.save(yaml_path)
    
    # Load YOLO model for training
    yolo_model = YOLO(yaml_path.name)
    
    # Train the model
    results = yolo_model.train(data=yaml_path.name, epochs=500, imgsz=640)
    
    # Return training results
    return jsonify({'weigth_path': yaml_path.name + '.pt'})

if __name__ == '__main__':
    app.run()