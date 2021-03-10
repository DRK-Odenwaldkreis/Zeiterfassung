<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

# This file is part of DRK Zeiterfassung.

# DRK Zeiterfassung is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# DRK Zeiterfassung is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DRK Zeiterfassung.  If not, see <http://www.gnu.org/licenses/>.

** ************** */

include_once 'preload.php';
if( isset($GLOBALS['G_sessionname']) ) { session_name ($GLOBALS['G_sessionname']); }
session_start();
$sec_level=1;
$current_site="report";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';

// role check
if( A_checkpermission(array(0,2,0,4)) ) {

    $errorhtml0 ='';
    $errorhtml1 ='';

    // Create report
    $val_report_display=0;
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {

        if(isset($_POST['get_report_all_staff_csv'])) {
            $month=($_POST['month']);
            $year=($_POST['year']);
            $uid=$_SESSION['uid'];

            $dir="/home/webservice/Zeiterfassung/CSVExport/";
            chdir($dir);

            // direct download
            /* $job="python3 job.py $month $year";
            exec($job,$script_output);
            $file=$script_output[0];
            if( file_exists("/home/webservice/Reports/$file") ) {
                header('Content-Type: application/octet-stream');
                header('Content-Disposition: attachment; filename="'.basename($file).'"');
                header('Pragma: no-cache');
                header('Expires: 0');
                readfile("/home/webservice/Reports/$file");
                exit;
            } */

            // create file and send email
            $job="python3 job.py $month $year $uid > /dev/null &";
            exec($job,$script_output);
            $errorhtml1 = H_build_boxinfo( 0, "Report wird erstellt und Downloadlink an Ihre E-Mail verschickt. Dies kann einen Augenblick dauern.", 'green' );
            
        } elseif(isset($_POST['get_report_all_staff'])) {
            $month=($_POST['month']);
            $year=($_POST['year']);
            $uid=$_SESSION['uid'];

            $dir="/home/webservice/Zeiterfassung/EinzelAbrechnungPDF/";
            chdir($dir);
            $job="python3 job.py $month $year $uid > /dev/null &";
            exec($job,$script_output);
            $errorhtml0 = H_build_boxinfo( 0, "Report wird erstellt und Downloadlink an Ihre E-Mail verschickt. Dies kann einen Augenblick dauern.", 'green' );
            
        } elseif(isset($_POST['get_report_single_date'])) {
            $date=($_POST['date']);
            
            $dir="/home/webservice/Zeiterfassung/TagesReportPDF/";
            chdir($dir);
            $job="python3 job.py '$date'";
            exec($job,$script_output);
            $file=$script_output[0];
            if( file_exists("/home/webservice/Reports/$file") ) {
                header('Content-Type: application/octet-stream');
                header('Content-Disposition: attachment; filename="'.basename($file).'"');
                header('Pragma: no-cache');
                header('Expires: 0');
                readfile("/home/webservice/Reports/$file");
                exit;
            }
        }
    }

    // Print html header
    echo $GLOBALS['G_html_header'];

    // Print html menu
    echo $GLOBALS['G_html_menu'];
    echo $GLOBALS['G_html_menu2'];

    // Print html content part A
    echo $GLOBALS['G_html_main_right_a'];

    echo '<h1>Report</h1>';



    $today_month=date("n",time());
    $today_year=date("Y",time());
    $today=date("Y-m-d",time());

    echo '<div class="row">';

    echo '<div class="card">
    <div class="col-sm-6">
    <h3>Monatsreport PDF</h3>
    <p class="list-group-item-text">Report mit allen MA. Pro MA neue Seite.</p>
    <p class="list-group-item-text">Zum Erstellen hier Monat auswählen. E-Mail-Benachrichtigung sobald zum Download verfügbar</p><p></p>';
    echo '<form action="'.$current_site.'.php" method="post">
        <div class="input-group">
        <span class="input-group-addon" id="basic-addon4">Monat</span>
        <input type="number" min="1" max="12" class="form-control" placeholder="Monat" aria-describedby="basic-addon4" value="'.$today_month.'" name="month" value=>
        <span class="input-group-addon" id="basic-addon5">Jahr</span>
        <input type="number" min="2021" max="2999" class="form-control" placeholder="Jahr" aria-describedby="basic-addon5" value="'.$today_year.'" name="year">
        <span class="input-group-btn">
        <input type="submit" class="btn btn-danger" value="PDF-Report erstellen" name="get_report_all_staff" />
        </span>
        </div>
        </form>';
        echo $errorhtml0;
    echo '</div></div>';

    echo '<div class="card">
    <div class="col-sm-6">
    <h3>Monatsreport CSV</h3>
    <p class="list-group-item-text">CSV zum Einlesen in weitere Datenverarbeitung.</p>
    <p class="list-group-item-text">Zum Erstellen hier Monat auswählen. Download wird gestartet.</p><p></p>';
    echo '<form action="'.$current_site.'.php" method="post">
        <div class="input-group">
        <span class="input-group-addon" id="basic-addon4">Monat</span>
        <input type="number" min="1" max="12" class="form-control" placeholder="Monat" aria-describedby="basic-addon4" value="'.$today_month.'" name="month" value=>
        <span class="input-group-addon" id="basic-addon5">Jahr</span>
        <input type="number" min="2021" max="2999" class="form-control" placeholder="Jahr" aria-describedby="basic-addon5" value="'.$today_year.'" name="year">
        <span class="input-group-btn">
        <input type="submit" class="btn btn-danger" value="CSV-Report abrufen" name="get_report_all_staff_csv" />
        </span>
        </div>
        </form>';
        echo $errorhtml1;
    echo '</div></div>';

    echo '<div class="card">
    <div class="col-sm-6">
    <h3>Tagesreport PDF</h3>
    <p class="list-group-item-text">Einzelner Tag mit allen MA.</p>
    <p class="list-group-item-text">Zum Erstellen hier Datum auswählen. Download wird gestartet.</p><p></p>';
    echo '<form action="'.$current_site.'.php" method="post">
        <div class="input-group">
        <span class="input-group-addon" id="basic-addon4">Arbeitstag</span>
        <input type="date" class="form-control" placeholder="JJJJ-MM-DD" aria-describedby="basic-addon4" value="'.$today.'" name="date" value=>
        <span class="input-group-btn">
        <input type="submit" class="btn btn-danger" value="PDF-Report abrufen" name="get_report_single_date" />
        </span>
        </div>
        </form>';
    echo '</div></div>';

    echo '<div class="card">
    <div class="col-sm-6">
    <h3>Einzel-Personalreport PDF</h3>
    <p class="list-group-item-text">Muss über Personaldaten geöffnet werden</p>';
    echo '<p></p><a href="staff.php" class="btn btn-danger">Zu den Personaldaten</a><p></p>';
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