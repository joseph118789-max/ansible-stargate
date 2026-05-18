# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type

class ModuleDocFragment:
    DOCUMENTATION = r'''
options:
  server:
    description:
      - Stargate/MasterSAM server URL
    required: true
    type: str
    aliases:
      - url
  username:
    description:
      - Username for authentication
    type: str
  password:
    description:
      - Password for authentication
    type: str
    no_log: true
  token:
    description:
      - Bearer token for API authentication
      - If not provided, module will attempt to authenticate using username/password
    type: str
    no_log: true
  validate_certs:
    description:
      - Whether to validate SSL certificates
    type: bool
    default: true
  use_ssl:
    description:
      - Whether to use HTTPS
    type: bool
    default: true
  timeout:
    description:
      - Timeout in seconds for API requests
    type: int
    default: 30
  api_version:
    description:
      - Stargate API version
    type: str
    default: "11.7.0"
'''