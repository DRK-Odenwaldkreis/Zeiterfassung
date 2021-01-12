<!doctype html>

<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

error site

** ************** */

include_once 'preload.php';

$errorcode=isset($_GET['e']) ? $_GET['e'] : 0 ;

switch ($errorcode) {
	case 'err80':
		// nosqlconnection
		echo "<h1>Error / Fehler (80)</h1>";
		echo '<p><b>Keine Verbindung zum Server möglich. Bitte zu einem späteren Zeitpunkt nochmal versuchen.</b></p>';
	break;
}

?>