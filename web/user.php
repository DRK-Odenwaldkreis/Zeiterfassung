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
ini_set('error_reporting', E_ALL ^ E_NOTICE);
ini_set('display_errors', ON);

$sec_level=1;
// Include functions
include 'tools.php';
include_once 'auth.php';

$current_site="user";

// Include secondary files
include 'menu.php';
 
$hostname = $_SERVER['HTTP_HOST'];
$path = dirname($_SERVER['PHP_SELF']);

$refererURL=$_SERVER['HTTP_REFERER'];
$refererPATH=parse_url($refererURL, PHP_URL_PATH);
$refererARG=parse_url($refererURL, PHP_URL_QUERY);


// m is for mode
if( isset($_GET['m']) ) { $mode=$_GET['m']; } else { $mode=''; }

// Open database connection
$Db=S_open_db();


$uid=$_SESSION['uid'];
$username=$_SESSION['username'];


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	// Change password
	if( isset($_POST['button-change']) ) {
		$mode='chgpwd';
        $uid=$_SESSION['uid'];

		$username=S_get_entry($Db,'SELECT username FROM li_user WHERE id='.$uid.';');
		$newpassword1 = $_POST['newpassword1'];
		$newpassword2 = $_POST['newpassword2'];
		$newpasswordhash = password_hash($_POST['newpassword1'], PASSWORD_BCRYPT);
		/* Is entered new password okay */
		if (!preg_match("#.*^(?=.{10,64})(?=.*[a-zA-Z])(?=.*[0-9]).*$#", $newpassword1)) {
			$errorhtml1=H_build_boxinfo( 400, '<span class="icon-warning"></span> Passwortstärke nicht ausreichend.<br>Passwort muss aus 10 bis 64 Zeichen bestehen und Ziffern wie auch Buchstaben enthalten.', 'red' );
		} else {
			/* Are both new passwords identical */
			if ($newpassword1 != $newpassword2) {
				$errorhtml1=H_build_boxinfo( 400, '<span class="icon-warning"></span> Passwörter stimmen nicht überein.', 'red' );
			} else {
				S_set_data($Db,'UPDATE li_user SET password_hash=\''.$newpasswordhash.'\' WHERE id='.$uid.';');
				$errorhtml1=H_build_boxinfo( 400, 'Neues Passwort wurde übernommen.', 'green' );
			}
		}
	}
}


// Print html header
echo $GLOBALS['G_html_header'];



// Print html menu
echo $GLOBALS['G_html_menu'];
echo $GLOBALS['G_html_menu2'];



echo $GLOBALS['G_html_common_fp'];

// Print html content part A
echo $GLOBALS['G_html_main_right_a'];
// Print head line
echo "<h1 class=\"FAIR-blk\" style=\"background-color:#fff;\">Benutzerverwaltung</h1>";

echo '<div style="text-align: center;">';
echo '<div style="margin-bottom:45px; margin-top:15px;">';

$box_width=400;

// Set password or reset password
if ($mode=='chgpwd') {
	$html_box_login.= '<div style="text-align: left; display: inline-block; vertical-align: top;">';
	$html_box_login.= H_build_boxhead( $box_width, 'boxl1', 'Passwort setzen oder ändern' );
	$html_box_login.= '<div class="FAIR-foldbox-static-part">';
	$html_box_login.= '
	<form action="'.$current_site.'.php" method="post">
	<div class="FAIR-si-box">';
	$html_box_login.= '<input type="text" class="FAIR-textbox-large-ro" name="username" placeholder="E-Mail" value="'.$username.'" readonly/>';
	$html_box_login.= '</div>';
	$html_box_login.= '<div class="FAIR-si-box">User ID: ';
	$html_box_login.= '<input type="text" class="FAIR-textbox-small-ro" name="uid" placeholder="User ID" value="'.$uid.'" readonly/>';
	$html_box_login.= '</div>';
	$html_box_login.= '<div class="FAIR-si-box">';
	$html_box_login.= '<input type="password" class="FAIR-textbox-large" name="newpassword1" placeholder="Neues Passwort" />';
	$html_box_login.= '</div>';
	$html_box_login.= '<div class="FAIR-si-box">';
	$html_box_login.= '<input type="password" class="FAIR-textbox-large" name="newpassword2" placeholder="Passwort wiederholen" />';
	$html_box_login.= '</div>';
	$html_box_login.= $errorhtml1;
	$html_box_login.= '<div class="FAIR-si-button">';
	$html_box_login.= '<input type="submit" class="btn btn-warning" value="Passwort eintragen" name="button-change" />';
	$html_box_login.= '</div>
	</form>
	';
	$html_box_login.= '</div>';
	$html_box_login.= '<p></p>';
	$html_box_login.='<ul class="FAIR-editmenu-ul">';
	$html_box_login.='<li class="FAIR-editmenu-sep"></li>';
	$html_box_login.= '<li class="FAIR-editmenu-ul"><a class="FAIR-editmenu-td" href="'.$current_site.'.php">
	<div class="FAIR-editmenu-left"><span class="icon-arrow-left10"></span><span style="margin-left:10px;"></span>Benutzerverwaltung</div><div class="FAIR-editmenu-right"></div>
	</a></li>';
	$html_box_login.='<li class="FAIR-editmenu-sep"></li>';
	$html_box_login.= '</ul>';
	
	$html_box_login.= H_build_boxfoot( );
	$html_box_login.= '</div>';
	
	echo $html_box_login;

}

echo '</div>';
echo '</div>';


// Print html content part C
echo $GLOBALS['G_html_main_right_c'];

// Print html footer
echo $GLOBALS['G_html_footer'];
// Close connection to database
S_close_db($Db);


?>