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
$current_site="dienstplan_upload";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';

// role check
if( A_checkpermission(array(0,0,3,4)) ) {

    $errorhtml0 ='';

    // Save file from upload
    if (!empty($_FILES)) {
        $uploaddir = '/home/webservice/Dienstplaene/';
        $filename = pathinfo($_FILES['userfile']['name'], PATHINFO_FILENAME);
        $extension = strtolower(pathinfo($_FILES['userfile']['name'], PATHINFO_EXTENSION));
        $week=$_POST['week'];
        $new_file = $uploaddir.'Dienstplan_'.$week.'.'.$extension;

        if (move_uploaded_file($_FILES['userfile']['tmp_name'], $new_file)) {
            $errorhtml0 = H_build_boxinfo( 0, "Datei wurde erfolgreich hochgeladen.", 'green' );
        }

    }

    // Print html header
    echo $GLOBALS['G_html_header'];

    // Print html menu
    echo $GLOBALS['G_html_menu'];
    echo $GLOBALS['G_html_menu2'];

    // Print html content part A
    echo $GLOBALS['G_html_main_right_a'];

    echo '<h1>Dienstplan Dateiverwaltung</h1>';





    echo '<div class="row">';

    echo '<div class="card">
    <div class="col-sm-6">';
    echo '<h3>Verfügbare Dienstpläne</h3>';
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

    // upload file
    // Available weeks
    $today = date('Y-m-d');
    $twoweek_date=date('Y-m-d', strtotime($today. ' + 0 days'));
    $start_date=date('Y-m-d', strtotime('next monday', strtotime($twoweek_date)));
    //build array of next 5 weeks
    $kw_array=array(
        array(date('Y',strtotime($start_date. ' - 14 days')),date('W',strtotime($start_date. ' - 14 days'))),
        array(date('Y',strtotime($start_date. ' - 7 days')),date('W',strtotime($start_date. ' - 7 days'))),
        array(date('Y',strtotime($start_date)),date('W',strtotime($start_date))),
        array(date('Y',strtotime($start_date. ' + 7 days')),date('W',strtotime($start_date. ' + 7 days'))),
        array(date('Y',strtotime($start_date. ' + 14 days')),date('W',strtotime($start_date. ' + 14 days')))
    );


    // upload file
    echo '<p></p><form enctype="multipart/form-data" action="'.$current_site.'.php" method="POST">
    <!-- MAX_FILE_SIZE muss vor dem Dateiupload Input Feld stehen -->
    <input type="hidden" name="MAX_FILE_SIZE" value="30000000" />
    <!-- Der Name des Input Felds bestimmt den Namen im $_FILES Array -->
    Neuen Dienstplan hochladen:<br><input name="userfile" type="file" />
    <select id="select-state" placeholder="Wähle eine Woche" name="week">
    <option value="" selected>Wähle...</option>
        ';
        foreach($kw_array as $i) {
            echo '<option value="'.$i[0].'_kw'.$i[1].'">'.$i[0].' KW'.$i[1].'</option>';
        }
        echo '
    </select>
    <input type="submit" value="Hochladen" />
    </form>';
    echo $errorhtml0;
    echo '</div></div>';

    echo '</div>';

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