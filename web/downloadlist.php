<!-- # This file is part of DRK Zeiterfassung.

# DRK Zeiterfassung is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# DRK Zeiterfassung is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DRK Zeiterfassung.  If not, see <http://www.gnu.org/licenses/>. -->


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
$current_site="downloadlist";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';

// role check
if( A_checkpermission(array(0,0,0,4)) ) {


    // Print html header
    echo $GLOBALS['G_html_header'];

    // Print html menu
    echo $GLOBALS['G_html_menu'];
    echo $GLOBALS['G_html_menu2'];

    // Print html content part A
    echo $GLOBALS['G_html_main_right_a'];

    echo '<h1>Files</h1>';

    echo '<h3>Reports/</h3>';
    echo '<p>';
    //Get list of files
    $log_path="/home/webservice/Reports/";
    $array_files=scandir($log_path);
    foreach($array_files as $a) {
        if( preg_match('/.pdf/',$a) || preg_match('/.zip/',$a) ) {
            echo '<a href="https://impfzentrum-odw.de/download.php?dir=r&file='.$a.'">'.$a.'</a><br>';
        }
        
    }
    echo '</p>';

    echo '<h3>Dienstplaene/</h3>';
    echo '<p>';
    //Get list of files
    $log_path="/home/webservice/Dienstplaene/";
    $array_files=scandir($log_path);
    foreach($array_files as $a) {
        if( preg_match('/.pdf/',$a) || preg_match('/.zip/',$a) ) {
            echo '<a href="https://impfzentrum-odw.de/download.php?dir=d&file='.$a.'">'.$a.'</a><br>';
        }
        
    }
    echo '</p>';

    echo '<h3>Planung/</h3>';
    echo '<p>';
    //Get list of files
    $log_path="/home/webservice/Planung/";
    $array_files=scandir($log_path);
    foreach($array_files as $a) {
        if( preg_match('/.pdf/',$a) || preg_match('/.zip/',$a) ) {
            echo '<a href="https://impfzentrum-odw.de/download.php?dir=p&file='.$a.'">'.$a.'</a><br>';
        }
        
    }
    echo '</p>';

} else {
    // Print html header
    echo $GLOBALS['G_html_header'];

    // Print html menu
    echo $GLOBALS['G_html_menu'];
    echo $GLOBALS['G_html_menu2'];

    // Print html content part A
    echo $GLOBALS['G_html_main_right_a'];
    echo '<h1>KEINE BERECHTIGUNG</h1>';
}

// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];

?>