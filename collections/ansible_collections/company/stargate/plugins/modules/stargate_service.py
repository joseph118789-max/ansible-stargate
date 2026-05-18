#!/usr/bin/python
# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: stargate_service
author:
  - Company Automation Team
version_added: "1.0.0"
short_description: Manage Stargate services
description:
  - Create, read, update, delete, start, stop, and restart services in Stargate.
  - Supports service discovery and configuration management.
notes:
  - This is an idempotent module for status queries and configuration reads.
requirements:
  - python >= 3.8
extends_documentation_fragment:
  - company.stargate.stargate
options:
  service_id:
    description:
      - Unique service identifier.
      - Required for targeted operations on specific services.
    type: str
    required: false
  state:
    description:
      - Desired state of the service.
    type: str
    choices: [present, absent, started, stopped, restarted]
    default: present
  name:
    description:
      - Human-readable service name.
    type: str
    required: false
  service_type:
    description:
      - Type of service (e.g., http, tcp, mysql, redis).
    type: str
    required: false
  port:
    description:
      - Service port number.
    type: int
    required: false
  host:
    description:
      - Host where service runs or is assigned.
    type: str
    required: false
  node_id:
    description:
      - Node identifier where service is deployed.
    type: str
    required: false
  config:
    description:
      - Service configuration as key-value pairs.
    type: dict
    required: false
  filter_params:
    description:
      - Additional filter parameters for list operations.
    type: dict
    required: false
  start:
    description:
      - Start the service.
    type: bool
    default: false
  stop:
    description:
      - Stop the service.
    type: bool
    default: false
  restart:
    description:
      - Restart the service.
    type: bool
    default: false
'''

EXAMPLES = r'''
# List all services
- name: Get all services
  company.stargate.stargate_service:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
  register: services

# Get services by status
- name: Get running services
  company.stargate.stargate_service:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    status: running
  register: running_services

# Get specific service
- name: Get service details
  company.stargate.stargate_service:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    service_id: "svc-001"
  register: service

# Create a new service
- name: Create service
  company.stargate.stargate_service:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    name: "nginx-web"
    service_type: http
    port: 8080
    host: "192.168.1.100"
    node_id: "node-001"
    config:
      max_connections: 1000
      timeout: 60

# Start a service
- name: Start service
  company.stargate.stargate_service:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    service_id: "svc-001"
    start: true

# Restart a service
- name: Restart service
  company.stargate.stargate_service:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    service_id: "svc-001"
    restart: true

# Delete a service
- name: Delete service
  company.stargate.stargate_service:
    server: "https://pms.example.com:9443"
    token: "{{ stargate_token }}"
    service_id: "svc-001"
    state: absent
'''

RETURN = r'''
services:
  description: List of service objects.
  type: list
  returned: when listing
service:
  description: Single service object.
  type: dict
  returned: when specific service_id
count:
  description: Number of services returned.
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


def get_services(module, endpoint, token, timeout):
    """Fetch list of services with optional filtering."""
    params = module.params.get('filter_params') or {}
    status = module.params.get('status')
    service_type = module.params.get('service_type')

    if status:
        params['status'] = status
    if service_type:
        params['type'] = service_type

    if params:
        param_str = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
        endpoint = '{}?{}'.format(endpoint, param_str)

    response, status_code = stargate_api_wrapper(
        module, 'GET', endpoint,
        headers={"Authorization": "Bearer {}".format(token)},
        timeout=timeout
    )
    return response


def build_service_data(module):
    """Build service data dict from module params."""
    data = {}
    for field in ['name', 'service_type', 'port', 'host', 'node_id', 'config']:
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
        service_id=dict(type='str', required=False),
        state=dict(type='str', default='present', choices=['present', 'absent', 'started', 'stopped', 'restarted']),
        name=dict(type='str', required=False),
        service_type=dict(type='str', required=False),
        port=dict(type='int', required=False),
        host=dict(type='str', required=False),
        node_id=dict(type='str', required=False),
        config=dict(type='dict', required=False),
        filter_params=dict(type='dict', required=False),
        status=dict(type='str', required=False),
        start=dict(type='bool', default=False),
        stop=dict(type='bool', default=False),
        restart=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {
        'changed': False,
        'services': [],
        'service': None,
        'count': 0,
    }

    server = module.params['server']
    token = module.params['token']
    service_id = module.params['service_id']
    state = module.params['state']
    timeout = module.params['timeout']
    start = module.params['start']
    stop = module.params['stop']
    restart = module.params['restart']

    base_endpoint = "/adama/rest/serviceStatusGet"

    try:
        if module.check_mode:
            result['msg'] = 'Check mode: service operation would proceed'
            module.exit_json(**result)

        if service_id:
            endpoint = "{}/{}".format(base_endpoint, service_id)
        else:
            endpoint = base_endpoint

        if state == 'absent' and service_id:
            response, status_code = stargate_api_wrapper(
                module, 'DELETE', endpoint,
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['msg'] = 'Service {} deleted'.format(service_id)
            module.exit_json(**result)

        elif restart and service_id:
            response, status_code = stargate_api_wrapper(
                module, 'POST',
                "{}/restart".format(endpoint),
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['service'] = response
            result['msg'] = 'Service {} restarted'.format(service_id)
            module.exit_json(**result)

        elif start and service_id:
            response, status_code = stargate_api_wrapper(
                module, 'POST',
                "{}/start".format(endpoint),
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['service'] = response
            result['msg'] = 'Service {} started'.format(service_id)
            module.exit_json(**result)

        elif stop and service_id:
            response, status_code = stargate_api_wrapper(
                module, 'POST',
                "{}/stop".format(endpoint),
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['changed'] = True
            result['service'] = response
            result['msg'] = 'Service {} stopped'.format(service_id)
            module.exit_json(**result)

        elif service_id:
            response, status_code = stargate_api_wrapper(
                module, 'GET', endpoint,
                headers={"Authorization": "Bearer {}".format(token)},
                timeout=timeout
            )
            result['service'] = response
            result['count'] = 1
            result['msg'] = 'Retrieved service {}'.format(service_id)
            module.exit_json(**result)

        else:
            services_response = get_services(module, base_endpoint, token, timeout)
            service_list = services_response if isinstance(services_response, list) else services_response.get('data', services_response)
            result['services'] = service_list
            result['count'] = len(service_list) if service_list else 0
            result['msg'] = 'Retrieved {} services'.format(result['count'])
            module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg="Service operation failed: {}".format(to_native(e)))


def main():
    run_module()


if __name__ == '__main__':
    main()