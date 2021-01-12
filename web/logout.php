<?php
/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

logout procedure

** ************** */

include_once 'preload.php';
if( isset($GLOBALS['G_sessionname']) ) { session_name ($GLOBALS['G_sessionname']); }
session_start();
session_destroy();
setcookie('drk-cookie', '', time() - 7*24*60*60);

$hostname = $_SERVER['HTTP_HOST'];
$path = dirname($_SERVER['PHP_SELF']);
$FLAG_http='https';
header('Location: '.$FLAG_http.'://'.$hostname.($path == '/' ? '' : $path).'/login.php');
?>