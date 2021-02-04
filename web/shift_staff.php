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
$current_site="shift_staff";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';



// role check
if( A_checkpermission(array(1,0,3,4)) ) {


    // Open database connection
    $Db=S_open_db();

    $errorhtml1 ='';
    $errorhtml2 ='';
    $errorhtml3 ='';
    $errorhtml4 ='';
    $selected_staff_id=0;

    // role check to get data from all staff members
    if( A_checkpermission(array(0,0,3,4)) ) {
        $array_staff=S_get_multientry($Db,'SELECT Id, Personalnummer, Vorname, Nachname FROM Personal;');
        if( isset($_POST['search_staff']) ) {
            $selected_staff_id=$_POST['selected_staff'];
        } elseif( isset($_POST['save_shifts']) ) {
            $selected_staff_id=$_POST['selected_staff'];
        } else {
            $selected_staff_id=$_GET['selected_staff'];
        }
        if($selected_staff_id==0) {
            // get own staff data
            $staff_id=S_get_entry($Db,'SELECT id FROM Personal WHERE id_li_user='.$_SESSION['uid'].';');
        } else {
            // get staff data from selected person
            $staff_id=$selected_staff_id;
        }
    } else {
        // get own staff data
        $staff_id=S_get_entry($Db,'SELECT id FROM Personal WHERE id_li_user='.$_SESSION['uid'].';');
    }
    $pnr=S_get_entry($Db,'SELECT Personalnummer FROM Personal WHERE id='.$staff_id.';');
    $u_vname=S_get_entry($Db,'SELECT Vorname FROM Personal WHERE id='.$staff_id.';');
    $u_nname=S_get_entry($Db,'SELECT Nachname FROM Personal WHERE id='.$staff_id.';');


    // Get data from form and write to database
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        if( isset($_POST['save_shifts']) ) {
            $selected_year=$_POST['year'];
            $selected_kw=$_POST['kw'];
            
            // 7 days
            for($i=1; $i <= 7; $i++) {
                $date=$_POST['day'.$i];
                // 2 shifts
                for($j=1; $j<=2; $j++) {
                    if(isset($_POST['e_'.$i.$j])) {$shift_value=$j;} else {$shift_value=0;}
                    // entry in DB existing?
                    $shift_in_db=S_get_entry($Db,'SELECT Schicht FROM Planung WHERE Personalnummer=\''.$pnr.'\' AND Datum=\''.$date.'\' AND Schicht='.$j.';');
                    if($shift_value>0) {
                        if( !($shift_in_db>0) ) {
                            // add shift
                            S_set_data($Db,'INSERT INTO Planung (Personalnummer, Datum, Schicht, Comment) VALUES (\''.$pnr.'\', \''.$date.'\', '.$j.', "");');
                            $errorhtml3 =  H_build_boxinfo( 0, 'Änderungen wurden gespeichert.', 'green' );
                        }
                    } elseif($shift_in_db>0) {
                        // remove shift if existing
                        S_set_data($Db,'DELETE FROM Planung WHERE Personalnummer=\''.$pnr.'\' AND Datum=\''.$date.'\' AND Schicht='.$j.';');
                        $errorhtml3 =  H_build_boxinfo( 0, 'Änderungen wurden gespeichert.', 'green' );
                    }
                }
                // comment (3rd shift)
                $shift_value=$_POST['e_'.$i.'3'];
                $shift_value_comment_v=$_POST['e_'.$i.'4v'];
                $shift_value_comment_b=$_POST['e_'.$i.'4b'];
                $shift_value_comment="$shift_value_comment_v - $shift_value_comment_b";
                // entry in DB existing?
                $shift_in_db=S_get_multientry($Db,'SELECT Schicht, Comment FROM Planung WHERE Personalnummer=\''.$pnr.'\' AND Datum=\''.$date.'\' AND Schicht=3;');
                if($shift_value!='') {
                    if( !($shift_in_db[0]>0) ) {
                        // add shift
                        $shift_value_comment = mysqli_real_escape_string($Db, $shift_value_comment);
                        S_set_data($Db,'INSERT INTO Planung (Personalnummer, Datum, Schicht, Comment) VALUES (\''.$pnr.'\', \''.$date.'\', 3, \''.$shift_value_comment.'\');');
                        $errorhtml3 =  H_build_boxinfo( 0, 'Änderungen wurden gespeichert.', 'green' );
                    } elseif($shift_in_db[1]!=$shift_value_comment) {
                        // update comment
                        S_set_data($Db,'UPDATE Planung SET Comment=\''.$shift_value_comment.'\' WHERE Personalnummer=\''.$pnr.'\' AND Datum=\''.$date.'\' AND Schicht=3;');
                        $errorhtml3 =  H_build_boxinfo( 0, 'Änderungen wurden gespeichert.', 'green' );
                    }
                } elseif($shift_in_db[0]>0) {
                    // remove shift if existing
                    S_set_data($Db,'DELETE FROM Planung WHERE Personalnummer=\''.$pnr.'\' AND Datum=\''.$date.'\' AND Schicht=3;');
                    $errorhtml3 =  H_build_boxinfo( 0, 'Änderungen wurden gespeichert.', 'green' );
                } 
            }
        }
    }

    
    // Available weeks
    $today = date('Y-m-d');
    $twoweek_date=date('Y-m-d', strtotime($today. ' + 14 days'));
    $start_date=date('Y-m-d', strtotime('next monday', strtotime($twoweek_date)));
    //build array of next 5 weeks
    $kw_array=array(
        array(date('Y',strtotime($start_date)),date('W',strtotime($start_date))),
        array(date('Y',strtotime($start_date. ' + 7 days')),date('W',strtotime($start_date. ' + 7 days'))),
        array(date('Y',strtotime($start_date. ' + 14 days')),date('W',strtotime($start_date. ' + 14 days'))),
        array(date('Y',strtotime($start_date. ' + 21 days')),date('W',strtotime($start_date. ' + 21 days'))),
        array(date('Y',strtotime($start_date. ' + 28 days')),date('W',strtotime($start_date. ' + 28 days')))
    );

    if ( !isset($selected_year) && $_SERVER['REQUEST_METHOD'] == 'GET') {
        // Get selected week
        if(isset($_GET['year']) && $_GET['year']>0 && isset($_GET['kw']) && $_GET['kw']>0) { 
            $selected_kw=sprintf('%02d', intval($_GET['kw']));
            $selected_year=intval($_GET['year']);
        } else {
            $selected_kw=$kw_array[0][1];
            $selected_year=$kw_array[0][0];
        }
    } elseif(!isset($selected_year)) {
        $selected_kw=$kw_array[0][1];
        $selected_year=$kw_array[0][0];
    }

    // get shifts from database
    $start_date_sql=date('Y-m-d',strtotime($selected_year."W".$selected_kw."1"));
    for($i=1; $i <= 7; $i++) {
        $s[$i][1]=S_get_entry($Db,'SELECT id FROM Planung WHERE Personalnummer='.$pnr.' AND Datum=\''.date('Y-m-d', strtotime($start_date_sql. ' + '.($i-1).' days')).'\' AND Schicht=1;');
        $s[$i][2]=S_get_entry($Db,'SELECT id FROM Planung WHERE Personalnummer='.$pnr.' AND Datum=\''.date('Y-m-d', strtotime($start_date_sql. ' + '.($i-1).' days')).'\' AND Schicht=2;');
        $s[$i][3]=S_get_entry($Db,'SELECT id FROM Planung WHERE Personalnummer='.$pnr.' AND Datum=\''.date('Y-m-d', strtotime($start_date_sql. ' + '.($i-1).' days')).'\' AND Schicht=3;');
        $s[$i][4]=S_get_entry($Db,'SELECT Comment FROM Planung WHERE Personalnummer='.$pnr.' AND Datum=\''.date('Y-m-d', strtotime($start_date_sql. ' + '.($i-1).' days')).'\' AND Schicht=3;');
        if($s[$i][1]>0) {$s_selected[$i][1]="checked";} else {$s_selected[$i][1]="";}
        if($s[$i][2]>0) {$s_selected[$i][2]="checked";} else {$s_selected[$i][2]="";}
        if($s[$i][3]>0) {$s_selected[$i][3]="checked";} else {$s_selected[$i][3]="";}
        $s_selected[$i][4]=substr($s[$i][4],0,5);
        $s_selected[$i][5]=substr($s[$i][4],8,5);
    }


    // Print html header
    echo $GLOBALS['G_html_header'];

    // Print html menu
    echo $GLOBALS['G_html_menu'];
    echo $GLOBALS['G_html_menu2'];

    // Print html content part A
    echo $GLOBALS['G_html_main_right_a'];

    echo '<h1>Schicht-Verfügbarkeiten melden</h1>';

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
    <div class="col-sm-2">';

    // role check to show all staff members
    if( A_checkpermission(array(0,0,3,4)) ) {
        echo'<form action="'.$current_site.'.php" method="post">
        <div class="input-group">
        <span class="input-group-addon" id="basic-addon1">Nr.</span>
        <select id="select-state" placeholder="Wähle eine Person..." name="selected_staff">
        <option value="" selected>Wähle...</option>
            ';
            foreach($array_staff as $i) {
                echo '<option value="'.$i[0].'">'.$i[1].' ('.$i[3].', '.$i[2].')</option>';
            }
            echo '
        </select>
        </div>
        <div class="FAIR-si-button">
        <input type="submit" class="btn btn-danger" value="Person anzeigen" name="search_staff" />
        </div></form>';
        echo '<h4>Ausgewählt:</h4><p><b>'.$u_vname.' '.$u_nname.'</b></p>
    <p>Nr. '.$pnr.'</p>';
    } else {
        echo '<p><b>'.$u_vname.' '.$u_nname.'</b></p>
        <p>Nr. '.$pnr.'</p>';
    }

    
    

    echo '<h3>Woche wählen</h3>';

    
    // print kw selection
    foreach($kw_array as $kw) {
        echo '<a class="list-group-item list-group-item-action list-group-item-FAIR" id="module-'.$kw[1].'" href="'.$current_site.'.php?kw='.$kw[1].'&year='.$kw[0].'&selected_staff='.$selected_staff_id.'">KW '.$kw[1].'</a>';
    }
    echo '<p>&nbsp;</p><p>Die oberste Kalenderwoche wird am Sonntag um Mitternacht geschlossen. Ab Montag steht dann eine neue Kalenderwoche zum Eintragen zur Verfügung.</p>';
    echo '</div>';

    

    echo '<div class="col-sm-10">
    <h3>KW '.$selected_kw.' in '.$selected_year.'</h3>';
    

    echo'<form action="'.$current_site.'.php" method="post">
    <input type="text" value="'.$selected_year.'" name="year" style="display:none;">
    <input type="text" value="'.$selected_kw.'" name="kw" style="display:none;">
    <input type="text" value="'.$selected_staff_id.'" name="selected_staff" style="display:none;">
    <table class="FAIR-data">
    <tr>
    <td class="FAIR-data-height1 FAIR-data-bottom">
    </td><td class="FAIR-data-height1 FAIR-data-bottom">
    Schichtwunsch<br><span style="font-size:75%;">(Beide = ich kann den ganzen Tag)</span>
    </td><td class="FAIR-data-height1 FAIR-data-bottom" colspan="2">
    Alternative Angabe<br><span style="font-size:75%;">mit Uhrzeit von xx:xx bis xx:xx</span>
    </td>
    </tr>
    ';
    $de_array=array('Mon','Die','Mit','Don','Fre','Sam','Son');

    // print rows for each day
    for($i=1; $i <= 7; $i++) {

        echo '<tr>
        <input type="text" value="'.date('Y-m-d',strtotime($selected_year."W".$selected_kw.$i)).'" name="day'.$i.'" style="display:none;">
        <td class="FAIR-data-height1 FAIR-data-bottom">
        '.$de_array[$i-1].', '.date('d.m.y',strtotime($selected_year."W".$selected_kw.$i)).'
        </td><td class="FAIR-data-height1 FAIR-data-bottom">
        <input type="checkbox" id="e_'.$i.'1" name="e_'.$i.'1" value="1" '.$s_selected[$i][1].'/>
        <label for="e_'.$i.'1">Früh</label>
        <input type="checkbox" id="e_'.$i.'2" name="e_'.$i.'2" value="2" '.$s_selected[$i][2].'/>
        <label for="e_'.$i.'2">Spät</label>
        </td><td class="FAIR-data-height1 FAIR-data-bottom">
        <input type="checkbox" id="e_'.$i.'3" name="e_'.$i.'3" value="3" '.$s_selected[$i][3].'/>
        <label for="e_'.$i.'3">Alternativ</label>
        </td><td class="FAIR-data-height1 FAIR-data-bottom">
        <div class="input-group">
        <span class="input-group-addon" id="e_'.$i.'4_label">von</span>
        <input type="time" id="e_'.$i.'4v" name="e_'.$i.'4v" class="form-control" autocomplete="off" value="'.$s_selected[$i][4].'"   />
        <span class="input-group-addon" id="e_'.$i.'4_label">bis</span>
        <input type="time" id="e_'.$i.'4b" name="e_'.$i.'4b" class="form-control" autocomplete="off" value="'.$s_selected[$i][5].'"   />
        </div>
        </td>
        </tr>';
    }

    
    echo'
    <tr>
    <td class="FAIR-data-height1 FAIR-data-bottom">
    </td><td class="FAIR-data-height1 FAIR-data-bottom">
    <span style="font-size:75%;">Früh von 07:00 bis 14:30<br>Spät von 14:30 bis 22:00</span>
    </td><td class="FAIR-data-height1 FAIR-data-bottom" colspan="2">
    </td>
    </tr>
    </table>

    <div class="FAIR-si-button">
    <input type="submit" class="btn btn-danger" value="Speichern" name="save_shifts" />
    </div></form>';

    echo $errorhtml3;

    echo '</div>';
    

    echo '</div></div>';

    // Dienstplan download
    echo '<h3>Download verfügbarer Dienstpläne</h3>';
    echo '<div class="card"><div class="row">
    <div class="col-sm-12">';
    echo '<p>Vom Dienstplaner bereitgestellte Dienstpläne für eine Kalenderwoche:
    </p>';
    //Get list of files
    // Available weeks
    $today = date('Y-m-d');
    $twoweek_date=date('Y-m-d', strtotime($today. ' + 0 days'));
    $start_date=date('Y-m-d', strtotime('next monday', strtotime($twoweek_date)));
    //build array of next 5 weeks
    $kw_array=array(
        array(date('Y',strtotime($start_date. ' - 14 days')),date('W',strtotime($start_date. ' - 14 days')),date('d.m.Y',strtotime($start_date. ' - 14 days'))),
        array(date('Y',strtotime($start_date. ' - 7 days')),date('W',strtotime($start_date. ' - 7 days')),date('d.m.Y',strtotime($start_date. ' - 7 days'))),
        array(date('Y',strtotime($start_date)),date('W',strtotime($start_date)),date('d.m.Y',strtotime($start_date))),
        array(date('Y',strtotime($start_date. ' + 7 days')),date('W',strtotime($start_date. ' + 7 days')),date('d.m.Y',strtotime($start_date. ' + 7 days'))),
        array(date('Y',strtotime($start_date. ' + 14 days')),date('W',strtotime($start_date. ' + 14 days')),date('d.m.Y',strtotime($start_date. ' + 14 days')))
    );
    $log_path="/home/webservice/Dienstplaene/";
    $array_files=scandir($log_path);
    foreach($kw_array as $i) {
        $a='Dienstplan_'.$i[0].'_kw'.$i[1].'.pdf';
        if(file_exists($log_path.$a)) {
            echo '<a class="list-group-item list-group-item-action list-group-item-redtext" href="https://impfzentrum-odw.de/download.php?dir=d&file='.$a.'">KW '.$i[1].' gültig ab '.$i[2].'<span class="FAIR-sep-l"></span><span class="FAIR-text-med">(Erstellt: '.date ("d.m.Y H:i", filemtime($log_path.$a)).')</a>';
        }
    }

    echo '</div>';
    echo '</div></div>';

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

// Close connection to database
S_close_db($Db);
?>