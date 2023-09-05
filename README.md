# ansible-callback-plugin-playbook-status
Simple callback plugin to send playbook event status to an API endpoint. 

These events can be seen in the Ansible codebase along with shipped plugins here: https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/callback/

Every event that occurs within a playbook can initiate custom actions. This plugin takes advantage of that and sends realtime status as events occur. 

## Events

This plugin covers the folowing playbook events:

* playbook_on_start
* playbook_on_play_start
* playbook_on_task_start
* playbook_on_stats

Additional events available as of this commit:

* playbook_on_notify
* playbook_on_no_hosts_matched
* playbook_on_no_hosts_remaining
* playbook_on_vars_prompt
* playbook_on_setup
* playbook_on_import_for_host
* playbook_on_not_import_for_host

## Requirements

Simply place this callback plugin in a `callback_plugins` directory at the same level as the playbook, or put this plugin into a collection.

Next, run a playbook as normal and observe the additional output.

## REST API Endpoint

By default this callback plugin is designed to run in 'demo' mode, meaning it will simply print to your console what requests would be sent to the defined endpoint. If you have a REST API endpoint, you can specify the details in ansible.cfg or environment variables.

This callback plugin communicates to a REST API endpoint using a token as authorization. One simple method to spin up a quick endpoint is available here: https://rbaskets.in/web or to run a local instance see https://github.com/darklynx/request-baskets

## Capabilities

This callback plugin can be modified to do any number of things, for example accept username and password instead of a token. This would require handling that logic in each python function. 
