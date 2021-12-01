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


// ///////////////////////////////////////////
// FOLLOWING VALUES MUST BE SET FOR PROPER USE

// admin email /not in use right now?/
$ADMINEMAIL = 'support@impfzentrum-odw.com';
//$ADMINEMAIL = 'support@testzentrum-odw.com';

// write in here the domain, e.g. 'example.com/'
$HOSTNAME_WEB = 'impfzentrum-odw.de/';
//$HOSTNAME_WEB = 'dienst.testzentrum-odw.de/';

// header names and system names
$SYSNAME_display = 'Impfzentrum Zeiterfassung';
//$SYSNAME_display = 'Testzentrum Zeiterfassung';
$SYSNAME_preheaddisplay = 'DRK';

// for imprint site - links to email and telephone (set in <p>-tag)
$SYSNAME_imprint_org_link = '<p><a href="mailto:dienstplan.impfzentrum@drk-odenwaldkreis.de">dienstplan.impfzentrum@drk-odenwaldkreis.de</a></p><p><a href="tel:+4960626019994">Telefon: 06062 - 60 19 994</a></p>';
//$SYSNAME_imprint_org_link = '<p><a href="mailto:testzentrum@drk-odenwaldkreis.de">testzentrum@drk-odenwaldkreis.de</a></p>';
$SYSNAME_imprint_support_link = '<p><a href="mailto:support@impfzentrum-odw.de">support@impfzentrum-odw.de</a></p>';
//$SYSNAME_imprint_support_link = '<p><a href="mailto:info@testzentrum-odenwald.de">info@testzentrum-odenwald.de</a></p>';

// with this email address outgoing mail will be sent
$SYSNAME_mail_sending = 'support@impfzentrum-odw.de';
//$SYSNAME_mail_sending = 'info@testzentrum-odenwald.de';

// to this email address reports will be sent
$SYSNAME_mail_report = 'report@impfzentrum-odw.de';
//$SYSNAME_mail_report = 'info@testzentrum-odenwald.de';

// to this email address shift plans will be sent / reply-to address
$SYSNAME_mail_shift_bcc = 'dienstplan.impfzentrum@drk-odenwaldkreis.de';
//$SYSNAME_mail_shift_bcc = 'testzentrum@drk-odenwaldkreis.de';



// pathes
$SYSPATH_main = '/home/webservice/';
//$SYSPATH_main = '/home/webservice_testz/';

$SYSPATH_logs = '/home/webservice/Logs/';
//$SYSPATH_logs = '/home/webservice_testz/Logs/';

$SYSPATH_reports = '/home/webservice/Reports/';
//$SYSPATH_reports = '/home/webservice_testz/Reports/';

$SYSPATH_scripts = '/home/webservice/Zeiterfassung/';
//$SYSPATH_scripts = '/home/webservice_testz/Zeiterfassung/';



// modules - can be switched on and off
// // Show "Verrechnung" in Dropdown and in List
$SYSMOD_Verrechnung=false;
// // Show "Kostenstelle" in Dropdown and in List
$SYSMOD_Kostenstelle=false;



// only for login and password reset function
$LOGINTOKENTIME = 6;
$LOCK_VALUE_THRESHOLD = 6;

?>
