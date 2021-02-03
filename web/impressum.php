<!-- # This file is part of DRK Zeiterfassung.

# DRK Zeiterfassung is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# DRK Zeiterfassung is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DRK Zeiterfassung.  If not, see <http://www.gnu.org/licenses/>. -->

<!doctype html>

<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

imprint site

** ************** */


include_once 'preload.php';
if( isset($GLOBALS['G_sessionname']) ) { session_name ($GLOBALS['G_sessionname']); }
session_start();
$current_site="impressum";
$sec_level=0;


// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';


// Print html header
echo $GLOBALS['G_html_header'];

// Print html menu
echo $GLOBALS['G_html_menu'];
echo $GLOBALS['G_html_menu2'];

// Print html content part A
echo $GLOBALS['G_html_main_right_a'];


if(isset( $_SESSION['uid']) && $_SESSION['uid']>=0 ) {
    echo '<h3>Personalorganisation</h3>
    <p>Bei Fragen zu Vertragsthemen oder organisatorischen Anfragen bitte eine E-Mail schreiben an:</p>
    <p><a href="mailto:corona-impfen@drk-odenwaldkreis.de">corona-impfen@drk-odenwaldkreis.de</a></p>
    <p>&nbsp;</p>';

    echo '<h3>Technischer Support</h3>
    <p><a target="_blank" href="https://github.com/DRK-Odenwaldkreis/Zeiterfassung#ablauf">Für die Dokumentation Terminal-Anwendung hier klicken</a></p>
    <p><a target="_blank" href="https://github.com/DRK-Odenwaldkreis/Zeiterfassung#webpage">Für die Dokumentation der Web-Anwendung hier klicken</a></p>
    <p>&nbsp;</p>
    <p>Bei technischen Fragen zum Zeiterfassungssystem bitte eine E-Mail schreiben an den Support:</p>
    <p><a href="mailto:support@impfzentrum-odw.de">support@impfzentrum-odw.de</a></p>
    <p>&nbsp;</p>';
}


echo '<h3>Impressum</h3>
<a href="https://drk-odenwaldkreis.de/impressum/">Direkt beim DRK Kreisverband Odenwaldkreis e. V.</a>';




// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];






?>