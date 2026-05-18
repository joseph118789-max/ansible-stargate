# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type

"""
Stargate REST API module_utils
Provides shared functions for Stargate API modules
"""

import json
import time
import urllib3
from ansible.module_utils.urls import fetch_url, urllib_error
from ansible.module_utils.six.moves.urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def stargate_api_wrapper(module, method, endpoint, data=None, headers=None, timeout=30, retries=3, retry_delay=5):
    """
    Generic wrapper for Stargate REST API calls with retry support.
    
    :param module: AnsibleModule instance
    :param method: HTTP method (GET, POST, PUT, DELETE)
    :param endpoint: API endpoint path
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
    api_version = module.params.get('api_version', '11.7.0')

    if not server:
        module.fail_json(msg="server parameter is required")

    # Build URL
    scheme = "https" if use_ssl else "http"
    base_url = server.rstrip('/')
    url = "{}{}".format(base_url, endpoint)

    # Default headers
    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-Version": api_version
    }

    # Add auth token if provided
    if token:
        default_headers["Authorization"] = "Bearer {}".format(token)

    # Merge provided headers
    if headers:
        default_headers.update(headers)

    # Prepare body
    body = json.dumps(data) if data is not None else None

    # Retry loop
    last_error = None
    for attempt in range(retries):
        try:
            response, info = fetch_url(
                module,
                url,
                method=method,
                data=body,
                headers=default_headers,
                timeout=timeout,
                validate_certs=validate_certs
            )

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

            # Token expired - attempt to re-authenticate
            if status_code == 401 and token and attempt < retries - 1:
                module.warn("Token expired, retrying authentication...")
                time.sleep(retry_delay)
                continue

            # Error codes
            error_msg = response_data.get('message', response_data.get('error', response_data.get('description', 'Unknown error')))
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


def stargate_login(module, server, username, password, validate_certs=True, timeout=30):
    """
    Authenticate with Stargate and return token.
    
    :param module: AnsibleModule instance
    :param server: Stargate server URL
    :param username: Username
    :param password: Password
    :param validate_certs: Validate SSL certs
    :param timeout: Request timeout
    :return: Token string
    """
    login_data = {
        "username": username,
        "password": password
    }
    
    endpoint = "/api/auth/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response, status = stargate_api_wrapper(
            module, "POST", endpoint, 
            data=login_data, 
            headers=headers,
            timeout=timeout,
            retries=1
        )
        
        # Extract token from response
        # Common token field names: token, sessionToken, accessToken, session_id
        token = (response.get('token') or 
                 response.get('sessionToken') or 
                 response.get('accessToken') or 
                 response.get('session_id') or
                 response.get('data', {}).get('token') or
                 response.get('data', {}).get('sessionToken'))
        
        if not token:
            module.fail_json(
                msg="No token found in login response. Response: {}".format(response),
                response=response
            )
        
        return token
        
    except Exception as e:
        module.fail_json(msg="Login failed: {}".format(str(e)))


def stargate_logout(module, server, token, validate_certs=True, timeout=30):
    """
    Logout from Stargate session.
    
    :param module: AnsibleModule instance
    :param server: Stargate server URL
    :param token: Session token
    :param validate_certs: Validate SSL certs
    :param timeout: Request timeout
    :return: Logout response
    """
    endpoint = "/api/auth/logout"
    
    try:
        response, status = stargate_api_wrapper(
            module, "POST", endpoint,
            headers={"Authorization": "Bearer {}".format(token)},
            timeout=timeout,
            retries=1
        )
        return response, status
    except Exception as e:
        # Logout failures are non-critical
        module.warn("Logout failed: {}".format(str(e)))
        return {'message': 'Logout attempted'}, 0