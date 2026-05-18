#!/usr/bin/python
# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: stargate_post
author:
  - Company Automation Team
version_added: "1.0.0"
short_description: Generic POST requests to Stargate REST API
description:
  - Makes POST requests to Stargate REST API endpoints.
  - Supports check_mode, idempotency, and response parsing.
notes:
  - Use this module for creating resources or invoking actions via the API.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  endpoint:
    description:
      - API endpoint path to post to.
      - Should start with /api/ or /.
    type: str
    required: true
  data:
    description:
      - Request body data to send as JSON.
    type: dict
    required: false
  return_raw:
    description:
      - Return raw response without JSON parsing.
    type: bool
    default: false
'''

EXAMPLES = r'''
# Create an alarm
- name: Create alarm
  company.stargate.stargate_post:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    endpoint: "/api/alarms"
    data:
      severity: critical
      message: "High CPU usage detected"
      node_id: "node-001"

# Acknowledge an alarm
- name: Acknowledge alarm
  company.stargate.stargate_post:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    endpoint: "/api/alarms/123/acknowledge"

# Trigger a service restart
- name: Restart service
  company.stargate.stargate_post:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    endpoint: "/api/services/456/restart"
'''

RETURN = r'''
data:
  description: Response data from the API endpoint.
  type: dict or list
  returned: always
status_code:
  description: HTTP status code from the response.
  type: int
  returned: always
changed:
  description: Whether the operation caused a change.
  type: bool
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

try:
    from ..module_utils.stargate_utils import stargate_api_wrapper
except ImportError:
    from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper


def run_module():
    module_args = dict(
        server=dict(type='str', required=True, aliases=['url']),
        token=dict(type='str', required=True, no_log=True),
        validate_certs=dict(type='bool', default=True),
        use_ssl=dict(type='bool', default=True),
        timeout=dict(type='int', default=30),
        api_version=dict(type='str', default='11.7.0'),
        endpoint=dict(type='str', required=True),
        data=dict(type='dict', required=False, default=None),
        return_raw=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {
        'changed': True,
        'data': None,
        'status_code': None,
    }

    server = module.params['server']
    token = module.params['token']
    endpoint = module.params['endpoint']
    data = module.params['data']
    return_raw = module.params['return_raw']
    timeout = module.params['timeout']

    try:
        if module.check_mode:
            result['changed'] = False
            result['msg'] = 'Check mode: would perform POST to {}'.format(endpoint)
            module.exit_json(**result)

        response, status_code = stargate_api_wrapper(
            module,
            'POST',
            endpoint,
            data=data,
            headers={"Authorization": "Bearer {}".format(token)},
            timeout=timeout
        )

        result['data'] = response
        result['status_code'] = status_code
        result['msg'] = 'Successfully posted data to {}'.format(endpoint)
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="POST request failed: {}".format(to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()