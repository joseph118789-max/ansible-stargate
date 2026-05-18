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
  - Authenticates with Stargate/MasterSAM REST API and returns a session token.
  - Supports username/password authentication with token storage for reuse.
notes:
  - Use M(stargate_logout) to properly terminate the session when done.
requirements:
  - python >= 3.8
  - requests
extends_documentation_fragment:
  - company.stargate.stargate
options:
  state:
    description:
      - C(present) will authenticate and return token.
      - C(absent) will logout the session.
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
# Login and store token for subsequent tasks
- name: Login to Stargate
  company.stargate.stargate_login:
    server: "https://pms.tony.lab.ctc-g.com.my:9443"
    username: "admin"
    password: "password"
  register: login_result

- name: Print token
  ansible.builtin.debug:
    msg: "Token is {{ login_result.token }}"

# Logout at end of play
- name: Logout from Stargate
  company.stargate.stargate_logout:
    server: "https://pms.tony.lab.ctc-g.com.my:9443"
    token: "{{ login_result.token }}"
'''

RETURN = r'''
token:
  description: The session token returned by Stargate.
  type: str
  returned: on successful login
expires:
  description: Token expiration time if available.
  type: str
  returned: when available
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

try:
    from ..module_utils.stargate_utils import stargate_login as api_login
    from ..module_utils.stargate_utils import stargate_logout as api_logout
except ImportError:
    from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login as api_login
    from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_logout as api_logout


def run_module():
    module_args = dict(
        server=dict(type='str', required=True, aliases=['url']),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        token=dict(type='str', required=False, no_log=True),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        validate_certs=dict(type='bool', default=True),
        use_ssl=dict(type='bool', default=True),
        timeout=dict(type='int', default=30),
        api_version=dict(type='str', default='11.7.0'),
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
    }

    if module.check_mode:
        module.exit_json(**result)

    server = module.params['server']
    state = module.params['state']
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    persist_token = module.params['persist_token']
    token_name = module.params['token_name']
    timeout = module.params['timeout']
    validate_certs = module.params['validate_certs']

    try:
        if state == 'present':
            # If no token provided, perform login
            if not token and username and password:
                module.debug("Authenticating with username/password")
                token = api_login(
                    module,
                    server,
                    username,
                    password,
                    validate_certs=validate_certs,
                    timeout=timeout
                )
                result['changed'] = True

            result['token'] = token
            result[token_name] = token

            # Store in ansible_facts for reuse
            module.params['ansible_facts'] = {token_name: token}

            result['msg'] = 'Successfully authenticated with Stargate'
            module.exit_json(**result)

        elif state == 'absent':
            if not token:
                module.fail_json(msg="token is required for logout")

            api_logout(module, server, token, validate_certs=validate_certs, timeout=timeout)
            result['changed'] = True
            result['msg'] = 'Successfully logged out from Stargate'
            module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="Login/logout failed: {}".format(to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()