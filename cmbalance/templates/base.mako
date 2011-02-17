<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="stylesheet" type="text/css" href="/static/core.css" />
    </head>
    <body>
        <header id="logo">
            <img src="/static/logo.png" alt="cyanogen(mod) mirror network" />
        </header>
        
        <nav id="navigation">
            <ul>
                <li><a href="/">Recent Files</a></li>
                <li class="break">By Type</li>
                <li class="bullet"><a href="/?type=stable">stable</a></li>
                <li class="bullet"><a href="/?type=RC">release candidate</a></li>
                <li class="bullet"><a href="/?type=nightly">nightly</a></li> 
                <li class="break">By Device</li>
                % for device in devices:
                <li class="bullet"><a href="/?device=${device.name}">${device.name}</a></li>
                % endfor
                <li class="break">Mirrors</li>
                <li class="bullet"><a href="/mirrors/list">list</a></li>
                <li class="bullet"><a href="/mirrors/become">become a mirror</a></li>
            </ul>
        </nav>
        <section id="container">
<script type="text/javascript"><!--
google_ad_client = "ca-pub-4305693279235670";
/* TeamDouche Mirror */
google_ad_slot = "5118872808";
google_ad_width = 728;
google_ad_height = 90;
//-->
</script> 
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js"> 
</script> 
            <br/><br/>
            ${next.body()}
        </section>
        <aside>
            <a href="http://tdrevolution.com/whmcs/link.php?id=7" target="_new">
                <img src="/static/tdr_skyscraper.png">
            </a>
        </aside>
    </body>
</html>