<!doctype html>

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