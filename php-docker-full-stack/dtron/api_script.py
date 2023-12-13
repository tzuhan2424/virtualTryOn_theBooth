from flask import Flask, request, jsonify
import os
import subprocess
import shutil


# import torch

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    #"/var/www/shared/test/image/image.jpg"
    request_image_path = request.form['image']
    # # Extract the original file name from the path
    original_file_name = os.path.basename(request_image_path)
    image_path = os.path.join("/data/shared/test/image", original_file_name)
    
    if os.path.exists(image_path):
        command = [
        'python', 'detectron2/projects/DensePose/apply_net.py', 'show', 
        'detectron2/projects/DensePose/configs/densepose_rcnn_R_50_FPN_s1x.yaml',
        'https://dl.fbaipublicfiles.com/densepose/densepose_rcnn_R_50_FPN_s1x/165712039/model_final_162be9.pkl',
        image_path, 'bbox,dp_segm', '-v'
        ]


        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
        except Exception as e:
            print("An detron error occurred:", e)
        

        move_msg = ""
        generated_image = 'final_visualized_image.jpg'
        if os.path.exists(generated_image):
            destination_folder = '/data/shared/test/image-densepose'
            new_path = os.path.join(destination_folder, original_file_name)
                    # Manually copy the file content
            with open(generated_image, 'rb') as f_src:
                with open(new_path, 'wb') as f_dst:
                    f_dst.write(f_src.read())

            # shutil.move(generated_image, new_path)

            move_msg=f"Moved '{generated_image}' to '{destination_folder}'"
            print(move_msg)
        else:
            move_msg = f"'{generated_image}' does not exist."
            print(move_msg)

        

        return jsonify({"message": "detron Image processed successfully", 'move_msg': move_msg}), 200

    else:
        return jsonify({"error": "File not found", "image_path": image_path}), 404

    






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
