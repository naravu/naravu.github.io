#!/bin/sh
#Fetch system report and display in html format

#Current path
way="shviapy.html"
echo "<html><head><title>$(hostname)&copy;</title><style>#myDIV {position: fixed; right: 0; top: 0; width: 6em; height: 100%; background-color: #d0d6df; color: #000000; text-decoration: none; font-size: 10pt; font-face: serif; list-style-type:none; visibility: show;} .classic {font-size: 12pt; background-color: #d0d6df; font-family: tahoma; margin-top: 0px; margin-right: 95px; text-decoration: bold; position: fixed; top:0; right:0; z-index: 2} #foot{position: relative; right: 0; bottom: 0; background-color: ffffff; width: 100%}  pre{tab-size: 8; background: #FFFFFF; color: #000000; padding: 10px; z-index: 2; border: 1px solid #000; width: 88%; } .container {position: relative; } .topright { position: absolute; top: 2px; right: 15px; font-size: 18px; border: 1px solid #ccc; background-color: #eee; color: #000000; z-index=2; } td{font-size: 15px; font-family: arial,sans-serif;} * {font-size: 1em; font-face: serif; } </style></head><body topmargin=0 leftmargin=4 rightmargin=0 bgcolor=#d0d6df>" > $way
echo "<div id=\"myDIV\"><ul id=myDIV><li></li><li><a href=#host>Host</a></li><li><a href='#network'>Network</a></li><li><a href='#swap'>Swap</li><li><a href='#user'>User</a></li><li><a href='#fstab'>FStab</li><li><a href='#file'>File</li><li><a href='#disk'>Disk</li><li><a href='#route'>Routes</li><a href='#port'>Ports</li><li><a href='#active'>Active</li><a href='#inactive'>Inactive</li><li><a href='#dmidecode'>System</li><li><a href='#dp'>Path</li><li><a href='#zombie'>Zombies</li><li><a href=javascript:window.print()>Print<a></li><li><script language=javascript>document.write('<a onclick=\"this.href=\'data:text/html;charset=UTF-8,\'+encodeURIComponent(document.documentElement.outerHTML)\" href=\'#\' download=\'$(hostname)-report.xls\'>Download</a>');</script></li><li><a href=# onclick=closeM()>Close</a><script> function closeM() { window.opener = self; window.close(); }</script></li><li><a href='#copy'>&copy;</a></li></ul></div>" >> $way
echo "<a name=host></a><b>Host Details</b><button class=classic onclick='myFunction()'>&#9776;</button><pre>$(hostnamectl)</pre>" >> $way
echo "<a name=network></a><b>Network Details</b><pre>$(ifconfig -a)</pre>" >> $way
echo "<a name=swap></a><font face=serif size=2><b>Swap Details</b></font><pre>$(free -h)</pre>" >> $way
echo "<a name=user></a><font face=serif size=2><b>Connected User Details</b></font><pre>$(w; cat /sys/class/power_supply/BAT0/capacity)</pre>" >> $way
echo "<a name=fstab></a><font face=serif size=2><b>FStab Details</b></font><pre>$(cat /etc/fstab)</pre>" >> $way
echo "<a name=file></a><font face=serif size=2><b>File System Details</b></font>" >> $way

#File System
echo "<div> <p>" >> $way
echo "<table cellpadding=0 cellspacing=0 border=0><tr><td>" >> $way
df -PTH > nets
cat nets | awk ' {print $5} ' | tail -n +1 | tr -d '%' > nets1
awk 'BEGIN {print "<table border=0 cellpadding=0 cellspaceing=0>"}
  {print "<tr>"; for(i = 1; i <= NF; i++) print "<td>" $i "</td>"; print "</tr>"}
  END {print "</table>"}' nets >> $way
echo "</td><td>" >> $way
awk 'BEGIN {print "<table border=0 cellpadding=0 cellspaceing=0>"}
  {print "<tr>"; for(i = 1; i <= NF; i++) print "<td>" $i "%</td><td><meter low=0.45 optimum=.2 high=0.75 value=" $i/100 "></meter>";  print "</td></tr>"}
  END {print "</table>"}' nets1 >> $way
echo "</td></tr></table>" >> $way
echo "</p></div>" >> $way

echo "<a name=disk></a><font face=serif size=2><b>Disk Details</b></font><pre>$(fdisk -l)</pre>" >> $way
echo "<a name=route></a><font face=serif size=2><b>Route Table Details</b></font><pre>$(netstat -nr)</pre>" >> $way
echo "<a name=port></a><font face=serif size=2><b>Listening Ports Details</b></font><pre>$(netstat -tupln|grep -i listen)</pre>" >> $way
echo "<a name=active></a><font face=serif size=2><b>Active Services</b></font><pre>$(systemctl list-units --all --type=service --no-pager | grep running)</pre>" >> $way
echo "<a name=inactive></a><font face=serif size=2><b>Inactive Services</b></font><pre>$(systemctl list-units --all --type=service --no-pager | grep exited)</pre>" >> $way
echo "<pre>$(systemctl list-units --all --type=service --no-pager | grep dead)</pre>" >> $way
echo "<a name=dmidecode></a><font face=serif size=2><b>System Details</b></font><pre>$(dmidecode)</pre>" >> $way
echo "<a name=inxi></a><font face=serif size=2><b>System Details New</b></font><pre>$(inxi -F)</pre>" >> $way
echo "<a name=zombie></a><font face=serif size=2><b>Zombies</b></font><pre>$(ps aux | grep 'defunct')</pre>" >> $way
echo "<a name=reboot></a><font face=serif size=2><b>Reboot</b></font><pre>$(last -x 2> /dev/null|grep reboot 1> /dev/null && /usr/bin/last -x 2> /dev/null|grep reboot|head -3 || \ echo -e "No reboot events are recorded.")</pre>" >> $way
echo "<a name=shut></a><font face=serif size=2><b>Shutdown</b></font><pre>$(last -x 2> /dev/null|grep shutdown 1> /dev/null && /usr/bin/last -x 2> /dev/null|grep shutdown|head -3 || \ echo -e "No shutdown events are recorded.")</pre>" >> $way
echo "<a name=mem></a><font face=serif size=2><b>Memory Hog</b></font><pre>$(ps -eo pmem,pid,ppid,user,stat,args --sort=-pmem|grep -v $$|head -6|sed 's/$/\n/')</pre>" >> $way
echo "<a name=cpuh></a><font face=serif size=2><b>CPU Hog</b></font><pre>$(ps -eo pcpu,pid,ppid,user,stat,args --sort=-pcpu|grep -v $$|head -6|sed 's/$/\n/')</pre>" >> $way

echo "<a name=dp></a><font face=serif size=2><b>Default Path</b></font><pre>$PATH</pre>" >> $way

echo "<a name=copy></a><div id=foot><pre> &copy; Last OS update: $(tail -1 /var/log/yum.log |cut -f1,2 -d' ') | Page update: $(date)</pre></div><script>function myFunction() {  var x = document.getElementById(\"myDIV\");  if (x.style.display === \"none\") {   x.style.display = \"block\";  } else {   x.style.display = \"none\";  }}</script></body></html>" >> $way

#--------Check Inode usage--------#