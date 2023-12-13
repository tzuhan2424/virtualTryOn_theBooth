<?php
    include "functions.php";


    $target_dir = "/var/www/shared/test/image/";


    // Check if a file has been uploaded
    if (isset($_FILES['file'])) {
        // Define the path to the upload folder
        $uploadDir = $target_dir;

        $customer_id = $_POST['customer_id'];
        $customer_image_name = $_POST['customer_image_name'];
        $subName = $customer_id.'_'.$customer_image_name;
        $target_file = $uploadDir . $subName;

        // $target_file = $uploadDir . basename($_FILES['file']['name']);


        // Move the file to the upload directory
        if (move_uploaded_file($_FILES['file']['tmp_name'], $target_file)) {
            // dtron
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://172.20.0.3:5000/process"); // Adjust the URL/port
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, ['image' => $target_file]); // this is you send the post method
            $response = curl_exec($ch);
            curl_close($ch);

            // openpose
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://10.100.198.22:5002/openpose"); // Adjust the URL/port

            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, ['image' => $target_file]); // this is you send the post method
            $response = curl_exec($ch);
            curl_close($ch);


            if ($response !== false) {
                echo "Server response: " . $response;
            } else {
                echo "Error contacting processing service";
            }

        //     // pgn_process
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://10.100.198.22:5003/pgn_process"); // Adjust the URL/port
    
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, ['image' => $target_file]); // this is you send the post method
            $response = curl_exec($ch);
            curl_close($ch);
    
    
            if ($response !== false) {
                echo "Server response: " . $response;
            } else {
                echo "Error contacting processing service";
            }

        //     //agnostic
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://10.100.198.22:5002/get_parse_agnostic"); // Adjust the URL/port

            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, ['image' => $target_file]); // this is you send the post method
            $response = curl_exec($ch);
            curl_close($ch);


            if ($response !== false) {
                echo "Server response: " . $response;
            } else {
                echo "Error contacting processing service";
            }

    


        //     // echo "File is successfully received and stored.";
        // } else {
        //     echo "There was an error uploading the file.";
        // }
        } else {
            echo "No file was uploaded.";
        }
    }




?>