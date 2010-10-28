<?php
// check to see that the file exists
if ($_GET['action'] == "fileExists") {
    $file = $_SERVER['DOCUMENT_ROOT'] . '/' . $_GET['file'];
    if (file_exists($file) == 1) {
        echo "true";
    } else {
        header("HTTP/1.0 404 Not Found");
    }
}
?>