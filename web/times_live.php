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
$current_site="times_live";
$sec_level=1;

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';

// role check
if( A_checkpermission(array(0,2,0,4)) ) {


  // Print html header
  echo $GLOBALS['G_html_header'];

  // Print html menu
  echo $GLOBALS['G_html_menu'];
  echo $GLOBALS['G_html_menu2'];

  // Print html content part A
  echo $GLOBALS['G_html_main_right_a'];

  $today=date("Y-m-d",time());

  if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // show different date
    if(isset($_POST['show_times'])) {
      $u_date=($_POST['date']);
      $today=$u_date; // for overwriting default search value in box
    } elseif(isset($_POST['show_times_minus1'])){
      $u_date=($_POST['date']);
      $today=date("Y-m-d",strtotime($u_date.' - 1 days'));
    } elseif(isset($_POST['show_times_plus1'])){
      $u_date=($_POST['date']);
      $today=date("Y-m-d",strtotime($u_date.' + 1 days'));
    } elseif(isset($_POST['show_times_today'])){
      
    }
  }


  // Open database connection
  $Db=S_open_db();

  // Get all shifts for today
  if($GLOBALS["SYSMOD_Verrechnung"]) {
    $array_staff=S_get_multientry($Db,'SELECT Dienste.Personalnummer, Personal.Vorname, Personal.Nachname, Dienste.Dienstbeginn, Dienste.Dienstende, Dienste.Art, Dienste.AutoClosed, Dienste.Verrechnung FROM Dienste JOIN Personal ON Personal.Personalnummer=Dienste.Personalnummer WHERE Date(Dienstbeginn)="'.$today.'";');
  } else {
    $array_staff=S_get_multientry($Db,'SELECT Dienste.Personalnummer, Personal.Vorname, Personal.Nachname, Dienste.Dienstbeginn, Dienste.Dienstende, Dienste.Art, Dienste.AutoClosed FROM Dienste JOIN Personal ON Personal.Personalnummer=Dienste.Personalnummer WHERE Date(Dienstbeginn)="'.$today.'";');
  }
  


  echo '<h1>Ansicht Personalbesetzung</h1>';

  // show available Schichtverfügbarkeiten
  echo '<div class="row">';

  echo '<div class="card">
  <div class="col-sm-4">';
  echo '<p></p>';
  echo'<form action="'.$current_site.'.php" method="post">
  <div class="input-group">
  <span class="input-group-addon" id="basic-addonA2">Tag auswählen</span>
  <input type="date" class="form-control" placeholder="Arbeitstag wählen" aria-describedby="basic-addonA2" value="'.$today.'" name="date">
  <span class="input-group-btn">
  <input type="submit" class="btn btn-default" value="- 1 Tag" name="show_times_minus1" />
  <input type="submit" class="btn btn-default" value="Heute" name="show_times_today" />
  <input type="submit" class="btn btn-default" value="+ 1 Tag" name="show_times_plus1" />
  </span>
  </div>
  <div class="FAIR-si-button">
    <input type="submit" class="btn btn-danger" value="Zeiten anzeigen" name="show_times" />
    </div></form>
  </div>';

  echo '
  <div class="col-sm-12">';

  //Get list of times
  foreach($array_staff as $i) {
    if($i[6]==1) {
      // Dienstende AutoClosed
      $dienstende=date("H:i",strtotime($i[4]));
      $class_dienstende='FAIR-change-red';
    } elseif($i[4]==NULL) {
      // Dienstende offen
      $dienstende='';
      $class_dienstende='FAIR-text-red';
    } else {
      $dienstende=date("H:i",strtotime($i[4]));
      $class_dienstende='';
    }
    echo '<form action="times.php" method="post">
    <div class="input-group">
    <span class="input-group-addon" id="basic-addon1">Nr.</span>';
    echo '<input type="text" class="form-control" placeholder="" aria-describedby="basic-addon1" value="'.$i[0].'" disabled>';
    echo '<input type="text" value="'.$today.'" name="date" style="display:none;">';
    echo '<input type="text" value="'.$i[0].'" name="pnr" style="display:none;">';
    echo '<span class="input-group-addon" id="basic-addon2">Name</span>';
    echo '<input type="text" class="form-control" placeholder="" aria-describedby="basic-addon2" value="'.$i[2].', '.$i[1].'" disabled>';
    echo '<span class="input-group-addon" id="basic-addon3">Kommen</span>';
    echo '<input type="time" class="form-control" placeholder="" aria-describedby="basic-addon3" value="'.date("H:i",strtotime($i[3])).'" disabled>';
    echo '<span class="input-group-addon '.$class_dienstende.'" id="basic-addon4">Gehen</span>';
    echo '<input type="time" class="form-control" placeholder="" aria-describedby="basic-addon4" value="'.$dienstende.'" disabled>';
    echo '<span class="input-group-addon" id="basic-addon4">Lohnart</span>';
    echo '<input type="text" class="form-control" placeholder="" aria-describedby="basic-addon4" value="'.$i[5].'" disabled>';
    if($GLOBALS["SYSMOD_Verrechnung"]) {
      echo '<span class="input-group-addon" id="basic-addon5">Verrechnung</span>';
      echo '<input type="text" class="form-control" placeholder="" aria-describedby="basic-addon5" value="'.$i[7].'" disabled>';
    }
    echo'<span class="input-group-btn">
          <input type="submit" class="btn btn-success" value="Ändern" name="search_staff" />
          </span>';
    echo '</div></form>';
  }
  echo '</div></div>';

  echo '</div>';


  // show analytics
  $array_staff=S_get_multientry($Db,'SELECT Stunde, Anzahl FROM Besetzung WHERE Date(Datum)="'.$today.'";');
  $k=0;

  echo "<script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>
  <script type=\"text/javascript\">
      google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Stunde', 'Besetzung'],
          ";
          foreach($array_staff as $i) {
            if($k>0) { echo ","; }
            echo "['".$i[0]." Uhr', ".$i[1]."]";
            $k++;
          }
          if($k==0) {
            echo "['7 Uhr', 0]";
            $k++;
          }
          if($k<16) {
            for($kk=$k;$kk<=(21-7);$kk++) {
              echo ",['".($k+7)." Uhr', 0]";
              $k++;
            }
          }
          echo "
        ]);

        var options = {
          chart: {
            title: 'Besetzung Personal',
            subtitle: 'für den ausgewählten Tag'
          }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }
    </script>
";
echo '<div class="col-sm-12">';
echo '<div id="columnchart_material" style="width: 800px; height: 500px;"></div>';
echo '</div>';

  // Close connection to database
  S_close_db($Db);

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
