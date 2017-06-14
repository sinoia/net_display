#!/usr/bin/env python
'''This example shows how a dashboard can be created on the net display and
then updated periodically.'''
import os
import socket
import requests

hostname = socket.gethostname()
port = 8888
url = 'http://'+hostname+':'+str(port)

def get_cpu():
    return "Dunno!"""

if __name__ == "__main__":
    r = requests.put(url+'/page_title', data = 'Server Monitor')
    # now we create some html for the message. This html contains new
    # element ids which can then be updated in later calls
    html = '''
    <table>
    <tr><th>CPU</th><td id="cpu"></td></tr>
    <tr><th>Memory</th><td id="mem"></td></tr>
    <tr><th>Storage</th><td id="disc"></td></tr>
    </table>
    '''
    r = requests.put(url+'/message', data = html)
    r = requests.put(url+'/cpu', data = '10')
    r = requests.put(url+'/mem', data = '20')
    r = requests.put(url+'/disc', data = '30')
