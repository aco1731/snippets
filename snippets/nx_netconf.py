#!/usr/bin/env python

from ncclient import manager
from bs4 import BeautifulSoup as BS

def main():

    with manager.connect(host='10.0.192.201',
                         port=22,
                         username='aaaa',
                         password='xxxxx',
                         hostkey_verify=False,
                         device_params={'name': 'nexus'}
                         ) as cisco_manager:

        command1={'show running-config'}

        cisco_output = str( cisco_manager.exec_command(command1))
        soup = BS(cisco_output,"lxml")
        textfile = soup.find('data').text
        
        with open("N5K_LAB.txt", 'w') as f:
            f.write(textfile)

if __name__ == '__main__':
    main()
