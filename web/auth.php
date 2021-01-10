<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

authentication frame

** ************** */

// Security level for elements in use if logged in
if( !isset($sec_level) ) { $sec_level=1; }

if( $sec_level==0 && isset($_SESSION['uid']) && $_SESSION['uid']>=0 ) { $sec_level=1; }


$FLAG_http='http';

$hostname = $_SERVER['HTTP_HOST'];
$path = dirname($_SERVER['PHP_SELF']);

include_once('val/admin01.php');
include_once('server_settings.php');
include_once('tools.php');
 
$linked_URL=$_SERVER['REQUEST_URI'];

if( $sec_level>0 ) {
	// Case: shutdown active -> go to login site
	if ($FLAG_SHUTDOWN=='true' ) {
		session_destroy();
		header('Location: '.$FLAG_http.'://'.$hostname.($path == '/' ? '' : $path).'/login.php');
	exit;
	}


	// Case: not logged in / PHP session expired
	if ( (!isset($_SESSION['signedin']) || !$_SESSION['signedin']) ) {
		// Check if user is logged in with special cookie
		$cookievalue=json_decode($_COOKIE['drk-cookie']);
		$username=$cookievalue->data->un;
		$hash=$cookievalue->data->pw;

		// Open database connection
		$Db=S_open_db();
		
		// Cookie of session is expired - check for remembered logged in status
		// PHP session will expire earlier
		if( !A_checkloggedin($Db,$username,$hash) ) {
			// Is referer url not a login site
			if( !preg_match('/login/',$linked_URL) ) {
				$_SESSION['linkURL'] = $linked_URL;
			}
			header('Location: '.$FLAG_http.'://'.$hostname.($path == '/' ? '' : $path).'/login.php');
			exit;
		}
		
		// Close connection to database
		S_close_db($Db);
	} else {
		$username = $_SESSION['username'];
	}
}
$html_usermenubar='';


?>