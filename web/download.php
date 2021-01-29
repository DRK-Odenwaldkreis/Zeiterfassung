<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

** ************** */

include_once 'preload.php';
if( isset($GLOBALS['G_sessionname']) ) { session_name ($GLOBALS['G_sessionname']); }
session_start();
$sec_level=1;
$current_site="download";

// Include functions
include_once 'tools.php';
include_once 'auth.php';

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $file=($_GET['file']);
    if(isset($_GET['dir'])) { $dir_id=$_GET['dir']; } else {$dir_id=0;}
    switch($dir_id) {
        case "r":
            $dir="Reports";
            break;
        case "d":
            $dir="Dienstplaene";
            break;
        case "p":
            $dir="Planung";
            break;
        default:
            $dir="Reports";   
    }
    
    if( file_exists("/home/webservice/$dir/$file") ) {
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="'.basename($file).'"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($file));
        readfile("/home/webservice/$dir/$file");
        exit;
    }
}
?>