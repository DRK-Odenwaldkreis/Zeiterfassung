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

tools

** ************** */

/****************************************/
/* SQL functions */
/****************************************/

// Open DB connection
function S_open_db () {
	/* Database connection information */
	$gaSql=$GLOBALS['gaSql_server'];
	
	// Connect to DB
	$link=mysqli_connect($gaSql['server'],$gaSql['user'],$gaSql['password'],$gaSql['db']);
	if (!$link) {
		echo "<br>Fehler: konnte nicht mit MySQL verbinden.";
		echo "<br>Debug-Fehlernummer: " . mysqli_connect_errno();
		echo "<br>Debug-Fehlermeldung: " . mysqli_connect_error();
		echo "<br>";
		exit;
	}

	if (!$link) {
		header('Location: error.php?e=err80');
	}

	// Return the database object
	return $link;
}

// Close DB connection
function S_close_db ($Db) {
	mysqli_close($Db);
	return 0;
}


// Return query result from SQL database - first entry only
function S_get_entry ($Db,$sQuery) {
	$result = mysqli_query( $Db, $sQuery );
	$r = mysqli_fetch_all($result);

	// Return result of SQL query
	return $r[0][0];
}
// Only for login
function S_get_entry_login_username ($Db,$username) {
	$stmt=mysqli_prepare($Db,"SELECT id FROM li_user WHERE lower(username)=?;");
	mysqli_stmt_bind_param($stmt, "s", $username);
	mysqli_stmt_execute($stmt);
	mysqli_stmt_bind_result($stmt, $id);
	mysqli_stmt_fetch($stmt);
	mysqli_stmt_close($stmt);

	// Return result of SQL query
	return $id;
}
// Return query result from SQL database - all entries
function S_get_multientry ($Db,$sQuery) {
	$result = mysqli_query( $Db, $sQuery );
	$r = mysqli_fetch_all($result);

	// Return result of SQL query
	return $r;
}
// Write data
function S_set_data ($Db,$sQuery) {
    $r = mysqli_query( $Db, $sQuery );
	
	// Return result of SQL query
	return $r;
}

// Returns for single staff in single date all shifts
function S_get_shift_single_date ($Db,$pnr,$date) {
	//get all shifts
	$shifts=S_get_multientry($Db,'SELECT id, Dienstbeginn, Dienstende, Art, AutoClosed FROM Dienste WHERE Personalnummer='.$pnr.' AND Date(Dienstbeginn)="'.$date.'";');
	return $shifts;
}



/****************************************/
/* Auxilliary functions */
/****************************************/

// Generate random token
function A_generate_token($length = 8) {
		// without 0, O, o, z, Z, y, Y
    $characters = '123456789abcdefghijklmnpqrstuvwxABCDEFGHIJKLMNPQRSTUVWX';
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $randomString;
}

// Login for user with $uid
// $mode is for 'password', 'code', ...
function A_login($Db,$uid,$mode) {
    
	$_SESSION['uid'] = $uid;
	if($_SESSION['uid']=='') { die("Error in database. (Err:102)"); }
	
	$_SESSION['signedin'] = true;
	$_SESSION['username'] = S_get_entry($Db,'SELECT username FROM li_user WHERE id='.$uid.';');

	/* Rollen
		1 - Mitarbeiter
		2 - Schichtleiter
		3 - Dienstplaner
		4 - Admin */
	$t = S_get_multientry($Db,'SELECT 0, role_1, role_2, role_3, role_4 FROM li_user WHERE id='.$uid.';');
	$_SESSION['roles']=$t[0];

	if($mode!='check' && $mode!='chguserid') {
		// Cookie will expire after 2 days after log-in
		// PHP session will expire earlier if no site request
		$expiry = time() + 2*24*60*60;
		$data = (object) array( "un" => $_SESSION['username'], "pw" => S_get_entry($Db,'SELECT password_hash FROM li_user WHERE id='.$uid.'') );
		$cookieData = (object) array( "data" => $data, "expiry" => $expiry );
		setcookie('drk-cookie', json_encode( $cookieData ), $expiry);
	}
	
	//login lock reset > set failed attempts to 0
	S_set_data($Db,'UPDATE li_user SET login_attempts=0 WHERE id='.$uid.';');
	
	// Delete older login tokens
	S_set_data($Db,'DELETE FROM li_token WHERE id_user='.$uid.';');

    return true;
}

// Check if user with $uid is already logged in after standard session time is expired
function A_checkloggedin($Db,$username,$hash) {

	// Benutzername und Hash werden überprüft
	if($username!='') {
		$uid=S_get_entry($Db,'SELECT id FROM li_user WHERE lower(username)=\''.$username.'\'');
		if($uid>0) {
			$db_hash=S_get_entry($Db,'SELECT password_hash FROM li_user WHERE id='.$uid.'');
		} else {
			$db_hash='';
		}
		// Check correct password hash
		if ( $hash === $db_hash ) {
			A_login($Db,$uid,'check');
			return true;
		}
	}

    return false;
}

// Check if user role fits to requirements
function A_checkpermission($requirement) {
	$bool_permission=false;
	foreach($requirement as $b) {
		if($b>0 && $_SESSION['roles'][$b]==1) { 
			$bool_permission=true;
		}
	}
return $bool_permission;
}

// send welcome email
function A_send_welcome_email($Db,$to) {
	$FLAG_EMAIL_NEWEMPLOYEE=S_get_entry($Db,'SELECT value FROM website_settings WHERE name="FLAG_EMAIL_NEWEMPLOYEE";');
	if($FLAG_EMAIL_NEWEMPLOYEE==1 && filter_var($to, FILTER_VALIDATE_EMAIL)) {
		// send email
		$header = "From: support@impfzentrum-odw.de\r\n";
		$header .= "Content-Type: text/html; charset=UTF-8\nContent-Transfer-Encoding: 8bit";
		$content=file_get_contents("/home/webservice/Zeiterfassung/utils/MailLayout/NewEmployee.html");
		$title='DRK Impfzentrum Zeiterfassung - Willkommen';
		mail($to, $title, $content, $header, "-r support@impfzentrum-odw.de");

		return true;
	} else {
		return false;
	}
}
// send email with staff roster info
function A_send_staffroster_email($Db,$kw) {
	// get email addresses
	$array_email_staff=S_get_multientry($Db,'SELECT li_user.username FROM Personal JOIN li_user ON Personal.id_li_user=li_user.id WHERE Aktiv=1;');
	$bcc='';
	foreach($array_email_staff as $email) {
		$bcc.=$email[0].',';
	}
	$bcc=substr($bcc, 0, -1);

	// send email
	$header = "From: support@impfzentrum-odw.de\r\n";
	$header .= "Bcc: $bcc\r\n";
	$header .= "Reply-To: dienstplan.impfzentrum@drk-odenwaldkreis.de\r\n";
	$header .= "Content-Type: text/html; charset=UTF-8\nContent-Transfer-Encoding: 8bit";
	$content=file_get_contents("/home/webservice/Zeiterfassung/utils/MailLayout/NewDienstplan.html");
	$content=preg_replace('/\[\[KW]]/',substr($kw,7,2),$content);
    $content=preg_replace('/\[\[YEAR]]/',substr($kw,0,4),$content);
	$title='DRK Impfzentrum Zeiterfassung - Dienstplan '.$kw;
	mail('report@impfzentrum-odw.de', $title, $content, $header, "-r support@impfzentrum-odw.de");
	
	return true;
}



/****************************************/
/* HTML code snippets */
/****************************************/

function H_build_boxhead( $w, $id, $title, $j=0 ) {
	if($w>0) {
		$w_string='width: '.$w.'px;';
		$w_string50='width: '.($w-50).'px;';
		$w_string10='width: '.($w-10).'px;';
	}
	$class_add='';
	$margin_add='';
	$margin_add='margin-right:15px;';
	$html_result = '<div style="float:none; '.$margin_add.'"><div class="FAIR-box-head'.$class_add.'" style="'.$w_string.' position: relative; z-index:'.(50-$j).';">
  <div class="FAIR-foldbox-head-left" style="display: inline; '. $w_string50.'">
  '.$title.'
  </div>
  <div class="FAIR-foldbox-head-right" style="display: inline; width: 50px;">&nbsp;
  </div></div>
  <div class="FAIR-foldbox-static '.$class_add.'" id="'.$id.'" style="display: block; '.$w_string.' position: relative; z-index: '.(49-$j).';">';
	return $html_result;
}
// return html code for info card after foldbox header
function H_build_boxinfo( $w, $text, $c='red' ) {
	if($c=='red') { $class='alert alert-danger'; }
	elseif($c=='blue') { $class='alert alert-info'; }
	elseif($c=='green') { $class='alert alert-success'; }
	else { $class='alert alert-warning'; }
	if($w==0) {
		$html_result = '<div class="'.$class.'" style="top: -5px">';
	} else {
		$html_result = '<div class="'.$class.'" style="width: '. ($w-20) .'px; left: -10px; top: -5px">';
	}
	$html_result .= '<p style="margin-right: 4px;">'.$text.'</p>';
	$html_result .= '</div>';
	return $html_result;
}
// return html code for box style
function H_build_boxheadinner( $w, $id, $title, $j=0 ) {
	$html_result = '<div style="float: none; margin-right:15px;"><div class="FAIR-box-head-inner" style="width: '.$w.'px; position: relative; z-index:'.(50-$j).';">
  <div class="FAIR-foldbox-head-left" style="display: inline; width: '. ($w-50) .'px;">
  '.$title.'
  </div>
  <div class="FAIR-foldbox-head-right" style="display: inline; width: 50px;">
  </div></div>
  <div class="FAIR-foldbox-static-inner" id="'.$id.'" style="display: block; width: '. ($w-10) .'px; position: relative; z-index: '.(49-$j).';">';
	return $html_result;
}

function H_build_boxfoot( ) {
	$html_result = '</div></div>';
	return $html_result;
}

?>