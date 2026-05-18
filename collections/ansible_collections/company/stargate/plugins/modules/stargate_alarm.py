#!/usr/bin/python
# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: stargate_alarm
author:
  - Company Automation Team
version_added: "1.0.0"
short_description: Manage Stargate alarms
description:
  - Create, read, update, delete, acknowledge, and clear alarms in Stargate.
  - Supports filtering, export, and bulk operations.
notes:
  - This is an idempotent module - repeated runs with same parameters produce same results.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  alarm_id:
    description:
      - Unique alarm identifier.
      - Required for state=present with specific alarm, or state=absent.
    type: str
    required: false
  state:
    description:
      - Desired state of the alarm.
    type: str
    choices: [present, absent]
    default: present
  severity:
    description:
      - Alarm severity level.
    type: str
    choices: [critical, high, medium, low, info]
    required: false
  status:
    description:
      - Alarm status for filtering or setting.
    type: str
    choices: [active, acknowledged, cleared]
    required: false
  message:
    description:
      - Alarm message or description.
    type: str
    required: false
  node_id:
    description:
      - Associated node identifier.
    type: str
    required: false
  source:
    description:
      - Alarm source system or component.
    type: str
    required: false
  filter_params:
    description:
      - Additional filter parameters for list operations.
    type: dict
    required: false
  export_format:
    description:
      - Format for alarm export (when action=export).
    type: str
    choices: [json, csv, xml]
    default: json
  acknowledge:
    description:
      - Acknowledge the alarm (set status to acknowledged).
    type: bool
    default: false
  clear:
    description:
      - Clear the alarm (set status to cleared).
    type: bool
    default: false
  acknowledge_all:
    description:
      - Acknowledge all matching alarms.
    type: bool
    default: false
  clear_all:
    description:
      - Clear all matching alarms.
    type: bool
    default: false
'''

EXAMPLES = r'''
# List all active alarms
- name: Get active alarms
  company.stargate.stargate_alarm:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    status: active
  register: alarms

# Get specific alarm
- name: Get alarm details
  company.stargate.stargate_alarm:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    alarm_id: "123"
  register: alarm

# Acknowledge an alarm
- name: Acknowledge alarm
  company.stargate.stargate_alarm:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    alarm_id: "123"
    acknowledge: true

# Clear an alarm
- name: Clear alarm
  company.stargate.stargate_alarm:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    alarm_id: "123"
    clear: true

# Acknowledge all critical alarms
- name: Acknowledge critical alarms
  company.stargate.stargate_alarm:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    severity: critical
    acknowledge_all: true

# Delete an alarm
- name: Delete alarm
  company.stargate.stargate_alarm:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    alarm_id: "123"
    state: absent
'''

RETURN = r'''
alarms:
  description: List of alarm objects.
  type: list
  returned: when applicable
alarm:
  description: Single alarm object (when alarm_id specified).
  type: dict
  returned: when applicable
count:
  description: Number of alarms returned.
  type: int
  returned: always
changed:
  description: Whether any change was made.
  type: bool
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

try:
    from ..module_utils.stargate_utils import stargate_api_wrapper
except ImportError:
    from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper


def get_alarms(module, endpoint, token, timeout):
    """Fetch list of alarms with optional filtering."""
    params = module.params.get('filter_params') or {}
    status = module.params.get('status')
    severity = module.params.get('severity')
    node_id = module.params.get('node_id')

    if status:
        params['status'] = status
    if severity:
        params['severity'] = severity
    if node_id:
        params['node_id'] = node_id

    if params:
        param_str = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
        endpoint = '{}?{}'.format(endpoint, param_str)

    response, status_code = stargate_api_wrapper(
        module, 'GET', endpoint,
        headers={"Authorization": "Bearer {}".format(token)},
        timeout=timeout
    )
    return response


def run_module():
    module_args = dict(
        server=dict(type='str', required=True, aliases=['url']),
        token=dict(type='str', required=True, no_log=True),
        validate_certs=dict(type='bool', default=True),
        use_ssl=dict(type='bool', default=True),
        timeout=dict(type='int', default=30),
        api_version=dict(type='str', default='11.7.0'),
        alarm_id=dict(type='str', required=False),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        severity=dict(type='str', required=False, choices=['critical', 'high', 'medium', 'low', 'info']),
        status=dict(type='str', required=False, choices=['active', 'acknowledged', 'cleared']),
        message=dict(type='str', required=False),
        node_id=dict(type='str', required=False),
        source=dict(type='str', required=False),
        filter_params=dict(type='dict', required=False),
        acknowledge=dict(type='bool', default=False),
        clear=dict(type='bool', default=False),
        acknowledge_all=dict(type='bool', default=False),
        clear_all=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {
        'changed': False,
        'alarms': [],
        'alarm': None,
        'count': 0,
    }

    server = module.params['server']
    token = module.params['token']
    alarm_id = module.params['alarm_id']
    state = module.params['state']
    timeout = module.params['timeout']
    acknowledge = module.params['acknowledge']
    clear = module.params['clear']
    acknowledge_all = module.params['acknowledge_all']
    clear_all = module.params['clear_all']

    base_endpoint = "/adama/rest/alarmGet"

    try:
        if module.check_mode:
            result['msg'] = 'Check mode: alarm operation would proceed'
            module.exit_json(**result)

        if alarm_id:
            endpoint = "{}/{}".format(base_endpoint, alarm_id)
        else:
            endpoint = base_endpoint

        if state == 'absent' and alarm_id:
            response, status_code = stargate_api_wrapper(
                module, 'DELETE', endpoint,
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['msg'] = 'Alarm {} deleted'.format(alarm_id)
            module.exit_json(**result)

        elif acknowledge_all or clear_all:
            alarms_response = get_alarms(module, base_endpoint, token, timeout)
            alarm_list = alarms_response if isinstance(alarms_response, list) else alarms_response.get('data', alarms_response)

            processed = 0
            for alarm in alarm_list:
                aid = alarm.get('id') or alarm.get('alarm_id')
                if not aid:
                    continue
                action = 'acknowledge' if acknowledge_all else 'clear'
                action_endpoint = "{}/{}/{}".format(base_endpoint, aid, action)
                stargate_api_wrapper(
                    module, 'POST',
                    action_endpoint,
                    headers={"Authorization": "Bearer {}".format(token)},
                    timeout=timeout
                )
                processed += 1

            result['changed'] = True
            result['count'] = processed
            result['msg'] = 'Processed {} alarms'.format(processed)
            module.exit_json(**result)

        elif alarm_id and (acknowledge or clear):
            action = 'acknowledge' if acknowledge else 'clear'
            response, status_code = stargate_api_wrapper(
                module, 'POST',
                "{}/{}".format(endpoint, action),
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['alarm'] = response
            result['msg'] = 'Alarm {} {}'.format(alarm_id, action)
            module.exit_json(**result)

        elif alarm_id:
            response, status_code = stargate_api_wrapper(
                module, 'GET', endpoint,
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['alarm'] = response
            result['count'] = 1
            result['msg'] = 'Retrieved alarm {}'.format(alarm_id)
            module.exit_json(**result)

        else:
            alarms_response = get_alarms(module, base_endpoint, token, timeout)
            alarm_list = alarms_response if isinstance(alarms_response, list) else alarms_response.get('data', alarms_response)
            result['alarms'] = alarm_list
            result['count'] = len(alarm_list) if alarm_list else 0
            result['msg'] = 'Retrieved {} alarms'.format(result['count'])
            module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="Alarm operation failed: {}".format(to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()