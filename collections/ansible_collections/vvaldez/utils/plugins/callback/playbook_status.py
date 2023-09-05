from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
from ansible import constants as C
from ansible.utils.color import colorize, hostcolor
from ansible.utils.display import Display
from ansible.module_utils._text import to_text
import json
import requests

DOCUMENTATION = '''
    name: playbook_status
    type: notification
    short_description: sends playbook status to a provided endpoint
    description:
      - Sends API POST to endpoint during playbook events
    requirements:
      - a REST API endpoint with an authorization token

    options:
      playbook_status_url:
        description: REST API endpoint URL
        env:
          - name: playbook_status_url
        ini:
          - section: callback_playbook_status
            key: playbook_status_url
      playbook_status_token:
        description: endpoint authorization token
        env:
          - name: playbook_status_token
        ini:
          - section: callback_playbook_status
            key: playbook_status_token
      playbook_status_action:
        description: endpoint action. valid values are [demo,post]
        env:
          - name: playbook_status_action
        ini:
          - section: callback_playbook_status
            key: playbook_status_action
    '''

class CallbackModule(CallbackBase):

    '''
    Call all the runner functions here
    '''

    CALLBACK_VERSION = 2.0                          # you should use version 2.0 at the time of wrtiting this post
    CALLBACK_TYPE = 'notification'                  # you can only use 1 stdout plugin at a time, so used notification
    CALLBACK_NAME = 'playbook_status'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__()
        self.playbook_status_url = None
        self.playbook_status_token = None
        self.playbook_status_headers = None
        self.playbook_status_action = None

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)
        self.playbook_status_url = self.get_option('playbook_status_url')
        self.playbook_status_token = self.get_option('playbook_status_token')
        self.playbook_status_headers = { 'Authorization': "Token %s" % self.playbook_status_token, 'Content-type': 'application/json' }
        self.playbook_status_action = self.get_option('playbook_status_action')

    def send_status(self, playbook_status_url, playbook_status_data, playbook_status_headers, playbook_status_action):
        self._display.display("INFO: callback plugin playbook_status: %s. ACTION: %s" % (playbook_status_data, playbook_status_action),color=C.COLOR_OK)
        # Action of 'demo' will NOT attempt to post to the given URL, but rather debug what it would do. This is useful when no REST API endpoint is available
        if playbook_status_action.lower() == "demo":
            self._display.display("DEBUG: Running requests.post() with parameters url: " + str(playbook_status_url) + " data: " + str(playbook_status_data) + " headers: " + str(playbook_status_headers),color=C.COLOR_OK)
        elif playbook_status_action.lower() == "post":
            r = requests.post(playbook_status_url, data=json.dumps(playbook_status_data), headers=playbook_status_headers)
        elif playbook_status_action.lower() == "":
            self._display.display("fatal: FAILED! No action was defined for this plugin!", color=C.COLOR_ERROR)
        else:
            self._display.display("fatal: FAILED! Unknown action of [%s]!" % playbook_status_action, color=C.COLOR_ERROR)

    def playbook_on_start(self):
        self.playbook_status_data = { 'playbook_status': 'Playbook started' }
        self.send_status(self.playbook_status_url, self.playbook_status_data, self.playbook_status_headers, self.playbook_status_action)

    def playbook_on_play_start(self, name):
        self.playbook_status_data = { 'playbook_status': "Play '" + name + "' started." }
        self.send_status(self.playbook_status_url, self.playbook_status_data, self.playbook_status_headers, self.playbook_status_action)

    def playbook_on_task_start(self, name, is_conditional):
        self.playbook_status_data = { 'playbook_status': "Task '" + name + "' started." }
        self.send_status(self.playbook_status_url, self.playbook_status_data, self.playbook_status_headers, self.playbook_status_action)

    def playbook_on_stats(self, stats):
        self.playbook_status_data = { 'playbook_status': "Playbook complete." }
        self.send_status(self.playbook_status_url, self.playbook_status_data, self.playbook_status_headers, self.playbook_status_action)