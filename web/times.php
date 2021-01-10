<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

** ************** */

include_once 'preload.php';
if( isset($GLOBALS['G_sessionname']) ) { session_name ($GLOBALS['G_sessionname']); }
session_start();
$current_site="times";
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

$today=date("Y-m-d",time());
$pnr="";

$errorhtml1 ='';
$bool_staff_display=false;

// Open database connection
$Db=S_open_db();

// Show staff
$bool_staff_display=false;
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Search on number
    if(isset($_POST['search_staff'])) {
        $pnr=($_POST['pnr']);
        $u_date=($_POST['date']);
        $today=$u_date; // for overwriting default search value in box
        $u_id=S_get_entry($Db,'SELECT id FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
        // check if pnr exists
        if( ctype_digit($u_id) ) {
            $bool_staff_display=true;
            $u_vname=S_get_entry($Db,'SELECT Vorname FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
            $u_nname=S_get_entry($Db,'SELECT Nachname FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
        } else {
            // Message pnr not found
            $errorhtml1 =  H_build_boxinfo( 0, 'Personalnummer nicht gefunden.', 'red' );
        }
    }
}

//
// Select staff
//
echo '<div class="card"><div class="row">
<div class="col-sm-6">
<h3>Mitarbeiter*in wählen</h3>';

echo'<form action="'.$current_site.'.php" method="post">
<div class="input-group">
  <span class="input-group-addon" id="basic-addon1">Nr.</span>
  <input type="text" class="form-control" placeholder="Personalnummer" aria-describedby="basic-addon1" name="pnr" value="'.$pnr.'">
  <span class="input-group-addon" id="basic-addon1">Tag</span>
  <input type="date" class="form-control" placeholder="Arbeitstag wählen" aria-describedby="basic-addon1" value="'.$today.'" name="date">
</div>
<div class="FAIR-si-button">
<input type="submit" class="btn btn-danger" value="Suchen" name="search_staff" />
</div></form>';
echo $errorhtml1;
echo '</div>';
// TODO: Extra feature list
// Search for name and/or number

if($bool_staff_display) {
// Show clocking and correct it
  echo '<div class="col-sm-6">
  <h3>Zeiten korrigieren/nachtragen</h3>';

  echo'<form action="'.$current_site.'.php" method="post">
  <div class="input-group">
    <span class="input-group-addon" id="basic-addon1">Nr.</span>
    <input type="text" class="form-control" placeholder="" aria-describedby="basic-addon1" value="'.$pnr.'" disabled>
    <span class="input-group-addon" id="basic-addon1">Tag</span>
    <input type="date" class="form-control" placeholder="" aria-describedby="basic-addon1" value="'.$u_date.'" disabled>
    <span class="input-group-addon" id="basic-addon1">Name</span>
    <input type="text" class="form-control" placeholder="" aria-describedby="basic-addon1" value="'.$u_nname.', '.$u_vname.'" disabled>
  </div>
  <div class="input-group">
    <span class="input-group-addon" id="basic-addon1">Kommen</span>
    <input type="time" class="form-control" placeholder="Kommenzeit" aria-describedby="basic-addon1">
    <span class="input-group-addon" id="basic-addon1">Gehen</span>
    <input type="time" class="form-control" placeholder="Gehenzeit" aria-describedby="basic-addon1">
    
    <span class="input-group-addon" id="basic-addon1">Lohnart</span>
    <select class="custom-select" id="inputGroupSelect01">
      <option selected>Wähle...</option>
      <option value="1">Normal</option>
      <option value="2">Krank</option>
      <option value="3">Urlaub</option>
    </select>
  </div>
  <div class="FAIR-si-button">
  <input type="submit" class="btn btn-danger" value="Eintragen" name="submit_times" />
  </div></form>';
  echo '</div>';
}
echo '</div></div>';


// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];
// Close connection to database
S_close_db($Db);
?>