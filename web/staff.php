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

// Show staff
$bool_staff_display=false;
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Search on number
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
echo '<div class="card"><div class="row">
<div class="col-sm-3">
<h3>Personal wählen</h3>';

echo'<form action="'.$current_site.'.php" method="post">
<div class="input-group">
  <span class="input-group-addon" id="basic-addon1">Nr.</span>
  <input type="text" class="form-control" placeholder="Personalnummer" aria-describedby="basic-addon1" name="pnr">
</div>
<div class="FAIR-si-button">
<input type="submit" class="btn btn-danger" value="Suchen" name="search_staff" />
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
    echo '<form action="report.php" method="post">
    <div class="input-group">
      <input type="text" value="'.$pnr.'" name="pnr" style="display:none;">
      <span class="input-group-addon" id="basic-addon4">Monat</span>
      <input type="number" min="1" max="12" class="form-control" placeholder="Monat" aria-describedby="basic-addon4" value="'.$today_month.'" name="month" value=>
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
  <input type="text" class="form-control" placeholder="Personalnummer" aria-describedby="basic-addon1" name="pnr">
  <span class="input-group-addon" id="basic-addon1">Vorname</span>
  <input type="text" class="form-control" placeholder="Vorname" aria-describedby="basic-addon1" name="vname">
  <span class="input-group-addon" id="basic-addon1">Nachname</span>
  <input type="text" class="form-control" placeholder="Nachname" aria-describedby="basic-addon1" name="nname">
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