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
$current_site="staff";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';



// Open database connection
$Db=S_open_db();

$errorhtml1 ='';
$errorhtml2 ='';

// Get staff number and name for select box
$array_staff=S_get_multientry($Db,'SELECT Id, Personalnummer, Vorname, Nachname, Hash FROM Personal;');

// Show staff
$bool_staff_display=false;
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Search on number
	if(isset($_POST['search_staff']) || isset($_POST['search_qr'])) {
        if(isset($_POST['search_staff'])) {
            $pnr=($_POST['pnr']);
            $u_hash=S_get_entry($Db,'SELECT Hash FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
            // check if pnr exists
            if( ctype_alnum($u_hash) ) {
                $bool_staff_display=true;
                $u_vname=S_get_entry($Db,'SELECT Vorname FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                $u_nname=S_get_entry($Db,'SELECT Nachname FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
            } else {
                // Message pnr not found
                $errorhtml1 =  H_build_boxinfo( 0, 'Personalnummer nicht gefunden.', 'red' );
            }
        } else {
            $u_hash=($_POST['qrcode']);
            $pnr=S_get_entry($Db,'SELECT Personalnummer FROM Personal WHERE Hash="'.$u_hash.'";');
            // check if qr code exists
            if( $pnr>0 ) {
                $bool_staff_display=true;
                $u_vname=S_get_entry($Db,'SELECT Vorname FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                $u_nname=S_get_entry($Db,'SELECT Nachname FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
            } else {
                // Message qr code not found
                $errorhtml1 =  H_build_boxinfo( 0, 'Kein Personal zum QR Code gefunden.', 'red' );
            }
        }
        
        
    }
    // Add staff to database
	if(isset($_POST['create_staff'])) {
        $pnr=($_POST['pnr']);
        // check pnr is number
        if( ctype_digit($pnr) ) {
            // check unique pnr
            if( !(S_get_entry($Db,'SELECT id FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);')>0) ) {
                $u_vname=($_POST['vname']);
                $u_nname=($_POST['nname']);
                // create hash / token (unique)
                $check_hash=false;
                do {
                    $u_hash=A_generate_token(8);
                    $check_hash=S_get_entry($Db,'SELECT id FROM Personal WHERE Hash='.$u_hash.';');
                } while ($check_hash>0);
                // write data
                S_set_data($Db,'INSERT INTO Personal (Vorname,Nachname,Personalnummer,Hash) VALUES (\''.$u_vname.'\',\''.$u_nname.'\',CAST('.$pnr.' AS int),\''.$u_hash.'\');');
            } else {
                // Message pnr exists already
                $errorhtml2 =  H_build_boxinfo( 0, 'Eingetragene Personalnummer existiert bereits.', 'red' );
            }
        } else {
            // Message pnr is not number
            $errorhtml2 =  H_build_boxinfo( 0, 'Eingetragene Personalnummer ist keine gültige Nummer.', 'red' );
        }
    }

    // report single staff
	if(isset($_POST['get_report_single_staff'])) {
        $pnr=($_POST['pnr']);
        $month=($_POST['month']);
        $year=($_POST['year']);

        $dir="/home/webservice/Zeiterfassung/EinzelAbrechnungPDF/";
        chdir($dir);
        $job="python3 job.py $month $year 0 $pnr";
        exec($job,$script_output);
        $file=$script_output[0];
        var_dump($script_output);
        if( file_exists("/home/webservice/Reports/$file") ) {
            header('Content-Description: File Transfer');
            header('Content-Type: application/octet-stream');
            header('Content-Disposition: attachment; filename="'.basename($file).'"');
            header('Expires: 0');
            header('Cache-Control: must-revalidate');
            header('Pragma: public');
            header('Content-Length: ' . filesize($file));
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

echo '<h1>Personaldaten</h1>';
//
// Select staff
//
echo '
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.6/js/standalone/selectize.min.js" integrity="sha256-+C0A5Ilqmu4QcSPxrlGpaZxJ04VjsRjKu+G82kl5UJk=" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.6/css/selectize.bootstrap3.min.css" integrity="sha256-ze/OEYGcFbPRmvCnrSeKbRTtjG4vGLHXgOqsyLFTRjg=" crossorigin="anonymous" />';

echo "<script>
$(document).ready(function () {
    $('select').selectize({
        sortField: 'text'
    });
});
</script>";


echo '<div class="card"><div class="row">
<div class="col-sm-3">
<h3>Personal wählen</h3>';

echo'<form action="'.$current_site.'.php" method="post">
<div class="input-group">
  <span class="input-group-addon" id="basic-addon1">Nr.</span>
  <select id="select-state" placeholder="Wähle eine Person..." name="pnr">
  <option value="" selected>Wähle...</option>
    ';
    foreach($array_staff as $i) {
        echo '<option value="'.$i[1].'">'.$i[1].' ('.$i[3].', '.$i[2].')</option>';
    }
    echo '
  </select>
</div>
<div class="FAIR-si-button">
<input type="submit" class="btn btn-danger" value="Anzeigen" name="search_staff" />
</div></form>';
echo'<h3>Alternative mit Scannen</h3>
<form action="'.$current_site.'.php" method="post">
<div class="input-group">
  <span class="input-group-addon" id="basic-addon11">QR Code</span>
  <input type="text" class="form-control" placeholder="scannen..." aria-describedby="basic-addon11" value="" name="qrcode" autocomplete="off">
</div>
<div class="FAIR-si-button">
<input type="submit" class="btn btn-danger" value="Anzeigen" name="search_qr" />
</div></form>';
echo $errorhtml1;
echo '</div>';
// TODO: Extra feature list
// Search for name and/or number

if($bool_staff_display) {
    // Show data
    echo '<div class="col-sm-3">
    <h3>Personal '.$pnr.'</h3>';

    echo '<p>Name: '.$u_nname.', '.$u_vname.'</p>';

    echo '</div>';

    // Show QR code
    echo '<div class="col-sm-3">
    <h3>QR Code</h3>';
    echo '<img src="qrcode.php?id='.$u_hash.'" />';
    echo '</div>';

    // Show report
    $today_month=date("n",time());
    $today_year=date("Y",time());
    echo '<div class="col-sm-2">
    <h3>Report</h3>';
    echo '<form action="'.$current_site.'.php" method="post">
    <div class="input-group">
      <input type="text" value="'.$pnr.'" name="pnr" style="display:none;">
      <span class="input-group-addon" id="basic-addon4">Monat</span>
      <input type="number" min="1" max="12" class="form-control" placeholder="Monat" aria-describedby="basic-addon4" value="'.$today_month.'" name="month">
      </div><div class="input-group">
      <span class="input-group-addon" id="basic-addon5">Jahr</span>
      <input type="number" min="2021" max="2999" class="form-control" placeholder="Jahr" aria-describedby="basic-addon5" value="'.$today_year.'" name="year">
    </div>
    <input type="submit" class="btn btn-danger" value="PDF-Report abrufen" name="get_report_single_staff" />
    </form>';
    
    echo '</div>';
}

echo '</div></div>';

//
// Add staff
//
echo '<div class="card"><div class="row">
<div class="col-sm-12">
<h3>Neues Personal anlegen</h3>';

echo'<form action="'.$current_site.'.php" method="post">
<div class="input-group">
  <span class="input-group-addon" id="basic-addon1">Nr.</span>
  <input type="text" class="form-control" placeholder="Personalnummer" aria-describedby="basic-addon1" name="pnr" autocomplete="off">
  <span class="input-group-addon" id="basic-addon1">Vorname</span>
  <input type="text" class="form-control" placeholder="Vorname" aria-describedby="basic-addon1" name="vname" autocomplete="off">
  <span class="input-group-addon" id="basic-addon1">Nachname</span>
  <input type="text" class="form-control" placeholder="Nachname" aria-describedby="basic-addon1" name="nname" autocomplete="off">
</div>
<div class="FAIR-si-button">
<input type="submit" class="btn btn-danger" value="Eintragen und anschließend anzeigen" name="create_staff" />
</div></form>';
echo $errorhtml2;
echo '</div></div></div>';


// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];

// Close connection to database
S_close_db($Db);
?>