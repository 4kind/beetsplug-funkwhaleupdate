# -*- coding: utf-8 -*-
"""Updates a Funkwhale library whenever the beets album was added.
This is based on the Kodi Update plugin.

Put something like the following in your config.yaml to configure:
    funkwhale:
        host: localhost
        port: 5000
        token: 1abc2fd0f0asfüpal
        library_name: mymusic
"""
from __future__ import division, absolute_import, print_function

import requests
from beets import config
from beets.plugins import BeetsPlugin
from datetime import datetime
import six
import os


def update_funkwhale(host, port, token, library, item_path):
    """Sends request to the Funkwhale api to import items of the given path."""
    url = "http://{0}:{1}/api/v1/libraries/fs-import".format(host, port)

    headers = {
        'Content-Type': 'application/json', 
        'Authorization': "Bearer {0}".format(token)
    }

    date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+01:00")

    # Create the payload. Id seems to be mandatory.
    payload = {
        'path': item_path, 
        'library': library,
        'import_reference': date_time
    }
    
    return requests.post(url, json=payload, headers=headers)


class FunkwhaleUpdate(BeetsPlugin):
    def __init__(self):
        super(FunkwhaleUpdate, self).__init__()
       
        library_uuid = self.get_library_uuid(config['funkwhale']['library_name'].get())
        
        if library_uuid:
            self.init_listener(library_uuid)

    def get_library_uuid(self, library_name):
        host = config['funkwhale']['host']
        port = config['funkwhale']['port']
        token = config['funkwhale']['token']
        
        url = "http://{0}:{1}/api/v1/libraries".format(host, port)

        headers = {
            'Accept': 'application/json', 
            'Authorization': "Bearer {0}".format(token)
        }

        """Sends request to the Funkwhale to get library uuid by library name."""
        r = requests.get(url, headers=headers)

        for library in r.json().get('results'):
            if library_name == library['name']:
                return self.init_listener(library['uuid'])
    
    def init_listener(self, library_uuid):
        # Adding defaults.
        config['funkwhale'].add({
            u'host': u'localhost',
            u'port': 5000,
            u'library_uuid': library_uuid
        })

        self.register_listener('database_change', self.listen_for_db_change)

    def listen_for_db_change(self, lib, model):
        """Listens for beets db change and register the update"""
        self.register_listener('album_imported', self.update)

    def update(self, lib, album):
        """When the client exists try to send refresh request to Funkwhale server.
        """
        self._log.info(u'Requesting a Funkwhale library update...')

        item_path = os.path.relpath(album.item_dir(), lib.directory)

        # Try to send update request.
        try:
            r = update_funkwhale(
                config['funkwhale']['host'].get(),
                config['funkwhale']['port'].get(),
                config['funkwhale']['token'].get(),
                config['funkwhale']['library_uuid'].get(),
                item_path
            )

            r.raise_for_status()

        except requests.exceptions.RequestException as e:
            self._log.warning(u'Funkwhale update failed: {0}', six.text_type(e))
            return

        status_code = r.status_code
        if status_code != 201:
            self._log.warning(u'Funkwhale update failed: JSON response was {0!r}', json)
            return

        self._log.info(u'Funkwhale update triggered')
