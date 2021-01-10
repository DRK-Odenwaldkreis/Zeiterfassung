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


// Menu
$_module_array=array(
    0=>array("text"=>'<h4 class="list-group-item-heading">Zeitkorrektur</h4><p class="list-group-item-text">Zeiten korrigieren oder nachtragen</p>',"link"=>"times.php"),
    1=>array("text"=>'<h4 class="list-group-item-heading">Personaldaten</h4><p class="list-group-item-text">Name und Personalnummer, Personalreport, QR-Code exportieren</p>',"link"=>"staff.php"),
    2=>array("text"=>'<h4 class="list-group-item-heading">Report</h4><p class="list-group-item-text">Monats- und Tagesreport</p>',"link"=>"report.php")
);

echo '<div class="row">';
echo '<div class="col-sm-8">
<h3>Modul wählen</h3>
<div class="list-group">';
foreach($_module_array as $key=>$a) {
    echo '<a class="list-group-item list-group-item-action list-group-item-FAIR" id="module-'.$key.'" href="'.$a["link"].'">'.$a["text"].'</a>';
}
echo '</div></div>';

// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];

?>