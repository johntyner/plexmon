#!/usr/bin/env python3

import collections
import dotenv
import requests
import json

# Suppress only the single warning from urllib3 needed.
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

defcfg = collections.OrderedDict()
defcfg['plex_addr'] = 'https://localhost:32400'
defcfg['plex_token'] = ''
defcfg['truenas_addr'] = 'https://localhost'
defcfg['truenas_apikey'] = ''
defcfg['plex_jail'] = 'plexmediaserver'

config = dotenv.dotenv_values('plexmon.conf')
for k in defcfg:
    if not k in config:
        config[k] = defcfg[k]

try:
    plex_session = requests.Session()
    plex_session.verify=False

    r = plex_session.get(
        config['plex_addr'] + '/',
        headers={
            'X-Plex-Token': config['plex_token']
        })
    if r.status_code not in (200, 201, 204):
        raise ConnectionError
except Exception as e:
    print('Restarting Plex Media Server...')

    truenas_session = requests.Session()
    truenas_session.verify=False

    r = truenas_session.post(
        config['truenas_addr'] + '/api/v2.0/jail/restart',
        headers={
            'Authorization': 'Bearer ' + config['truenas_apikey'],
            'Content-Type': 'application/json',
        },
        data=json.dumps(config['plex_jail']))
