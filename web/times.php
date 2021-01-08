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

$today=date("Y-m-d",time());

echo '<div class="row">';
// Select staff
echo '<div class="col-sm-6">
<h3>Mitarbeiter*in wählen</h3>';

echo'<form action="'.$current_site.'.php" method="post">
<div class="input-group">
  <span class="input-group-addon" id="basic-addon1">Nr.</span>
  <input type="text" class="form-control" placeholder="Personalnummer" aria-describedby="basic-addon1">
  <span class="input-group-addon" id="basic-addon1">Tag</span>
  <input type="date" class="form-control" placeholder="Arbeitstag wählen" aria-describedby="basic-addon1" value="'.$today.'">
</div>
<div class="FAIR-si-button">
<input type="submit" class="btn btn-danger" value="Suchen" name="search_staff" />
</div></form>';
echo '</div>';
// TODO: Extra feature list
// Search for name and/or number

// Show clocking and correct it
echo '<div class="col-sm-6">
<h3>Zeiten korrigieren/nachtragen</h3>';

echo'<form action="'.$current_site.'.php" method="post">
<div class="input-group">
  <span class="input-group-addon" id="basic-addon1">Nr.</span>
  <input type="text" class="form-control" placeholder="" aria-describedby="basic-addon1" disabled>
  <span class="input-group-addon" id="basic-addon1">Tag</span>
  <input type="date" class="form-control" placeholder="" aria-describedby="basic-addon1" disabled>
  <span class="input-group-addon" id="basic-addon1">Name</span>
  <input type="text" class="form-control" placeholder="" aria-describedby="basic-addon1" disabled>
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


// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];

?>