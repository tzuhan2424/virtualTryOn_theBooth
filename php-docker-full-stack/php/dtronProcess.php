<?php
// URL of the dtron Python API
$url = "http://172.18.0.2:5000/";

// Initialize cURL session
$ch = curl_init($url);

// Set cURL options
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, ['data' => 'test data']);

// Execute the POST request
$response = curl_exec($ch);

// Close cURL session
curl_close($ch);

// Print the response from Python API
echo "Response from Python API: " . $response;
?>
