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
$current_site="staff";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';

// role check
if( A_checkpermission(array(0,2,0,4)) ) {

    // Open database connection
    $Db=S_open_db();

    $errorhtml1 ='';
    $errorhtml2 ='';
    $errorhtml3 ='';
    $errorhtml4 ='';


    // Show staff
    $bool_staff_display=false;
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        
        // Add staff to database
        if(isset($_POST['create_staff'])) {
            $pnr=($_POST['pnr']);
            // check pnr is number
            if( ctype_digit($pnr) ) {
                // check unique pnr
                if( !(S_get_entry($Db,'SELECT id FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);')>0) ) {
                    $u_vname=preg_replace("/'/","´",$_POST['vname']);
                    $u_nname=preg_replace("/'/","´",$_POST['nname']);
                    $u_email=($_POST['email']);
                    $u_lohngruppe=$_POST['lohngruppe'];
                    $u_taetigkeit=$_POST['taetigkeit'];
                    $u_vertrag=$_POST['vertrag'];
                    if($u_vertrag=='') {$u_vertrag=0;}
                    $u_mandant=$_POST['mandant'];
                    $u_abrechnungskreis=$_POST['abrechnungskreis'];
                    if(isset($_POST['hauptamtlich'])) { $u_hauptamtlich=1;} else {$u_hauptamtlich=0;}
                    // check unique email
                    if( !(S_get_entry($Db,'SELECT id FROM li_user WHERE username=\''.$u_email.'\';')>0) ) {
                        // create hash / token (unique)
                        $check_hash=false;
                        do {
                            $u_hash=A_generate_token(8);
                            $check_hash=S_get_entry($Db,'SELECT id FROM Personal WHERE Hash='.$u_hash.';');
                        } while ($check_hash>0);
                        // write data
                        //  create login user
                        if($u_email!='') {
                            S_set_data($Db,'INSERT INTO li_user (username) VALUES (\''.$u_email.'\');');
                            $new_uid=S_get_entry($Db,'SELECT id FROM li_user WHERE lower(username)=\''.$u_email.'\';');
                        } else {
                            $new_uid=0;
                        }
                        //  create staff
                        S_set_data($Db,'INSERT INTO Personal (Vorname, Nachname, Personalnummer, Hash, id_li_user, Taetigkeit, Gruppe, Vertragsnummer, Mandant, Abrechnungskreis,Hauptamtlich) VALUES (
                        \''.$u_vname.'\',
                        \''.$u_nname.'\',
                        CAST('.$pnr.' AS int),
                        \''.$u_hash.'\',
                        '.$new_uid.',
                        \''.$u_taetigkeit.'\',
                        \''.$u_lohngruppe.'\',
                        CAST('.$u_vertrag.' AS int),
                        CAST('.$u_mandant.' AS int),
                        CAST('.$u_abrechnungskreis.' AS int),
                        '.$u_hauptamtlich.');');
                        $errorhtml2 =  H_build_boxinfo( 0, 'Personaldaten wurden erstellt.', 'green' );
                        // Welcome email
                        $res_email=A_send_welcome_email($Db, $u_email);
                        if($res_email) {
                            $errorhtml2 .=  H_build_boxinfo( 0, 'Begrüßungs-E-Mail wurde verschickt.', 'green' );
                        }
                    } else {
                        // Message email exists already
                        $errorhtml2 =  H_build_boxinfo( 0, 'Eingetragene E-Mail-Adresse bereits eingetragen. Es sind keine Dopplungen erlaubt.<br>Sollte die Person bereits einen Login-Zugang haben, bitte den Support kontaktieren.', 'red' );
                    }
                } else {
                    // Message pnr exists already
                    $errorhtml2 =  H_build_boxinfo( 0, 'Eingetragene Personalnummer existiert bereits.', 'red' );
                }
            } else {
                // Message pnr is not number
                $errorhtml2 =  H_build_boxinfo( 0, 'Eingetragene Personalnummer ist keine gültige Nummer.', 'red' );
            }
        }

        // Edit staff in database
        if(isset($_POST['edit_staff'])) {
            $pnr=($_POST['e_pnr']);
            $old_pnr=($_POST['old_pnr']);
            // check pnr is number
            if( ctype_digit($pnr) ) {
                // check unique pnr or same pnr
                if( $pnr==$old_pnr || !(S_get_entry($Db,'SELECT id FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);')>0) ) {
                    $u_vname=preg_replace("/'/","´",$_POST['e_vname']);
                    $u_nname=preg_replace("/'/","´",$_POST['e_nname']);
                    if(isset($_POST['e_active'])) { $u_active=1;} else {$u_active=0;}
                    $u_email=($_POST['e_email']);
                    $u_old_email=($_POST['old_email']);
                    $u_lohngruppe=$_POST['e_lohngruppe'];
                    $u_taetigkeit=$_POST['e_taetigkeit'];
                    $u_vertrag=$_POST['e_vertrag'];
                    $u_mandant=$_POST['e_mandant'];
                    $u_abrechnungskreis=$_POST['e_abrechnungskreis'];
                    if(isset($_POST['e_hauptamtlich'])) { $u_hauptamtlich=1;} else {$u_hauptamtlich=0;}
                    // check unique email or same email
                    if( $u_email==$u_old_email || !(S_get_entry($Db,'SELECT id FROM li_user WHERE username=\''.$u_email.'\';')>0) ) {
                        // write data
                        //  edit login user if changed
                        if( $u_email!=$u_old_email) {
                            // check if link between staff and login_user was set
                            $u_id_li_user=S_get_entry($Db,'SELECT id_li_user FROM Personal WHERE Personalnummer=CAST('.$old_pnr.' AS int);');
                            if($u_id_li_user>0) {
                                if($u_email!='') {
                                    // update email
                                    S_set_data($Db,'UPDATE li_user SET username=\''.$u_email.'\' WHERE id='.$u_id_li_user.';');
                                } else {
                                    // email field is empty
                                    $errorhtml4=  H_build_boxinfo( 0, 'E-Mail-Feld darf nicht leer sein.', 'red' );
                                }
                            } else {
                                // link was not set, add new login_user
                                S_set_data($Db,'INSERT INTO li_user (username) VALUES (\''.$u_email.'\');');
                                $new_uid=S_get_entry($Db,'SELECT id FROM li_user WHERE lower(username)=\''.$u_email.'\';');
                                //  add link to staff
                                S_set_data($Db,'UPDATE Personal SET id_li_user=\''.$new_uid.'\' WHERE Personalnummer=CAST('.$old_pnr.' AS int);');
                            }
                        }
                        //  edit staff data
                        S_set_data($Db,'UPDATE Personal SET Personalnummer=\''.$pnr.'\', Vorname=\''.$u_vname.'\', Nachname=\''.$u_nname.'\', Aktiv='.$u_active.', Gruppe=\''.$u_lohngruppe.'\', Taetigkeit=\''.$u_taetigkeit.'\', Vertragsnummer=CAST('.$u_vertrag.' AS int), Mandant=CAST('.$u_mandant.' AS int), Abrechnungskreis=CAST('.$u_abrechnungskreis.' AS int), Hauptamtlich='.$u_hauptamtlich.' WHERE Personalnummer=CAST('.$old_pnr.' AS int);');
                        if($pnr!=$old_pnr) {
                            S_set_data($Db,'UPDATE Dienste SET Personalnummer=\''.$pnr.'\' WHERE Personalnummer=CAST('.$old_pnr.' AS int);');
                        }
                        $errorhtml3 =  H_build_boxinfo( 0, 'Änderungen wurden gespeichert.', 'green' );
                    } else {
                        // Message email exists already
                        $errorhtml3 =  H_build_boxinfo( 0, 'Eingetragene E-Mail-Adresse bereits eingetragen. Es sind keine Dopplungen erlaubt.<br>Sollte die Person bereits einen Login-Zugang haben, bitte den Support kontaktieren.', 'red' );
                    }
                } else {
                    // Message pnr exists already
                    $errorhtml3=  H_build_boxinfo( 0, 'Eingetragene Personalnummer existiert bereits.', 'red' );
                }
            } else {
                // Message pnr is not number
                $errorhtml3 =  H_build_boxinfo( 0, 'Eingetragene Personalnummer ist keine gültige Nummer.', 'red' );
            }
        }

        // Search on number
        if( isset($_POST['search_staff']) || isset($_POST['search_qr']) || isset($_POST['edit_staff']) || isset($_POST['create_staff']) ) {
            if( isset($_POST['search_staff']) || isset($_POST['edit_staff']) || isset($_POST['create_staff']) ) {
                if( isset($_POST['search_staff']) ) {
                    $pnr=($_POST['pnr']);
                }
                $u_hash=S_get_entry($Db,'SELECT Hash FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                // check if pnr exists
                if( ctype_alnum($u_hash) ) {
                    $bool_staff_display=true;
                    $u_vname=S_get_entry($Db,'SELECT Vorname FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_nname=S_get_entry($Db,'SELECT Nachname FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_taetigkeit=S_get_entry($Db,'SELECT Taetigkeit FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_lohngruppe=S_get_entry($Db,'SELECT Gruppe FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_vertrag=S_get_entry($Db,'SELECT Vertragsnummer FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_mandant=S_get_entry($Db,'SELECT Mandant FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_abrechnungskreis=S_get_entry($Db,'SELECT Abrechnungskreis FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_hauptamtlich=S_get_entry($Db,'SELECT Hauptamtlich FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_id_li_user=S_get_entry($Db,'SELECT id_li_user FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_active=S_get_entry($Db,'SELECT Aktiv FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_email=S_get_entry($Db,'SELECT username FROM li_user WHERE id='.$u_id_li_user.';');
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
                    $u_taetigkeit=S_get_entry($Db,'SELECT Taetigkeit FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_lohngruppe=S_get_entry($Db,'SELECT Gruppe FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_vertrag=S_get_entry($Db,'SELECT Vertragsnummer FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_mandant=S_get_entry($Db,'SELECT Mandant FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_abrechnungskreis=S_get_entry($Db,'SELECT Abrechnungskreis FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_hauptamtlich=S_get_entry($Db,'SELECT Hauptamtlich FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_id_li_user=S_get_entry($Db,'SELECT id_li_user FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_active=S_get_entry($Db,'SELECT Aktiv FROM Personal WHERE Personalnummer=CAST('.$pnr.' AS int);');
                    $u_email=S_get_entry($Db,'SELECT username FROM li_user WHERE id='.$u_id_li_user.';');
                } else {
                    // Message qr code not found
                    $errorhtml1 =  H_build_boxinfo( 0, 'Kein Personal zum QR Code gefunden.', 'red' );
                }
            }
        }

        // report single staff
        if(isset($_POST['get_report_single_staff'])) {
            $pnr=($_POST['pnr']);
            $month=($_POST['month']);
            $year=($_POST['year']);

            $dir=$GLOBALS["SYSPATH_scripts"]."EinzelAbrechnungPDF/";
            chdir($dir);
            $job="python3 job.py $month $year 0 $pnr";
            exec($job,$script_output);
            $file=$script_output[0];
            var_dump($script_output);
            if( file_exists($GLOBALS["SYSPATH_reports"].$file) ) {
                //header('Content-Description: File Transfer');
                header('Content-Type: application/octet-stream');
                header('Content-Disposition: attachment; filename="'.basename($file).'"');
                header('Pragma: no-cache');
                header('Expires: 0');
                //header('Content-Length: ' . filesize($file));
                readfile($GLOBALS["SYSPATH_reports"].$file);
                exit;
            }

            
        }
    }

    // Get staff number and name for select box
    $array_staff=S_get_multientry($Db,'SELECT Id, Personalnummer, Vorname, Nachname, Hash FROM Personal;');
    $array_salary=S_get_multientry($Db,'SELECT Bezeichnung FROM Lohngruppe;');


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
        $('#select-state').selectize({
            sortField: 'text'
        });
    });
    </script>";


    echo '<div class="card"><div class="row">
    <div class="col-lg-3">
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
    echo $errorhtml4;
    echo $errorhtml3;
    echo $errorhtml1;
    echo '</div>';
    // TODO: Extra feature list
    // Search for name and/or number

    if($bool_staff_display) {
        // Show data of staff member
        echo '<div class="col-lg-5">
        <h3>Personal '.$pnr.'</h3>';
        if($u_active==1) {$u_act_selected="checked";} else {$u_act_selected="";}
        if($u_hauptamtlich==1) {$u_hauptamtlich_selected="checked";} else {$u_hauptamtlich_selected="";}
        switch ($u_taetigkeit) {
            case "0":
              $selected[0]="selected"; $selected[1]=""; $selected[2]=""; $selected[3]=""; $selected[4]=""; break;
            case "Medizinisch":
              $selected[1]="selected"; $selected[0]=""; $selected[2]=""; $selected[3]=""; $selected[4]=""; break;
            case "Rettungssanitäter":
              $selected[2]="selected"; $selected[0]=""; $selected[1]=""; $selected[3]=""; $selected[4]=""; break;
            case "Verwaltung":
              $selected[3]="selected"; $selected[0]=""; $selected[1]=""; $selected[2]=""; $selected[4]=""; break;
            case "Sanitätshelfer":
              $selected[4]="selected"; $selected[0]=""; $selected[1]=""; $selected[2]=""; $selected[3]=""; break;
          }

        echo'<form action="'.$current_site.'.php" method="post">
        <div class="input-group">
        <input type="text" value="'.$pnr.'" name="old_pnr" style="display:none;">
        <input type="text" value="'.$u_email.'" name="old_email" style="display:none;">
        <span class="input-group-addon">
        <input type="checkbox" aria-label="MA aktiv" name="e_active" '.$u_act_selected.'>
        <label for="active">MA aktiv</label>
        </span>
        <span class="input-group-addon" id="basic-addon1">Personalnr.</span>
        <input type="text" class="form-control" placeholder="Personalnummer" aria-describedby="basic-addon1" name="e_pnr" autocomplete="off" value="'.$pnr.'">
        <span class="input-group-addon" id="basic-addon1">Vertragsnr.</span>
        <input type="text" class="form-control" placeholder="Vertrag" aria-describedby="basic-addon1" name="e_vertrag" autocomplete="off" value="'.$u_vertrag.'">
        </div><div class="input-group">
        <span class="input-group-addon" id="basic-addon1">Vorname</span>
        <input type="text" class="form-control" placeholder="Vorname" aria-describedby="basic-addon1" name="e_vname" autocomplete="off" value="'.$u_vname.'">
        <span class="input-group-addon" id="basic-addon1">Nachname</span>
        <input type="text" class="form-control" placeholder="Nachname" aria-describedby="basic-addon1" name="e_nname" autocomplete="off" value="'.$u_nname.'">
        </div><div class="input-group">
        <span class="input-group-addon" id="basic-addon1">E-Mail</span>
        <input type="text" class="form-control" placeholder="E-Mail-Adresse" aria-describedby="basic-addon1" name="e_email" autocomplete="off" value="'.$u_email.'">
        </div><div class="input-group">
        <span class="input-group-addon">
        <input type="checkbox" aria-label="Hauptamtlich" name="e_hauptamtlich" '.$u_hauptamtlich_selected.'>
        <label for="Hauptamtlich">Hauptamtlich</label>
        </span>
        <span class="input-group-addon" id="basic-addon6">Tätigkeit</span>
        <select class="custom-select" id="inputGroupSelect01" name="e_taetigkeit" style="margin-top:0px;">
          <option value="0" '.$selected[0].'>n/v</option>
          <option value="Medizinisch" '.$selected[1].'>Medizinisch</option>
          <option value="Rettungssanitäter" '.$selected[2].'>Rettungssanitäter</option>
          <option value="Verwaltung" '.$selected[3].'>Verwaltung</option>
          <option value="Sanitätshelfer" '.$selected[4].'>Sanitätshelfer</option>
        </select>
        <span class="input-group-addon" id="basic-addon6">Lohngruppe</span>
        <select class="custom-select" id="inputGroupSelect02" name="e_lohngruppe" style="margin-top:0px;">';
        // get values from Lohngruppe
        echo '<option value="">n/v</option>';
        foreach($array_salary as $l) {
            if($l[0]==$u_lohngruppe) {$selected="selected";} else {$selected="";}
            echo '<option value="'.$l[0].'" '.$selected.'>'.$l[0].'</option>';
        }
        echo '</select>
        </div><div class="input-group">
        <span class="input-group-addon" id="basic-addon6">Mandant</span>
        <select class="custom-select" id="inputGroupSelect03" name="e_mandant" style="margin-top:0px;">';
        if($u_mandant=='0') {$selected="selected";} else {$selected="";}
        echo '<option value="0" '.$selected.'>n/v</option>';
        if($u_mandant=='800') {$selected="selected";} else {$selected="";}
        echo '<option value="800" '.$selected.'>800</option>';
        if($u_mandant=='801') {$selected="selected";} else {$selected="";}
        echo '<option value="801" '.$selected.'>801</option>';
        echo '</select>
        <span class="input-group-addon" id="basic-addon6">AK</span>
        <select class="custom-select" id="inputGroupSelect04" name="e_abrechnungskreis" style="margin-top:0px;">';
        if($u_abrechnungskreis=='0') {$selected="selected";} else {$selected="";}
        echo '<option value="0" '.$selected.'>n/v</option>';
        if($u_abrechnungskreis=='4') {$selected="selected";} else {$selected="";}
        echo '<option value="4" '.$selected.'>4 (Impfen)</option>';
        if($u_abrechnungskreis=='5') {$selected="selected";} else {$selected="";}
        echo '<option value="5" '.$selected.'>5 (Testen)</option>';
        echo '</select>

        </div>
        <div class="FAIR-si-button">
        <input type="submit" class="btn btn-danger" value="Änderung speichern" name="edit_staff" />
        </div></form>';

        echo '</div>';

        // Show QR code
        echo '<div class="col-lg-2">
        <h3>QR Code</h3>';
        echo '<img src="qrcode.php?id='.$u_hash.'" />';
        echo '</div>';

        // Show report
        $today_month=date("n",time());
        $today_year=date("Y",time());
        echo '<div class="col-lg-2">
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
    if(true) {
        echo '<div class="card"><div class="row">
        <div class="col-sm-12">
        <h3>Neues Personal anlegen</h3>';

        echo'<form action="'.$current_site.'.php" method="post">
        <div class="input-group">
        <span class="input-group-addon" id="basic-addon1">Nr.</span>
        <input type="text" class="form-control" placeholder="Personalnummer" aria-describedby="basic-addon1" name="pnr" autocomplete="off">
        <span class="input-group-addon" id="basic-addon1">Vertragsnr.</span>
        <input type="text" class="form-control" placeholder="Vertrag" aria-describedby="basic-addon1" name="vertrag" autocomplete="off">
        </div><div class="input-group">
        <span class="input-group-addon" id="basic-addon1">Vorname</span>
        <input type="text" class="form-control" placeholder="Vorname" aria-describedby="basic-addon1" name="vname" autocomplete="off">
        </div><div class="input-group">
        <span class="input-group-addon" id="basic-addon1">Nachname</span>
        <input type="text" class="form-control" placeholder="Nachname" aria-describedby="basic-addon1" name="nname" autocomplete="off">
        </div><div class="input-group">
        <span class="input-group-addon" id="basic-addon1">E-Mail</span>
        <input type="text" class="form-control" placeholder="E-Mail-Adresse" aria-describedby="basic-addon1" name="email" autocomplete="off">
        </div><div class="input-group">
        <span class="input-group-addon">
        <input type="checkbox" aria-label="Hauptamtlich" name="hauptamtlich">
        <label for="Hauptamtlich">Hauptamtlich</label>
        </span>
        <span class="input-group-addon" id="basic-addon6">Tätigkeit</span>
        <select class="custom-select" id="inputGroupSelect01n" name="taetigkeit" style="margin-top:0px;">
          <option value="Medizinisch">Medizinisch</option>
          <option value="Rettungssanitäter">Rettungssanitäter</option>
          <option value="Verwaltung">Verwaltung</option>
          <option value="Sanitätshelfer">Sanitätshelfer</option>
        </select>
        <span class="input-group-addon" id="basic-addon6">Lohngruppe</span>
        <select class="custom-select" id="inputGroupSelect02n" name="lohngruppe" style="margin-top:0px;">';
        // get values from Lohngruppe
        //echo '<option value="">n/v</option>';
        foreach($array_salary as $l) {
            echo '<option value="'.$l[0].'">'.$l[0].'</option>';
        }
        echo '</select>
        </div><div class="input-group">
        <span class="input-group-addon" id="basic-addon6">Mandant</span>
        <select class="custom-select" id="inputGroupSelect03n" name="mandant" style="margin-top:0px;">';
        echo '<option value="800">800</option>';
        echo '<option value="801">801</option>';
        echo '</select>
        <span class="input-group-addon" id="basic-addon6">AK</span>
        <select class="custom-select" id="inputGroupSelect04n" name="abrechnungskreis" style="margin-top:0px;">';
        echo '<option value="4">4 (Impfen)</option>';
        echo '<option value="5">5 (Testen)</option>';
        echo '</select>
        </div>
        <div class="FAIR-si-button">
        <input type="submit" class="btn btn-danger" value="Eintragen und anschließend anzeigen" name="create_staff" />
        </div></form>';
        echo $errorhtml2;
        echo '</div></div></div>';
    }

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