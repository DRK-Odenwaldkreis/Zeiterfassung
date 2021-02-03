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

// Include library for QR codes
include_once 'lib/phpqrcode/qrlib.php';

$param = $_GET['id']; // remember to sanitize that - it is user input!
    
// we need to be sure ours script does not output anything!!!
// otherwise it will break up PNG binary!

ob_start("callback");

// here DB request or some processing
$codeText = $param;

// end of processing here
$debugLog = ob_get_contents();
ob_end_clean();

// outputs image directly into browser, as PNG stream
QRcode::png($codeText,false,QR_ECLEVEL_H,6,4);

?>