# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type

"""
Stargate REST API module_utils
Provides shared functions for Stargate API modules
"""

import base64
import json
import ssl
import time
import urllib3
from ansible.module_utils.urls import fetch_url, urllib_error
from ansible.module_utils.six.moves.urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def stargate_api_wrapper(module, method, endpoint, data=None, headers=None, timeout=30, retries=3, retry_delay=5):
    """
    Generic wrapper for Stargate REST API calls with retry support.
    
    Auth format: base64(username:token) as Bearer token
    
    :param module: AnsibleModule instance
    :param method: HTTP method (GET, POST, PUT, DELETE)
    :param endpoint: API endpoint path (e.g., /userGet)
    :param data: Request body (dict, will be JSON serialized)
    :param headers: Additional headers
    :param timeout: Request timeout in seconds
    :param retries: Number of retries on failure
    :param retry_delay: Delay between retries in seconds
    :return: (response_data, status_code)
    """
    server = module.params.get('server')
    token = module.params.get('token')
    validate_certs = module.params.get('validate_certs', True)
    use_ssl = module.params.get('use_ssl', True)

    if not server:
        module.fail_json(msg="server parameter is required")

    # Build URL - Stargate uses /adama/rest/{endpoint}
    scheme = "https" if use_ssl else "http"
    base_url = server.rstrip('/')
    url = "{}{}".format(base_url, endpoint)

    # Default headers
    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Add auth token - format: base64(username:token)
    if token:
        auth_b64 = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        default_headers["Authorization"] = "Bearer {}".format(auth_b64)

    # Merge provided headers
    if headers:
        default_headers.update(headers)

    # Prepare body
    body = json.dumps(data) if data is not None else None

    # Retry loop
    last_error = None
    for attempt in range(retries):
        try:
            # Build fetch_url kwargs (validate_certs not supported in Ansible 2.14+)
            fetch_kwargs = {
                'module': module,
                'url': url,
                'method': method,
                'data': body,
                'headers': default_headers,
                'timeout': timeout,
            }
            
            # Handle SSL verification - create unverified context if needed
            if not validate_certs:
                # Use ca_path=None with force=True to disable SSL verification
                fetch_kwargs['force'] = True
                fetch_kwargs['ca_path'] = None
            
            response, info = fetch_url(**fetch_kwargs)

            if response is None:
                # Connection error - retry
                last_error = "HTTP Timeout/Connection error: {}".format(info.get('msg', 'Unknown'))
                if attempt < retries - 1:
                    time.sleep(retry_delay)
                    continue
                module.fail_json(msg="Failed to connect to Stargate API: {}".format(last_error))

            status_code = info.get('status', 0)
            response_body = response.read().decode('utf-8')

            # Handle JSON response
            try:
                response_data = json.loads(response_body) if response_body else {}
            except ValueError:
                response_data = {'raw': response_body}

            # Success codes (including 4xx for non-critical responses)
            if status_code in (200, 201, 204):
                return response_data, status_code

            # Error codes
            error_msg = response_data.get('message', response_data.get('errorMsg', response_data.get('error', response_data.get('description', 'Unknown error'))))
            module.fail_json(
                msg="Stargate API error (HTTP {}): {}".format(status_code, error_msg),
                status_code=status_code,
                response=response_data
            )

        except urllib_error.URLError as e:
            last_error = str(e)
            if attempt < retries - 1:
                time.sleep(retry_delay)
                continue
            module.fail_json(msg="URL error: {}".format(last_error))
        except Exception as e:
            last_error = str(e)
            if attempt < retries - 1:
                time.sleep(retry_delay)
                continue
            module.fail_json(msg="Unexpected error: {}".format(last_error))

    module.fail_json(msg="Failed after {} retries. Last error: {}".format(retries, last_error))