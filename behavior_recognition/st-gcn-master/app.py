from flask import Flask, request, jsonify
import argparse
import sys
import subprocess

# torchlight
import torchlight
from torchlight import import_class

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def train():
    data = request.get_json()
    
    config_file = request.files['config_path']
    weight_file = request.files['weight_path']
    keypoint_data = data.get('keypoint_data')
    
    command = f"python main.py predict --keypoint_data {keypoint_data} --config {config_file} --weights{weight_file}"
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
  
    prediction_result = {'prediction': output}
    
    return jsonify(prediction_result)

@app.route('/train', methods=['POST'])
def train():
    
    #data = request.get_json()
    
    config_file = request.files['config_path']
    
    command = f"python main.py recognition -c {config_file} --work_dir ./]"
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
  
    
    return jsonify({'weigth_path': config_file.name + '.pt','config_path': os.path.abspath(config_file)})

if __name__ == '__main__':
    app.run(debug=True)