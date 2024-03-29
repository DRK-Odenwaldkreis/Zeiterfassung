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
$current_site="download";

// Include functions
include_once 'tools.php';
include_once 'auth.php';

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $file=($_GET['file']);
    if(isset($_GET['dir'])) { $dir_id=$_GET['dir']; } else {$dir_id=0;}
    switch($dir_id) {
        case "r":
            $dir="Reports";
            break;
        case "d":
            $dir="Dienstplaene";
            break;
        case "p":
            $dir="Planung";
            break;
        default:
            $dir="Reports";   
    }
    
    if( file_exists($GLOBALS["SYSPATH_main"]."$dir/$file") ) {
        //header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="'.basename($file).'"');
        header('Pragma: no-cache');
        header('Expires: 0');
        //header('Content-Length: ' . filesize($file));
        readfile($GLOBALS["SYSPATH_main"]."$dir/$file");
        exit;
    }
}
?>