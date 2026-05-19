#!/usr/bin/python
# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: stargate_user
author:
  - Company Automation Team
version_added: "1.0.0"
short_description: Manage Stargate user operations via REST API
description:
  - Create, read, update, delete, and count users in Stargate REST API.
  - All operations use POST to /adama/rest/{endpoint}
notes:
  - Stargate REST API uses POST for all endpoints at /adama/rest/{endpoint}
  - Data is passed as JSON body, not query parameters.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  operation:
    description:
      - Operation to perform
    type: str
    required: true
    choices:
      - userGet
      - userCount
      - userCreate
      - userDelete
      - userUpdate
  user_data:
    description:
      - User data for create/update operations (JSON dict)
    type: dict
    required: false
  start:
    description:
      - Start index for pagination (userGet)
    type: int
    required: false
    default: 0
  length:
    description:
      - Number of records to return (userGet)
    type: int
    required: false
    default: 10
'''

EXAMPLES = r'''
# Get all users
- name: Fetch users
  company.stargate.stargate_user:
    server: "https://10.201.208.160:8443"
    token: "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
    operation: userGet
    start: 0
    length: 10
  register: result

# Count users
- name: Count all users
  company.stargate.stargate_user:
    server: "https://10.201.208.160:8443"
    token: "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
    operation: userCount
  register: result

# Create a user
- name: Create new user
  company.stargate.stargate_user:
    server: "https://10.201.208.160:8443"
    token: "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
    operation: userCreate
    user_data:
      name: "testuser"
      password: "SecurePass123"
      enabled: true
  register: result

# Update a user
- name: Update user
  company.stargate.stargate_user:
    server: "https://10.201.208.160:8443"
    token: "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
    operation: userUpdate
    user_data:
      id: 123
      name: "updateduser"
      enabled: false
  register: result

# Delete a user
- name: Delete user
  company.stargate.stargate_user:
    server: "https://10.201.208.160:8443"
    token: "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
    operation: userDelete
    user_data:
      id: 123
  register: result
'''

RETURN = r'''
user:
  description: User data from the API response
  type: dict or list
  returned: always
errorMsg:
  description: Error message from the API
  type: str
  returned: when error occurs
status_code:
  description: HTTP status code from the response
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
        operation=dict(type='str', required=True, choices=[
            'userGet', 'userCount', 'userCreate', 'userDelete', 'userUpdate'
        ]),
        user_data=dict(type='dict', required=False, default=None),
        start=dict(type='int', required=False, default=0),
        length=dict(type='int', required=False, default=10),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {
        'changed': False,
        'user': None,
        'errorMsg': None,
        'status_code': None,
    }

    operation = module.params['operation']
    user_data = module.params['user_data']
    start = module.params['start']
    length = module.params['length']

    try:
        if module.check_mode:
            result['msg'] = 'Check mode: would perform {} operation'.format(operation)
            module.exit_json(**result)

        # Build endpoint path
        endpoint = '/adama/rest/{}'.format(operation)

        # Build request data
        data = user_data.copy() if user_data else {}
        if operation == 'userGet':
            data['start'] = start
            data['length'] = length

        response, status_code = stargate_api_wrapper(
            module,
            'POST',
            endpoint,
            data=data,
            timeout=module.params['timeout']
        )

        # Extract user data from response
        if 'user' in response:
            result['user'] = response['user']
        else:
            result['user'] = response

        if 'errorMsg' in response:
            result['errorMsg'] = response['errorMsg']

        result['status_code'] = status_code
        result['msg'] = 'Successfully performed {} operation'.format(operation)

        # Operations that modify data are considered changes
        if operation in ('userCreate', 'userDelete', 'userUpdate'):
            result['changed'] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="{} operation failed: {}".format(operation, to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()