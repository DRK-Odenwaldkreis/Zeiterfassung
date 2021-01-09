<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

login procedure

** ************** */



// Include functions
include_once 'server_settings.php';
include_once 'tools.php';

var_dump(function_exists('mysqli_connect'));

// Open database connection
$Db=S_open_db();




// Close connection to database
S_close_db($Db);

?>