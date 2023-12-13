<?php

header('Access-Control-Allow-Origin: *'); // Allows all origins

include "functions.php";
$a= 'Hello world!';

return_json_success($a);

?>