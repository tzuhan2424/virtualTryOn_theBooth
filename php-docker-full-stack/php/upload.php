<?php


    $target_dir = "/var/www/shared/test/image/";
    //$_FILES["userImage"]["name"] will give you the original filename of the file that the user uploaded.
    $target_file = $target_dir . basename($_FILES["userImage"]["name"]);


    // echo $target_file;


    if (move_uploaded_file($_FILES["userImage"]["tmp_name"], $target_file)) {
        echo "The file ". htmlspecialchars(basename($_FILES["userImage"]["name"])). " has been uploaded.";

        // Notify Python service (Detectron2) for processing - Adjust URL as necessary
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "http://172.20.0.3:5000/process"); // Adjust the URL/port
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, ['image' => $target_file]); // this is you send the post method
        $response = curl_exec($ch);
        curl_close($ch);


        if ($response !== false) {
            echo "Server response detron2: " . $response;
        } else {
            echo "Error contacting processing service";
        }

        // Notify Python service (Detectron2) for processing - Adjust URL as necessary
        $ch = curl_init();
        // curl_setopt($ch, CURLOPT_URL, "http://172.0.0.1:5002/openpose"); // Adjust the URL/port
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




        





        


    
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
?>
