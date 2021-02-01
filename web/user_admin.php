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
$current_site="user_admin";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';

// role check
if( A_checkpermission(array(0,0,0,4)) ) {


    // Open database connection
    $Db=S_open_db();

    $errorhtml1 ='';
    $errorhtml2 ='';
    $errorhtml3 ='';
    $errorhtml4 ='';


    // Show user
    $bool_staff_display=false;
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {

        // Edit user in database
        if(isset($_POST['edit_staff'])) {
            $user_id=($_POST['user_id']);
            $old_email=($_POST['old_email']);
            $email=($_POST['e_email']);

            // check unique email or same email
            if( $email==$old_email || !(S_get_entry($Db,'SELECT id FROM li_user WHERE username=\''.$email.'\';')>0) ) {

                $attempts=$_POST['e_attempts'];
                if(isset($_POST['e_r1'])) { $u_role_1=1;} else {$u_role_1=0;}
                if(isset($_POST['e_r2'])) { $u_role_2=1;} else {$u_role_2=0;}
                if(isset($_POST['e_r3'])) { $u_role_3=1;} else {$u_role_3=0;}
                if(isset($_POST['e_r4'])) { $u_role_4=1;} else {$u_role_4=0;}

                // write data
                if($email!='') {
                    // update email
                    S_set_data($Db,'UPDATE li_user SET username=\''.$email.'\' WHERE id='.$user_id.';');
                } else {
                    // email field is empty
                    $errorhtml4=  H_build_boxinfo( 0, 'E-Mail-Feld darf nicht leer sein.', 'red' );
                }

                //  edit staff data
                S_set_data($Db,'UPDATE li_user SET login_attempts=CAST('.$attempts.' AS int), role_1='.$u_role_1.', role_2='.$u_role_2.', role_3='.$u_role_3.', role_4='.$u_role_4.'  WHERE id='.$user_id.';');
                $errorhtml3 =  H_build_boxinfo( 0, 'Änderungen wurden gespeichert.', 'green' );
                
            } else {
                // Message email exists already
                $errorhtml3 =  H_build_boxinfo( 0, 'Eingetragene E-Mail-Adresse bereits eingetragen. Es sind keine Dopplungen erlaubt.<br>Sollte die Person bereits einen Login-Zugang haben, bitte den Support kontaktieren.', 'red' );
            }

        }

        // Search on number
        if( isset($_POST['search_staff']) || isset($_POST['edit_staff']) || isset($_POST['create_staff']) ) {
            if( isset($_POST['search_staff']) ) {
                $user_id=($_POST['user_id']);
            }
            $bool_staff_display=true;
            $u_email=S_get_entry($Db,'SELECT username FROM li_user WHERE id=CAST('.$user_id.' AS int);');
            $u_nname=S_get_entry($Db,'SELECT Personal.Nachname FROM Personal JOIN li_user ON Personal.id_li_user=li_user.id WHERE li_user.id=CAST('.$user_id.' AS int);');
            $u_vname=S_get_entry($Db,'SELECT Personal.Vorname FROM Personal JOIN li_user ON Personal.id_li_user=li_user.id WHERE li_user.id=CAST('.$user_id.' AS int);');
            $u_attempts=S_get_entry($Db,'SELECT login_attempts FROM li_user WHERE id=CAST('.$user_id.' AS int);');
            $u_role_1=S_get_entry($Db,'SELECT role_1 FROM li_user WHERE id=CAST('.$user_id.' AS int);');
            $u_role_2=S_get_entry($Db,'SELECT role_2 FROM li_user WHERE id=CAST('.$user_id.' AS int);');
            $u_role_3=S_get_entry($Db,'SELECT role_3 FROM li_user WHERE id=CAST('.$user_id.' AS int);');
            $u_role_4=S_get_entry($Db,'SELECT role_4 FROM li_user WHERE id=CAST('.$user_id.' AS int);');
            if($u_nname!='') {
                $u_display=$u_nname.', '.$u_vname;
            } else {
                $u_display='(nicht mit Mitarbeiter*in verknüpft)';
            }
        }

        // save settings for web app
        if( isset($_POST['save_settings']) ) {
            if(isset($_POST['s_1'])) {
                S_set_data($Db,'UPDATE website_settings SET value=1 WHERE name="FLAG_EMAIL_NEWEMPLOYEE";');
            } else {
                S_set_data($Db,'UPDATE website_settings SET value=0 WHERE name="FLAG_EMAIL_NEWEMPLOYEE";');
            }
        }
    }

    // Get user details
    $array_staff=S_get_multientry($Db,'SELECT li_user.Id, li_user.username, Personal.Nachname, Personal.Vorname FROM li_user LEFT OUTER JOIN Personal ON Personal.id_li_user=li_user.id;');

    // Print html header
    echo $GLOBALS['G_html_header'];

    // Print html menu
    echo $GLOBALS['G_html_menu'];
    echo $GLOBALS['G_html_menu2'];

    // Print html content part A
    echo $GLOBALS['G_html_main_right_a'];

    echo '<h1>Admin: User-Management</h1>';
    //
    // Select user
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
    <div class="col-sm-4">
    <h3>Personal wählen</h3>';

    echo'<form action="'.$current_site.'.php" method="post">
    <div class="input-group">
    <span class="input-group-addon" id="basic-addon1">Nr.</span>
    <select id="select-state" placeholder="Wähle eine Person..." name="user_id">
    <option value="" selected>Wähle...</option>
        ';
        foreach($array_staff as $i) {
            if($i[2]!='') {
                $display=$i[2].', '.$i[3].' ('.$i[1].')';
            } else {
                $display=$i[1];
            }
            echo '<option value="'.$i[0].'">'.$display.'</option>';
        }
        echo '
    </select>
    </div>
    <div class="FAIR-si-button">
    <input type="submit" class="btn btn-danger" value="Anzeigen" name="search_staff" />
    </div></form>';
    echo $errorhtml4;
    echo $errorhtml3;
    echo $errorhtml1;
    echo '</div>';
    // TODO: Extra feature list
    // Search for name and/or number

    if($bool_staff_display) {
        // Show data of staff member
        echo '<div class="col-sm-8">
        <h3>User '.$user_id.'</h3>
        <p>'.$u_display.'</p>';
        if($u_role_1==1) {$u_role_1_selected="checked";} else {$u_role_1_selected="";}
        if($u_role_2==1) {$u_role_2_selected="checked";} else {$u_role_2_selected="";}
        if($u_role_3==1) {$u_role_3_selected="checked";} else {$u_role_3_selected="";}
        if($u_role_4==1) {$u_role_4_selected="checked";} else {$u_role_4_selected="";}

        echo'<form action="'.$current_site.'.php" method="post">
        <div class="input-group">
        <input type="text" value="'.$user_id.'" name="user_id" style="display:none;">
        <input type="text" value="'.$u_email.'" name="old_email" style="display:none;">
        <span class="input-group-addon" id="basic-addon1">E-Mail</span>
        <input type="text" class="form-control" placeholder="E-Mail-Adresse" aria-describedby="basic-addon1" name="e_email" autocomplete="off" value="'.$u_email.'">
        <span class="input-group-addon" id="basic-addon1">Login-Versuche</span>
        <input type="text" class="form-control" placeholder="Login-Versuche" aria-describedby="basic-addon2" name="e_attempts" autocomplete="off" value="'.$u_attempts.'">
        </div><div class="input-group">
        <span class="input-group-addon">
        <input type="checkbox" aria-label="r1" name="e_r1" '.$u_role_1_selected.'>
        <label for="e_r1">Rolle MA</label><span style="padding-left:10px;"></span>
        <input type="checkbox" aria-label="r2" name="e_r2" '.$u_role_2_selected.'>
        <label for="e_r2">Rolle Schichtleiter</label><span style="padding-left:10px;"></span>
        <input type="checkbox" aria-label="r3" name="e_r3" '.$u_role_3_selected.'>
        <label for="e_r3">Rolle Dienstplaner</label><span style="padding-left:10px;"></span>
        <input type="checkbox" aria-label="r4" name="e_r4" '.$u_role_4_selected.'>
        <label for="e_r4">Rolle Admin</label><span style="padding-left:10px;"></span>
        </span>
        </div>
        <div class="FAIR-si-button">
        <input type="submit" class="btn btn-danger" value="Änderung speichern" name="edit_staff" />
        </div></form>';

        echo '</div>';
    }

    echo '</div></div>';




    // Checks for website administration
    echo '<div class="card"><div class="row">
    <div class="col-sm-4">
    <h3>Set values</h3>';
    $FLAG_EMAIL_NEWEMPLOYEE=S_get_entry($Db,'SELECT value FROM website_settings WHERE name="FLAG_EMAIL_NEWEMPLOYEE";');
    if($FLAG_EMAIL_NEWEMPLOYEE==1) {
        $s_selected['FLAG_EMAIL_NEWEMPLOYEE']='checked';
    } else {
        $s_selected['FLAG_EMAIL_NEWEMPLOYEE']='';
    }

    echo'<form action="'.$current_site.'.php" method="post">

    <input type="checkbox" id="s_1" name="s_1" value="s1" '.$s_selected['FLAG_EMAIL_NEWEMPLOYEE'].'/>
    <label for="s_1">Welcome email</label><br>
    
    <div class="FAIR-si-button">
    <input type="submit" class="btn btn-danger" value="Speichern" name="save_settings" />
    </div></form>';
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

// Close connection to database
S_close_db($Db);
?>