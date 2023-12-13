from flask import Flask, request, jsonify
import os
import subprocess
import shutil
app = Flask(__name__)
host = '0.0.0.0'  # Replace with the desired IP address
port = 5003        # Replace with the desired port number


@app.route('/pgn_process', methods=['POST'])
def pgn_process():
    request_image_path = request.form['image']
    original_file_name = os.path.basename(request_image_path)
    root='/home/lintzuh@kean.edu/virtualTryOn/projectData/test/'
    image_path = os.path.join(root, 'image',original_file_name)
    tmp_dir = '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/CIHP_PGN/project_tmp'

    # Create tmp_dir if it does not exist
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    
    if os.path.exists(image_path):
             
        shutil.copy(image_path, tmp_dir)
        out_dir = '/home/lintzuh@kean.edu/virtualTryOn/projectData/test' 

        #use testG still weird, because I still try to solve the depedency issue, so I change package
        # if I could use tf then this flask env is not neccessary
        inf_pgn_project_command = [
            '/home/lintzuh@kean.edu/miniconda3/envs/tf/bin/python',  # Path to the Python executable in the desired environment
            '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/CIHP_PGN/inf_pgn_project.py',  # Script name
            '-i', tmp_dir,                # Input directory argument
            '-o', out_dir                 # Output directory argument
        ]

        # inf_pgn_project_command = [
        #     '/home/lintzuh@kean.edu/miniconda3/envs/tf/bin/python',  # Path to the Python executable in the desired environment
        #     '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/CIHP_PGN/inf_pgn_project.py',  # Script name
        #     '-i','/home/lintzuh@kean.edu/virtualTryOn/projectData/test/image' ,                # Input directory argument
        #     '-o', out_dir                 # Output directory argument
        # ]

        result = subprocess.run(inf_pgn_project_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        remove_files_in_directory(tmp_dir)

        return jsonify({"message": "CIHP success"}), 200


    else:
        return jsonify({"error": "File not found", "image_path": image_path}), 404
    


def remove_files_in_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove the file    








if __name__ == '__main__':
     app.run(host=host, port=port)