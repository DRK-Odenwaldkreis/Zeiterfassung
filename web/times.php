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

$errorhtml0 ='';
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
            // Get shifts for selected date
            $u_shifts=S_get_shift_single_date($Db,$pnr,$u_date);
        } else {
            // Message pnr not found
            $errorhtml1 =  H_build_boxinfo( 0, 'Personalnummer nicht gefunden.', 'red' );
        }
    } elseif(isset($_POST['submit_times'])) {
      // Zeiten nachtragen
      $pnr=$_POST['pnr'];
      $u_date=$_POST['date'];
      $today=$u_date; // for overwriting default search value in box
      $u_shift_start=$_POST['start_time'];
      $u_shift_end=$_POST['end_time'];
      $u_shift_type=$_POST['lohnart'];
      // Make sql timestamps
      $u_s_start=$u_date.' '.$u_shift_start.':00';
      $u_s_end=$u_date.' '.$u_shift_end.':00';
      $res=S_set_data($Db,'INSERT INTO Dienste (Personalnummer,Dienstbeginn,Dienstende,Art) VALUES (CAST('.$pnr.' AS int),\''.$u_s_start.'\',\''.$u_s_end.'\',\''.$u_shift_type.'\');');
      if(!$res){
        $errorhtml0 = H_build_boxinfo( 0, "Fehler beim Eintragen - ungültige Werte", 'red' );
      } else {
        $errorhtml0 = H_build_boxinfo( 0, "Zeiten eingetragen von $u_s_start bis $u_s_end mit Lohnart $u_shift_type", 'green' );
      }
    } elseif(isset($_POST['save_times'])) {
      // Zeiten korrigieren
      $id=$_POST['id'];
      $pnr=$_POST['pnr'];
      $u_date=$_POST['date'];
      $today=$u_date; // for overwriting default search value in box
      $u_shift_start=$_POST['start_time'];
      $u_shift_end=$_POST['end_time'];
      $u_shift_type=$_POST['lohnart'];
      // Make sql timestamps
      $u_s_start=$u_date.' '.$u_shift_start.':00';
      $u_s_end=$u_date.' '.$u_shift_end.':00';
      $res=S_set_data($Db,'UPDATE Dienste SET Dienstbeginn=\''.$u_s_start.'\', Dienstende=\''.$u_s_end.'\', Art=\''.$u_shift_type.'\' WHERE id=CAST('.$id.' AS int);');
      if(!$res){
        $errorhtml0 = H_build_boxinfo( 0, "Fehler beim Eintragen - ungültige Werte", 'red' );
      } else {
        $errorhtml0 = H_build_boxinfo( 0, "Zeiten eingetragen von $u_s_start bis $u_s_end mit Lohnart $u_shift_type", 'green' );
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
  <span class="input-group-addon" id="basic-addonA1">Nr.</span>
  <input type="text" class="form-control" placeholder="Personalnummer" aria-describedby="basic-addonA1" name="pnr" value="'.$pnr.'">
  <span class="input-group-addon" id="basic-addonA2">Tag</span>
  <input type="date" class="form-control" placeholder="Arbeitstag wählen" aria-describedby="basic-addonA2" value="'.$today.'" name="date">
</div>
<div class="FAIR-si-button">
<input type="submit" class="btn btn-danger" value="Suchen" name="search_staff" />
</div></form>';
echo $errorhtml0;
echo $errorhtml1;
echo '</div>';
// TODO: Extra feature list
// Search for name and/or number

if($bool_staff_display) {
// Show shifts and correct it
  echo '<div class="col-sm-6">';

  // Zeiten nachtragen
  if(!$u_shifts) {
    echo '<h3>Zeiten nachtragen</h3>';
    echo '<form action="'.$current_site.'.php" method="post">
    <div class="input-group">
      <span class="input-group-addon" id="basic-addon1">Nr.</span>
      <input type="text" class="form-control" placeholder="" aria-describedby="basic-addon1" value="'.$pnr.'" disabled>
      <span class="input-group-addon" id="basic-addon2">Tag</span>
      <input type="date" class="form-control" placeholder="" aria-describedby="basic-addon2" value="'.$u_date.'" disabled>
      <span class="input-group-addon" id="basic-addon3">Name</span>
      <input type="text" class="form-control" placeholder="" aria-describedby="basic-addon3" value="'.$u_nname.', '.$u_vname.'" disabled>
    </div>
    <div class="input-group">
      <input type="text" value="'.$pnr.'" name="pnr" style="display:none;">
      <input type="text" value="'.$u_date.'" name="date" style="display:none;">
      <span class="input-group-addon" id="basic-addon4">Kommen</span>
      <input type="time" class="form-control" placeholder="Kommenzeit" aria-describedby="basic-addon4" name="start_time">
      <span class="input-group-addon" id="basic-addon5">Gehen</span>
      <input type="time" class="form-control" placeholder="Gehenzeit" aria-describedby="basic-addon5" name="end_time">
      
      <span class="input-group-addon" id="basic-addon6">Lohnart</span>
      <select class="custom-select" id="inputGroupSelect01" name="lohnart">
        <option value="Normal" selected>Normal</option>
        <option value="Krank">Krank</option>
        <option value="Urlaub">Urlaub</option>
      </select>

      <span class="input-group-btn">
      <input type="submit" class="btn btn-danger" value="Eintragen" name="submit_times" />
      </span>
    </div></form>';

  } else {
  // Zeiten korrigieren
    echo '<h3>Zeiten korrigieren</h3>';
    echo '<form>
    <div class="input-group">
      <span class="input-group-addon" id="basic-addon1">Nr.</span>
      <input type="text" class="form-control" placeholder="" aria-describedby="basic-addon1" value="'.$pnr.'" disabled>
      <span class="input-group-addon" id="basic-addon2">Tag</span>
      <input type="date" class="form-control" placeholder="" aria-describedby="basic-addon2" value="'.$u_date.'" disabled>
      <span class="input-group-addon" id="basic-addon3">Name</span>
      <input type="text" class="form-control" placeholder="" aria-describedby="basic-addon3" value="'.$u_nname.', '.$u_vname.'" disabled>
    </div></form>';

    foreach($u_shifts as $i) {
      switch ($i[3]) {
        case "Normal":
          $selected[0]="selected"; $selected[1]=""; $selected[2]=""; break;
        case "Krank":
          $selected[1]="selected"; $selected[0]=""; $selected[2]=""; break;
        case "Urlaub":
          $selected[2]="selected"; $selected[1]=""; $selected[1]=""; break;
      }
      
      echo'<form action="'.$current_site.'.php" method="post">
      <div class="input-group">
        <input type="text" value="'.$i[0].'" name="id" style="display:none;">
        <input type="text" value="'.$u_date.'" name="date" style="display:none;">
        <input type="text" value="'.$pnr.'" name="pnr" style="display:none;">
        <span class="input-group-addon" id="basic-addon1-'.$i[0].'">Kommen</span>
        <input type="time" class="form-control" placeholder="Kommenzeit" aria-describedby="basic-addon1-'.$i[0].'" value="'.date("H:i",strtotime($i[1])).'" name="start_time">
        <span class="input-group-addon" id="basic-addon2-'.$i[0].'">Gehen</span>
        <input type="text" value="'.$i[2].'" style="display:none;">
        <input type="time" class="form-control" placeholder="Gehenzeit" aria-describedby="basic-addon2-'.$i[0].'" value="'.date("H:i",strtotime($i[2])).'" name="end_time">
        
        <span class="input-group-addon" id="basic-addon3-'.$i[0].'">Lohnart</span>
        <select class="custom-select" id="inputGroupSelect01" name="lohnart">
          <option value="Normal" '.$selected[0].'>Normal</option>
          <option value="Krank" '.$selected[1].'>Krank</option>
          <option value="Urlaub" '.$selected[2].'>Urlaub</option>
        </select>

        <span class="input-group-btn">
        <input type="submit" class="btn btn-danger" value="Speichern" name="save_times" />
        </span>
      </div></form>';
    }
  }
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