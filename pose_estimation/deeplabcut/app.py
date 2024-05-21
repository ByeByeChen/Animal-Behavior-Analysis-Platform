from flask import Flask, request, jsonify
from dlc_interface import DeepLabCutProcessor
from werkzeug.utils import secure_filename
import os
import csv 
import json

app = Flask(__name)

app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/predict', methods=['POST'])
def predict():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    data = request.json
    task = "Testcore"
    scorer = "Mackenzie"
    filename = data['filename']
    path_config_file = data['config_path']
    video_path = 'uploads/' + filename
    result_path = 'uploads/'+filename+'efficentnet-b6.csv'
    dlc_processor = DeepLabCutProcessor(task, scorer,video_path,path_config_file)
    dlc_processor.inference(video_path)
    result = dlc_processor.predict(data)
    if result == True:
        return csv_to_json(result_path)
    else:
        return jsonify({'error': 'Reference faild'})
    
    

@app.route('/train', methods=['POST'])
def train():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    data = request.json
    task = "Testcore"
    scorer = "Mackenzie"
    #path_config_file = './normal_config.yaml'
    filename = data['filename']
    video_path = 'uploads/' + filename
    dlc_processor = DeepLabCutProcessor(task, scorer,video_path)
    result = dlc_processor.train(data)
    response = jsonify(result)
    
    return response

def csv_to_json(file_path): 

    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            data.append(row)

    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True)