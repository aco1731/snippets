#!/usr/bin/env python
import thread
from ncclient import manager
from bs4 import BeautifulSoup
import sys, os, warnings


def nxos_connect(host, port, user, password):
    return manager.connect(host=host, port=port, username=user, 
                         password=password,hostkey_verify=False,device_params={'name': 'nexus'})


def nxos_backup(switch,login,password):

    with nxos_connect(host=switch, port=22, user=login, password=password) as m:
        cmd={'show running-config'}
        cisco_output = str( m.exec_command(cmd))
        soup = BeautifulSoup(cisco_output,"lxml")
        textfile = soup.find('data').text.strip()
        arq = switch + ".txt"
        with open(arq, 'w') as f:
            f.write(textfile)


if __name__ == '__main__':
    #nxos_backup(sys.argv[1], sys.argv[2], sys.argv[3])
    try:
        thread.start_new_thread(nxos_backup, ("DSWRJCV500", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV501", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV510", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV511", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV514", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV515", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV516", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV517", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV518", "login", "password"))
        thread.start_new_thread(nxos_backup, ("DSWRJCV519", "login", "password"))
    except:
        print "Error: Thread"
    
