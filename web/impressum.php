<!doctype html>

<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

imprint site

** ************** */


include_once 'preload.php';
if( isset($GLOBALS['G_sessionname']) ) { session_name ($GLOBALS['G_sessionname']); }
session_start();
$current_site="impressum";
$sec_level=0;


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


if(isset( $_SESSION['uid']) && $_SESSION['uid']>=0 ) {
    echo '<h3>Support</h3>
    <p>Bei Fragen zum System bitte eine E-Mail schreiben an den Support.</p>
    <p>email@example.com</p>';
}


echo '<h3>Impressum</h3>
<a href="https://drk-odenwaldkreis.de/impressum/">Direkt beim DRK Kreisverband Odenwaldkreis e. V.</a>';




// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];






?>