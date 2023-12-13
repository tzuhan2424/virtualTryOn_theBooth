<?php
// Define the path to the shared directory
$shared_dir = "/var/www/shared/";

// Replace 'image.jpg' with the name of the image file you want to display
$file_name = "image.jpg";

// Construct the full path to the image file
$file_path = $shared_dir . $file_name;

// Check if the image file exists
if (file_exists($file_path)) {
    // Set the appropriate content type based on the file's extension
    $file_extension = strtolower(pathinfo($file_path, PATHINFO_EXTENSION));
    switch ($file_extension) {
        case 'jpg':
        case 'jpeg':
            header('Content-Type: image/jpeg');
            break;
        case 'png':
            header('Content-Type: image/png');
            break;
        // Add more cases for other file types as needed
        default:
            header('Content-Type: application/octet-stream');
    }

    // Output the file content
    readfile($file_path);
    exit;
}
?> 


<!DOCTYPE html>
<html>
<head>
    <title>Show Image</title>
</head>
<body>
    <h1>Image Not Found</h1>
    <p>The requested image was not found.</p>
</body>
</html>