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
  - Makes POST requests to Stargate REST API endpoints (Stargate uses POST for all operations).
  - Supports check_mode, idempotency, and response parsing.
notes:
  - Stargate REST API uses POST for all endpoints at /adama/rest/{endpoint}
  - Data is passed as JSON body, not query parameters.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  endpoint:
    description:
      - API endpoint name (e.g., /userGet, /connectionGet).
      - Will be prefixed with /adama/rest/
    type: str
    required: true
  data:
    description:
      - JSON body data to send with the request.
    type: dict
    required: false
  return_content:
    description:
      - Key in response to extract (e.g., 'user', 'connection', 'alarm').
    type: str
    required: false
'''

EXAMPLES = r'''
# Get all users
- name: Fetch users
  company.stargate.stargate_get:
    server: "https://10.201.208.160:8443"
    token: "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
    endpoint: "/userGet"
    data:
      start: 0
      length: 5
  register: result

# Get connections
- name: Fetch connections
  company.stargate.stargate_get:
    server: "https://10.201.208.160:8443"
    token: "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
    endpoint: "/connectionGet"
    data:
      start: 0
      length: 10
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
        validate_certs=dict(type='bool', default=False),
        use_ssl=dict(type='bool', default=True),
        timeout=dict(type='int', default=30),
        endpoint=dict(type='str', required=True),
        data=dict(type='dict', required=False, default=None),
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
    data = module.params['data']
    timeout = module.params['timeout']

    try:
        if module.check_mode:
            result['msg'] = 'Check mode: would perform POST to /adama/rest{}'.format(endpoint)
            module.exit_json(**result)

        # Stargate expects /adama/rest/{endpoint}
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        api_endpoint = '/adama/rest{}'.format(endpoint)

        response, status_code = stargate_api_wrapper(
            module,
            'POST',
            api_endpoint,
            data=data,
            timeout=timeout
        )

        result['data'] = response
        result['status_code'] = status_code
        result['msg'] = 'Successfully retrieved data from {}'.format(api_endpoint)
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="POST request failed: {}".format(to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()