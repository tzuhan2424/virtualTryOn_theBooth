<?php
echo <<<HTML
<form action="./php/upload.php" method="post" enctype="multipart/form-data">
    Select image to upload:
    <input type="file" name="userImage" id="userImage">
    <input type="submit" value="Upload Image" name="submit">
</form>
HTML;
?>