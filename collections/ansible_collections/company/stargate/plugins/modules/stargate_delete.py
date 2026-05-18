#!/usr/bin/python
# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: stargate_delete
author:
  - Company Automation Team
version_added: "1.0.0"
short_description: Generic DELETE requests to Stargate REST API
description:
  - Makes DELETE requests to Stargate REST API endpoints.
  - Supports check_mode and idempotency.
notes:
  - Use this module for removing resources via the API.
  - Most delete operations are idempotent - deleting already-deleted resources typically returns 404 or 204.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  endpoint:
    description:
      - API endpoint path to delete.
      - Should start with /api/ or /.
    type: str
    required: true
'''

EXAMPLES = r'''
# Delete an alarm
- name: Delete alarm
  company.stargate.stargate_delete:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    endpoint: "/api/alarms/123"

# Remove a service
- name: Delete service
  company.stargate.stargate_delete:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    endpoint: "/api/services/456"
'''

RETURN = r'''
data:
  description: Response data from the API endpoint.
  type: dict or list
  returned: when available
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
    timeout = module.params['timeout']

    try:
        if module.check_mode:
            result['changed'] = False
            result['msg'] = 'Check mode: would perform DELETE on {}'.format(endpoint)
            module.exit_json(**result)

        response, status_code = stargate_api_wrapper(
            module,
            'DELETE',
            endpoint,
            headers={"Authorization": "Bearer {}".format(token)},
            timeout=timeout
        )

        result['data'] = response
        result['status_code'] = status_code
        result['msg'] = 'Successfully deleted {}'.format(endpoint)
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="DELETE request failed: {}".format(to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()