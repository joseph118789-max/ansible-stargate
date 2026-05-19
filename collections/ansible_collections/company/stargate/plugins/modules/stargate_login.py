#!/usr/bin/python
# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: stargate_login
author:
  - Company Automation Team
version_added: "1.0.0"
short_description: Authenticate with Stargate REST API
description:
  - Authenticates with Stargate/MasterSAM REST API using username:token Bearer auth.
  - The token is the API Secret from the MasterSAM API User configuration.
  - Auth format: base64(username:token) sent as Authorization: Bearer <b64>
notes:
  - Token is used directly as the API secret from Stargate API User configuration.
  - No separate login endpoint - authentication is done per-request with Bearer token.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  state:
    description:
      - C(present) returns the token in expected format.
      - C(absent) is a no-op for logout (Stargate uses stateless auth).
    type: str
    choices: [present, absent]
    default: present
  persist_token:
    description:
      - Whether to set the token as an Ansible fact for reuse in the same play.
    type: bool
    default: true
  token_name:
    description:
      - Name of the fact to store the token when persist_token is true.
    type: str
    default: stargate_token
'''

EXAMPLES = r'''
# Login with API user and secret
- name: Login to Stargate
  company.stargate.stargate_login:
    server: "https://YOUR_SERVER_IP:8443"
    username: "ansible"
    password: "YOUR_TOKEN"
  register: login_result

# Use token in subsequent calls
- name: Get users
  company.stargate.stargate_get:
    server: "https://YOUR_SERVER_IP:8443"
    token: "{{ login_result.token }}"
    endpoint: "/userGet"
    data:
      start: 0
      length: 5
'''

RETURN = r'''
token:
  description: The raw API token (username:token format, base64 encoded by stargate_utils).
  type: str
  returned: on successful login
username:
  description: The username used for authentication.
  type: str
  returned: on successful login
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native


def run_module():
    module_args = dict(
        server=dict(type='str', required=True, aliases=['url']),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        token=dict(type='str', required=False, no_log=True),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        validate_certs=dict(type='bool', default=False),
        use_ssl=dict(type='bool', default=True),
        timeout=dict(type='int', default=30),
        persist_token=dict(type='bool', default=True),
        token_name=dict(type='str', default='stargate_token'),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        required_if=[
            ('state', 'present', ['username', 'password']),
        ],
        supports_check_mode=True
    )

    result = {
        'changed': False,
        'token': None,
        'username': None,
    }

    if module.check_mode:
        module.exit_json(**result)

    username = module.params['username']
    password = module.params['password']  # This is the API token/secret
    persist_token = module.params['persist_token']
    token_name = module.params['token_name']

    # Stargate uses username:token as the auth credential
    # The raw token format is "username:token" - stargate_utils handles base64 encoding
    raw_token = "{}:{}".format(username, password)
    
    result['token'] = raw_token
    result['username'] = username
    result[token_name] = raw_token

    # Store in ansible_facts for reuse
    module.params['ansible_facts'] = {token_name: raw_token}

    result['msg'] = 'Token prepared for Stargate API (auth handled per-request)'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()