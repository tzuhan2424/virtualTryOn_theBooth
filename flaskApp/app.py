from flask import Flask, request, jsonify
import os
import subprocess
import shutil

app = Flask(__name__)
host = '0.0.0.0'  # Replace with the desired IP address
port = 5002        # Replace with the desired port number

def writeTheDataList(cname, pname, root):
    # Content to be written to the file
    content = f"{cname} {pname}"
    file_name = "pairs.txt"
    filepath = os.path.join(root, file_name)

    # Writing to the file
    try:
        with open(filepath, 'w') as file:
            file.write(content)
        message = f"File '{filepath}' has been written successfully."
    except Exception as e:
        message = f"An error occurred: {e}"

# $fields = [
#     'customer_id' => '1', // Replace with actual customer id
#     'customer_imageName' => 'tzuhan.jpg', // Replace with actual image name
#     'product_id' => '1', // Replace with actual product id
#     'product_image' => '00013_00.jpg', // Replace with actual product image name
# ];
        
def search_and_replace(image_name, dataroot):
    clothPath = os.path.join(dataroot, 'cloth', image_name)
    clothmaskPaht = os.path.join(dataroot, 'cloth-mask', image_name)

    # Check if image is in cloth or cloth_mask directories
    image_in_cloth = os.path.exists(clothPath)
    image_in_cloth_mask = os.path.exists(clothmaskPaht)
    print('image_in_cloth', clothPath)
    dummycloth = '/home/lintzuh@kean.edu/virtualTryOn/projectData/test/dummy/cloth/00006_00.jpg'
    dummyclothmask = '/home/lintzuh@kean.edu/virtualTryOn/projectData/test/dummy/cloth-mask/00006_00.jpg'
    # If image is not in either directory, copy the dummy image to the target directory
    if not image_in_cloth and not image_in_cloth_mask:
        # Assuming you want to keep the original image name in the target directory
        # target_cloth_path = os.path.join(image_in_cloth, image_name)
        # target_clothmask_path = os.path.join(image_in_cloth_mask, image_name)

        # Copy the dummy image
        try:
            shutil.copy(dummycloth, clothPath)
            shutil.copy(dummyclothmask, clothmaskPaht)

            print(f"Dummy image copied to {clothmaskPaht}")
        except Exception as e:
            print(f"Error copying dummy image: {e}")


@app.route('/virtualTryOn', methods=['POST'])
def virtualTryOn():
    customer_id = request.form['customer_id']
    customer_imageName = request.form['customer_imageName']
    product_id = request.form['product_id']
    product_imageName = request.form['product_image']

    serverCustomerImage = customer_id+'_'+customer_imageName
    fileOutPutRoot = '/home/lintzuh@kean.edu/virtualTryOn/projectData/txtFile'
    print('serverCustomerImage', serverCustomerImage)
    writeTheDataList(serverCustomerImage, product_imageName, fileOutPutRoot)
    dataroot= '/home/lintzuh@kean.edu/virtualTryOn/projectData/test'
    # if cloth and cloth mask no, customImage put dummy image into it
    search_and_replace(serverCustomerImage, dataroot)
    # run the script
    command = [
        'python3', '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/test_generator.py', '--occlusion', '--cuda', 'True', 
        '--test_name', '/home/lintzuh@kean.edu/virtualTryOn/projectData/test/Mytest/test', 
        '--tocg_checkpoint', '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/checkpoints/mtviton.pth', '--gpu_ids', '0', 
        '--gen_checkpoint', '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/checkpoints/gen.pth', '--datasetting', 'unpaired', 
        '--dataroot', '/home/lintzuh@kean.edu/virtualTryOn/projectData', 
        '--data_list', fileOutPutRoot+'/pairs.txt', 
        '--output_dir', '/home/lintzuh@kean.edu/virtualTryOn/projectData/test/Output'
    ]



    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except Exception as e:
        return jsonify({"message": e}), 200





    return jsonify({"message": "tryon success"}), 200



@app.route('/get_parse_agnostic', methods=['POST'])
def get_parse_agnostic():
    request_image_path = request.form['image']
    original_file_name = os.path.basename(request_image_path)
    root='/home/lintzuh@kean.edu/virtualTryOn/projectData/test/'
    image_path = os.path.join(root, 'image',original_file_name)
    tmp_dir_root = '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/HRproject_tmp/'
    tmp_dir = os.path.join(tmp_dir_root, 'image')
    # if not os.path.exists(tmp_dir):
    #     os.makedirs(tmp_dir)

    if os.path.exists(image_path):     
        # shutil.copy(image_path, tmp_dir)
        out_dir = '/home/lintzuh@kean.edu/virtualTryOn/projectData/test/image-parse-agnostic-v3.2' 

        try:
            project_command = [
                'python', '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/get_parse_agnostic.py',  # Python command and script name
                '--data_path', root,                # Input directory argument
                '--output_path',  out_dir # Output directory argument
            ]

            result = subprocess.run(project_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

            remove_files_in_directory(tmp_dir)
        except Exception as e:
            print("An error occurred:", e)


        return jsonify({"message": "get_parse_agnostic success"}), 200


    else:
        return jsonify({"error": "File not found", "image_path": image_path}), 404
    


def remove_files_in_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove the file 




@app.route('/openpose', methods=['POST'])
def openpose_processed():
    request_image_path = request.form['image']
    original_file_name = os.path.basename(request_image_path)
    root='/home/lintzuh@kean.edu/virtualTryOn/projectData/test/'
    image_path = os.path.join(root, 'image',original_file_name)

    if os.path.exists(image_path):
        img_folder = os.path.join(root, 'image')
        out_json = os.path.join(root, 'openpose_json')
        out_img = os.path.join(root, 'openpose_img')
        print(out_json)
        print(out_img)
        openpose_command = [
        '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/openpose/build/examples/openpose/openpose.bin',  # Path to the OpenPose binary
        '--image_dir', img_folder,  # Path to input images
        '--hand',  # Enable hand keypoints detection
        '--disable_blending',  # Disable blending of the keypoints on the original image
        '--display', '0',  # Disable GUI display
        '--write_json',out_json,  # Path to write JSON output
        '--num_gpu', '1',  # Number of GPUs to use
        '--num_gpu_start', '2',  # GPU to start with
        '--write_images', out_img  # Path to write rendered images
        ]
        openposeHome = '/home/lintzuh@kean.edu/virtualTryOn/HR-VITON/openpose'
        try:
            # Assuming 'openpose_command' is already defined as shown in previous examples
            result = subprocess.run(openpose_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,cwd=openposeHome)

            # Print the output and error for debugging
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

            # Check if the command was successful
            if result.returncode != 0:
                print("Error: OpenPose command failed.")
            else:
                print("Success: OpenPose command executed.")

        except Exception as e:
            print("An error occurred:", e)
        return jsonify({"message": "Image processed successfully"}), 200

    else:
        return jsonify({"error": "File not found", "image_path": image_path}), 404
    
if __name__ == '__main__':
     app.run(host=host, port=port)