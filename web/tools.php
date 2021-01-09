<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

tools

** ************** */

/****************************************/
/* SQL functions */
/****************************************/

// Open DB connection
function S_open_db () {
	/* Database connection information */
	$gaSql=$GLOBALS['gaSql_server'];
	
	echo "<br>connect to ";
	echo "<br>".'"'.$gaSql['server'].'",'.
	'"'.$gaSql['user'].'",'.
	'"'.'",'.
	'"'.$gaSql['db'].'",'.
	''.$gaSql['port'].'';

	// Connect to DB
	$gaSql['link'] = mysqli_connect(
        "'".$gaSql['server']."',".
        "'".$gaSql['user']."',".
		"'".$gaSql['password']."',".
		"'".$gaSql['db']."',".
		"".$gaSql['port']."".
		"" );// or die('Could not connect. Error code: ' . pg_last_error());
echo "<br> TEST";
	if (!$gaSql['link']) {
		echo "Fehler: konnte nicht mit MySQL verbinden." . PHP_EOL;
		echo "Debug-Fehlernummer: " . mysqli_connect_errno() . PHP_EOL;
		echo "Debug-Fehlermeldung: " . mysqli_connect_error() . PHP_EOL;
		exit;
	}

	echo 'Success... ' . mysqli_get_host_info($gaSql['link']) . "\n";

  /*if (!$gaSql['link']) {
	  header('Location: error.php?e=err80');
  }*/
	// Return the database object
	return $gaSql['link'];
}

// Close DB connection
function S_close_db ($Db) {
	mysqli_close($Db);
	return 0;
}


// Return query result from SQL database - first entry only
function S_get_entry ($Db,$sQuery) {
    $rResult = pg_query( $Db, $sQuery ) or die(pg_last_error());
	$r=false;
	while ($row = pg_fetch_row($rResult)) {
		$r=$row[0];
		break;
	}
	
	// Return result of SQL query
	return $r;
}

function S_set_data ($Db,$sQuery) {
    $rResult = pg_query( $Db, $sQuery ) or die(pg_last_error());
	$r=false;
	while ($row = pg_fetch_row($rResult)) {
		$r=$row[0];
	}
	
	// Return result of SQL query
	return $r;
}



/****************************************/
/* Auxilliary functions */
/****************************************/

// Generate random token
function A_generate_token($length = 8) {
		// without 0, O, o
    $characters = '123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ';
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