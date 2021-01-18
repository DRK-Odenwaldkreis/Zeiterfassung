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
$current_site="log";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';


// Print html header
echo $GLOBALS['G_html_header'];

// Print html menu
echo $GLOBALS['G_html_menu'];
echo $GLOBALS['G_html_menu2'];

// Print html content part A
echo $GLOBALS['G_html_main_right_a'];

echo '<h1>Logs</h1>';

echo '<pre>UID: '.$_SESSION['uid'].'</pre>';


// tail of $file with last $int lines
function file_tail($file,$int) {
    $file_content=file($file);
    $r="";
    for ($i = max(0, count($file_content)-$int-1); $i < count($file_content); $i++) {
         $r .= $file_content[$i] . "";
    }
    return $r;
}

//Get log file
$log_path="/home/webservice/Logs/";
echo '<h3>reportJob.log</h3>';
echo '<pre>';
echo file_tail($log_path."reportJob.log",40);
echo '</pre>';
echo '<h3>CSVExportJob.log</h3>';
echo '<pre>';
echo file_tail($log_path."CSVExportJob.log",40);
echo '</pre>';
echo '<h3>singleReportJob.log</h3>';
echo '<pre>';
echo file_tail($log_path."singleReportJob.log",40);
echo '</pre>';


// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];

?>