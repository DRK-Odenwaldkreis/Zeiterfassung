<?php

/* **************

Zeiterfassung für das Impfzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
January 2021

file with HTML elements
to construct website frame
and some global used values
** ************** */



// HTML header with complete <head> element
$G_html_header='<html lang="en">
  <head>
    <title>DRK Impfzentrum - Zeiterfassung</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	
<link rel="shortcut icon" href="index.ico" type="image/x-ico; charset=binary" />
<link rel="icon" href="index.ico" type="image/x-ico; charset=binary" />


<link href="css/bootstrap.css" rel="stylesheet">
<!-- Custom styles for this template -->
<link href="css/dashboard.css" rel="stylesheet">
    
  </head>';

// HTML body with menu
// contains start of <body> element
$G_html_menu='<body>';
$G_html_menu_login='<body style="background-color:#101010;">';
$G_html_menu2='<nav class="navbar navbar-inverse navbar-fixed-top FAIR-navbar">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-brand" href="index.php"><span style="color:#eee;">ImpfZEr</span><span class="shorten"> Impfzentrum Zeiterfassung</span></a>';
if($_SESSION['uid']>0) {
	$G_html_menu2.='<ul class="nav navbar-nav navbar-left">';
	
	

	// Print button "Suche"
	$G_html_menu2.='<li><a href="search.php">Suche</a></li>';



	// Logged in / expiration of cookie
	$cookievalue=json_decode($_COOKIE['drk-cookie']);
	$expiry=$cookievalue->expiry;
	$expiry_diff=($expiry-time())/60; // in minutes
	if($expiry_diff<20) {$expiry_diff=20;}
	if( floor($expiry_diff / 60) < 2 ) { $expiry_text=ceil($expiry_diff).' Min.'; } // ceil = round up
	else { $expiry_text=ceil($expiry_diff / 60).' Std.'; } // ceil = round up
	$G_html_menu2.='<li title="Eingeloggt für '.$expiry_text.'" data-toggle="tooltip" data-placement="bottom" class="shorten"><a style="color:#fff; font-size:85%;"><span class="icon-clock2"></span>&nbsp;'.$expiry_text.'</a></li>';
	
	$G_html_menu2.='<li><a href="logout.php" style="color: #fff; background-color: #9f0000;">Logout</a></li>';
} else {
	$G_html_menu2.='</div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
			<li><a href="impressum.php">Impressum</a></li>
			<li><a href="login.php" style="color: #fff; background-color: #419f00;">Login</a></li>';
}
$G_html_menu2.='</ul>
        
          </ul>
        </div>
      </div>
    </nav>
';

// HTML element for content
$G_html_main_right_a='<main role="main" class="FAIR-main-col">';

// HTML section for database table and its content
// Content is produced with JS after initialisation of site
$G_html_main_right_b='
		  <div class="table-responsive">
		  <table id="main-tab" class="table table-striped display" width="100%"></table>
		  </div>
		  
		  <div class="table-responsive" style="visibility: hidden; position: fixed;">
		  <table id="comment-tab" class="table table-striped display" width="100%"></table>
		  </div>
';

// HTML closure elements before footer
$G_html_main_right_c='
        </main>
      </div>
    </div>';

// HTML footer section with closure of <body> and <html> elements
$G_html_footer='
  </body>
</html>';


// HTML closure elements before footer
$G_html_no_permission='
        <div style="padding-top:8px;"><h2 class="FAIR-redgrey">Keine Berechtigung</h2></div>';
	
?>