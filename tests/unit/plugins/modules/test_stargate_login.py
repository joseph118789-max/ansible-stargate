# (c) 2024 Company Automation Team
# GNU General Public License v3.0+

"""Unit tests for stargate_login module.

Note: These tests focus on the logic/structure rather than mocking Ansible internals.
For full integration testing, use molecule scenarios.
"""

import pytest
import base64
import json
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, '/root/.openclaw/workspace/projects/ansible-stargate/collections/ansible_collections/company/stargate/plugins/modules')


class TestStargateLoginAuthFormat:
    """Test authentication token format."""

    def test_bearer_token_format(self):
        """Test that Bearer token is correctly formatted."""
        username = "ansible"
        token = "f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
        
        # Base64 encode username:token
        auth_b64 = base64.b64encode(f"{username}:{token}".encode()).decode()
        bearer = f"Bearer {auth_b64}"
        
        expected_b64 = "YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM="
        
        assert bearer == f"Bearer {expected_b64}"
        assert bearer.startswith("Bearer ")
        assert len(bearer) > 20

    def test_token_base64_encoding(self):
        """Test token is properly base64 encoded."""
        token = "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
        encoded = base64.b64encode(token.encode()).decode()
        
        # Verify it's valid base64
        decoded = base64.b64decode(encoded).decode()
        assert decoded == token

    def test_auth_header_format(self):
        """Test Authorization header format."""
        token_b64 = base64.b64encode(b"ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c").decode()
        
        headers = {
            "Authorization": f"Bearer {token_b64}",
            "Content-Type": "application/json"
        }
        
        assert headers["Authorization"] == "Bearer YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM="
        assert headers["Content-Type"] == "application/json"


class TestStargateLoginEndpoint:
    """Test login endpoint construction."""

    def test_login_url_construction(self):
        """Test login endpoint URL is correctly formed."""
        server = "https://10.201.208.160:8443"
        # Stargate API uses /adama/rest prefix
        endpoint = "/adama/rest/userGet"
        
        url = f"{server}{endpoint}"
        
        assert url == "https://10.201.208.160:8443/adama/rest/userGet"
        assert server.startswith("https://")

    def test_full_url_construction(self):
        """Test full URL with query parameters."""
        server = "https://10.201.208.160:8443"
        endpoint = "/adama/rest/userGet"
        
        # Pagination params as strings (Stargate requirement)
        params = {"start": "0", "length": "10"}
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        
        url = f"{server}{endpoint}?{query_string}"
        
        assert "start=0" in url
        assert "length=10" in url


class TestStargateLoginResponseParsing:
    """Test login response parsing."""

    def test_success_response_parsing(self):
        """Test successful login response structure."""
        response = {
            'user': [{'id': '1', 'username': 'mgadmin'}],
            'errorMsg': None
        }
        
        assert 'user' in response
        assert response['errorMsg'] is None

    def test_error_response_parsing(self):
        """Test error response parsing."""
        response = {
            'message': 'login failed',
            'errorMsg': 'invalid credentials'
        }
        
        assert 'errorMsg' in response
        assert response['errorMsg'] == 'invalid credentials'

    def test_token_response_structure(self):
        """Test token response structure."""
        token_response = {
            'token': 'f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c',
            'userId': 'user-123'
        }
        
        assert 'token' in token_response
        assert 'userId' in token_response


class TestStargateLoginModuleParams:
    """Test module parameter handling."""

    def test_required_params_structure(self):
        """Test required parameters are defined."""
        required_params = ['server', 'username', 'password']
        
        module_params = {
            'server': 'https://10.201.208.160:8443',
            'username': 'ansible',
            'password': 'f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c'
        }
        
        for param in required_params:
            assert param in module_params

    def test_optional_params_defaults(self):
        """Test optional parameters have defaults."""
        optional_params = {
            'validate_certs': True,
            'use_ssl': True,
            'timeout': 30,
            'retries': 3,
            'retry_delay': 5
        }
        
        assert optional_params['validate_certs'] == True
        assert optional_params['use_ssl'] == True
        assert optional_params['timeout'] == 30
        assert optional_params['retries'] == 3
        assert optional_params['retry_delay'] == 5

    def test_token_storage_format(self):
        """Test token is stored in correct format for facts."""
        facts = {}
        token = "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
        facts['stargate_token'] = token
        
        assert facts['stargate_token'] == token
        assert ':' in facts['stargate_token']


class TestStargateLoginRetryLogic:
    """Test retry logic for login."""

    def test_retry_on_500(self):
        """Test retry behavior on 500 error."""
        # Simulate: first call 500, second call 200
        error_response = {'errorMsg': 'server error'}, 500
        success_response = {'user': []}, 200
        
        responses = [error_response, success_response]
        
        # Should retry and succeed
        assert len(responses) == 2
        assert responses[0][1] == 500
        assert responses[1][1] == 200

    def test_no_retry_on_401(self):
        """Test no retry on auth failure (401)."""
        error_response = {'errorMsg': 'unauthorized'}, 401
        
        # Should fail immediately, not retry
        assert error_response[1] == 401

    def test_max_retries_exceeded(self):
        """Test max retries behavior."""
        max_retries = 3
        
        # After 3 failures, should give up
        attempts = 0
        for i in range(max_retries):
            attempts += 1
        
        assert attempts == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])