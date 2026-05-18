#!/usr/bin/python
# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: stargate_node
author:
  - Company Automation Team
version_added: "1.0.0"
short_description: Manage Stargate nodes
description:
  - Discover, register, and manage nodes in Stargate.
  - Supports node status queries, configuration updates, and maintenance mode.
notes:
  - Idempotent for status queries and configuration reads.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  node_id:
    description:
      - Unique node identifier.
      - Required for targeted operations on specific nodes.
    type: str
    required: false
  state:
    description:
      - Desired state of the node.
    type: str
    choices: [present, absent, maintenance]
    default: present
  name:
    description:
      - Human-readable node name.
    type: str
    required: false
  ip_address:
    description:
      - Node IP address.
    type: str
    required: false
  site:
    description:
      - Site or location identifier for the node.
    type: str
    required: false
  status:
    description:
      - Filter or set node operational status.
    type: str
    choices: [online, offline, maintenance, active]
    required: false
  labels:
    description:
      - Key-value labels/tags for the node.
    type: dict
    required: false
  filter_params:
    description:
      - Additional filter parameters for list operations.
    type: dict
    required: false
  discover:
    description:
      - Perform node discovery scan.
    type: bool
    default: false
'''

EXAMPLES = r'''
# List all nodes
- name: Get all nodes
  company.stargate.stargate_node:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
  register: nodes

# Get nodes by status
- name: Get online nodes
  company.stargate.stargate_node:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    status: online
  register: online_nodes

# Register a new node
- name: Register node
  company.stargate.stargate_node:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    name: "k3s-worker-01"
    ip_address: "192.168.1.151"
    site: "site1"
    labels:
      role: worker
      environment: production

# Set node to maintenance
- name: Enable maintenance mode
  company.stargate.stargate_node:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    node_id: "node-001"
    state: maintenance

# Update node labels
- name: Update node labels
  company.stargate.stargate_node:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    node_id: "node-001"
    labels:
      environment: staging
      version: "2.0"

# Discover new nodes
- name: Discover nodes on network
  company.stargate.stargate_node:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    discover: true
  register: discovered
'''

RETURN = r'''
nodes:
  description: List of node objects.
  type: list
  returned: when listing
node:
  description: Single node object.
  type: dict
  returned: when specific node_id
count:
  description: Number of nodes returned.
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


def get_nodes(module, endpoint, token, timeout):
    """Fetch list of nodes with optional filtering."""
    params = module.params.get('filter_params') or {}
    status = module.params.get('status')
    site = module.params.get('site')

    if status:
        params['status'] = status
    if site:
        params['site'] = site

    if params:
        param_str = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
        endpoint = '{}?{}'.format(endpoint, param_str)

    response, status_code = stargate_api_wrapper(
        module, 'GET', endpoint,
        headers={"Authorization": "Bearer {}".format(token)},
        timeout=timeout
    )
    return response


def build_node_data(module):
    """Build node data dict from module params."""
    data = {}
    for field in ['name', 'ip_address', 'site', 'status', 'labels']:
        val = module.params.get(field)
        if val is not None:
            data[field] = val
    return data


def run_module():
    module_args = dict(
        server=dict(type='str', required=True, aliases=['url']),
        token=dict(type='str', required=True, no_log=True),
        validate_certs=dict(type='bool', default=True),
        use_ssl=dict(type='bool', default=True),
        timeout=dict(type='int', default=30),
        api_version=dict(type='str', default='11.7.0'),
        node_id=dict(type='str', required=False),
        state=dict(type='str', default='present', choices=['present', 'absent', 'maintenance']),
        name=dict(type='str', required=False),
        ip_address=dict(type='str', required=False),
        site=dict(type='str', required=False),
        status=dict(type='str', required=False, choices=['online', 'offline', 'maintenance', 'active']),
        labels=dict(type='dict', required=False),
        filter_params=dict(type='dict', required=False),
        discover=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {
        'changed': False,
        'nodes': [],
        'node': None,
        'count': 0,
    }

    server = module.params['server']
    token = module.params['token']
    node_id = module.params['node_id']
    state = module.params['state']
    timeout = module.params['timeout']
    discover = module.params['discover']

    base_endpoint = "/api/nodes"

    try:
        if module.check_mode:
            result['msg'] = 'Check mode: node operation would proceed'
            module.exit_json(**result)

        if discover:
            response, status_code = stargate_api_wrapper(
                module, 'POST',
                "{}/discover".format(base_endpoint),
                data=build_node_data(module),
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['nodes'] = response if isinstance(response, list) else response.get('data', [response])
            result['count'] = len(result['nodes'])
            result['msg'] = 'Discovered {} nodes'.format(result['count'])
            module.exit_json(**result)

        if node_id:
            endpoint = "{}/{}".format(base_endpoint, node_id)
        else:
            endpoint = base_endpoint

        if state == 'absent' and node_id:
            response, status_code = stargate_api_wrapper(
                module, 'DELETE', endpoint,
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['msg'] = 'Node {} deleted'.format(node_id)
            module.exit_json(**result)

        elif state == 'maintenance' and node_id:
            response, status_code = stargate_api_wrapper(
                module, 'PUT', endpoint,
                data={'status': 'maintenance'},
                headers={"Authorization": "Bearer {}".(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['node'] = response
            result['msg'] = 'Node {} set to maintenance'.format(node_id)
            module.exit_json(**result)

        elif node_id:
            response, status_code = stargate_api_wrapper(
                module, 'GET', endpoint,
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['node'] = response
            result['count'] = 1
            result['msg'] = 'Retrieved node {}'.format(node_id)
            module.exit_json(**result)

        else:
            nodes_response = get_nodes(module, base_endpoint, token, timeout)
            node_list = nodes_response if isinstance(nodes_response, list) else nodes_response.get('data', nodes_response)
            result['nodes'] = node_list
            result['count'] = len(node_list) if node_list else 0
            result['msg'] = 'Retrieved {} nodes'.format(result['count'])
            module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="Node operation failed: {}".format(to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()