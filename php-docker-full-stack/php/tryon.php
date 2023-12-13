<?php

include "functions.php";
$url = 'http://10.100.198.22:5002/virtualTryOn'; // Replace with the actual URL of your Flask app

$customer_id = $_POST['customer_id'];
$customer_image_name = $_POST['customer_image'];
$product_id = $_POST['product_id'];
$product_name =  $_POST['product_image'];

$fields = [
    'customer_id' => $customer_id,
    'customer_imageName' => $customer_image_name,
    'product_id' => $product_id,
    'product_image' => $product_name,
];

// Use cURL to send the POST request
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($fields));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response1 = curl_exec($ch);
if ($response1 === FALSE) {
    die(curl_error($ch));
}

curl_close($ch);
ob_start(); // Start output buffering

$root_dir = "/var/www/shared/test/Output/";
$customer_image_name_without_extension = pathinfo($customer_image_name, PATHINFO_FILENAME);
$product_image_name_without_extension = pathinfo($product_name, PATHINFO_FILENAME);

$file = $root_dir.$customer_id.'_'.$customer_image_name_without_extension.'_'.$product_image_name_without_extension.'.png';

if (file_exists($file)) {
    ob_clean(); // Clean (erase) the output buffer and turn off output buffering

    header('Access-Control-Allow-Origin: *'); // Allows all origins
    header('Content-Type: image/png'); 
    // header('Content-Disposition: attachment; filename="'.basename($file).'"');
    // header('Content-Length: ' . filesize($file));
    readfile($file);
    exit;
} else {
    header('Content-Type: text/plain'); // Make sure to change the content type
    echo "File not found.";
    exit;
}

?>
