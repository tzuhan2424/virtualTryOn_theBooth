from flask import Flask, request, jsonify


# import torch

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    return 1

    






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
