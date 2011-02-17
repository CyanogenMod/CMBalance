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
            <img src="https://www.google.com/adsense/static/en_US/images/leaderboard.gif">
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