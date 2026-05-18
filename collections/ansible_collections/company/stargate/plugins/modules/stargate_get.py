#!/usr/bin/python
# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: stargate_get
author:
  - Company Automation Team
version_added: "1.0.0"
short_description: Generic GET requests to Stargate REST API
description:
  - Makes GET requests to Stargate REST API endpoints.
  - Supports check_mode, idempotency, and response parsing.
notes:
  - Use this module for read-only operations against any API endpoint.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  endpoint:
    description:
      - API endpoint path to query.
      - Should start with /api/ or /.
    type: str
    required: true
  params:
    description:
      - Query parameters to append to the URL.
    type: dict
    required: false
  return_raw:
    description:
      - Return raw response without JSON parsing.
    type: bool
    default: false
'''

EXAMPLES = r'''
# Get all alarms
- name: Fetch all alarms
  company.stargate.stargate_get:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    endpoint: "/api/alarms"

# Get specific alarm by ID
- name: Fetch alarm details
  company.stargate.stargate_get:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    endpoint: "/api/alarms/123"

# Get nodes with filters
- name: Get active nodes
  company.stargate.stargate_get:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    endpoint: "/api/nodes"
    params:
      status: active
      site: site1
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
        params=dict(type='dict', required=False, default=None),
        return_raw=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {
        'changed': False,
        'data': None,
        'status_code': None,
    }

    server = module.params['server']
    token = module.params['token']
    endpoint = module.params['endpoint']
    params = module.params['params']
    return_raw = module.params['return_raw']
    timeout = module.params['timeout']
    validate_certs = module.params['validate_certs']
    use_ssl = module.params['use_ssl']
    api_version = module.params['api_version']

    try:
        if module.check_mode:
            result['msg'] = 'Check mode: would perform GET to {}'.format(endpoint)
            module.exit_json(**result)

        # Build endpoint with query params if provided
        if params:
            param_str = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
            endpoint = '{}?{}'.format(endpoint, param_str) if '?' not in endpoint else '{}&{}'.format(endpoint, param_str)

        response, status_code = stargate_api_wrapper(
            module,
            'GET',
            endpoint,
            headers={"Authorization": "Bearer {}".format(token)},
            timeout=timeout
        )

        if return_raw:
            result['data'] = response
        else:
            result['data'] = response

        result['status_code'] = status_code
        result['msg'] = 'Successfully retrieved data from {}'.format(endpoint)
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="GET request failed: {}".format(to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()