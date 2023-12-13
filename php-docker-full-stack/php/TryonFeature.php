<?php

$url = 'http://10.100.198.22:5002/virtualTryOn'; // Replace with the actual URL of your Flask app

$customer_id = $_POST['customer_id'];
$customer_image_name = $_POST['customer_image_name'];
$subName = $customer_id.'_'.$customer_image_name;
$target_file = $uploadDir . $subName;

$fields = [
    'customer_id' => $customer_id, // Replace with actual customer id
    'customer_imageName' => $customer_image_name, // Replace with actual image name
    'product_id' => '1', // Replace with actual product id
    'product_image' => '00190_00.jpg', // Replace with actual product image name
];
// The data you want to send via POST


// Use cURL to send the POST request
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($fields));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// Execute the request and fetch the response. Check for errors
$response1 = curl_exec($ch);
if ($response === FALSE) {
    die(curl_error($ch));
}

curl_close($ch);


// $root_dir = "/var/www/shared/test/Output/";
// $customer_image_name = "something.jpg";
// $customer_image_name_without_extension = pathinfo($customer_image_name, PATHINFO_FILENAME);
// $product_image_name_without_extension = pathinfo($product_name, PATHINFO_FILENAME);

// $file = $customer_id.'_'.$customer_image_name_without_extension.'_'.$product_image_name_without_extension.'.png';
// $file = $root_dir.$file;
// if (file_exists($file)) {
//     header('Content-Type: image/png'); 
//     header('Content-Disposition: attachment; filename="'.basename($file).'"');
//     header('Content-Length: ' . filesize($file));
//     readfile($file);
//     exit;
// } else {
//     echo "File not found.";
// }


?>