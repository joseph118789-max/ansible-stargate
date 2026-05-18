# Copyright (c) 2024 Company Automation Team
# GNU General Public License v3.0+

"""
Unit tests for stargate_utils module
"""

import json
import pytest
from unittest.mock import MagicMock, patch


class MockResponse:
    """Mock response object for fetch_url"""

    def __init__(self, body, status=200):
        self._body = body
        self.status = status

    def read(self):
        return self._body.encode('utf-8')


class MockInfo:
    """Mock info dict for fetch_url"""

    def __init__(self, status=200, msg='OK'):
        self._data = {'status': status, 'msg': msg}

    def get(self, key, default=None):
        return self._data.get(key, default)


def make_mock_response(body, status=200):
    """Factory to create mock response tuple (response, info)"""
    return MockResponse(body, status), MockInfo(status)


class TestStargateLogin:
    """Tests for stargate_login function"""

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_login_success_token_field(self, mock_api_wrapper):
        """Test successful login when token is in 'token' field"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.return_value = (
            {'token': 'abc123xyz'}, 200
        )

        result = stargate_login(module, 'https://stargate.example.com', 'admin', 'password')

        assert result == 'abc123xyz'
        mock_api_wrapper.assert_called_once()
        call_kwargs = mock_api_wrapper.call_args[1]
        assert call_kwargs['method'] == 'POST'
        assert call_kwargs['data']['username'] == 'admin'

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_login_success_session_token_field(self, mock_api_wrapper):
        """Test successful login when token is in 'sessionToken' field"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.return_value = (
            {'sessionToken': 'session-token-abc'}, 200
        )

        result = stargate_login(module, 'https://stargate.example.com', 'admin', 'password')

        assert result == 'session-token-abc'

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_login_success_access_token_field(self, mock_api_wrapper):
        """Test successful login when token is in 'accessToken' field"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.return_value = (
            {'accessToken': 'access-token-xyz'}, 200
        )

        result = stargate_login(module, 'https://stargate.example.com', 'admin', 'password')

        assert result == 'access-token-xyz'

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_login_success_session_id_field(self, mock_api_wrapper):
        """Test successful login when token is in 'session_id' field"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.return_value = (
            {'session_id': 'session-id-123'}, 200
        )

        result = stargate_login(module, 'https://stargate.example.com', 'admin', 'password')

        assert result == 'session-id-123'

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_login_success_token_in_data_field(self, mock_api_wrapper):
        """Test successful login when token is nested in 'data' object"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.return_value = (
            {'data': {'token': 'nested-token-456'}}, 200
        )

        result = stargate_login(module, 'https://stargate.example.com', 'admin', 'password')

        assert result == 'nested-token-456'

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_login_success_session_token_in_data_field(self, mock_api_wrapper):
        """Test successful login when sessionToken is nested in 'data' object"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.return_value = (
            {'data': {'sessionToken': 'nested-session-token'}}, 200
        )

        result = stargate_login(module, 'https://stargate.example.com', 'admin', 'password')

        assert result == 'nested-session-token'

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_login_failure_no_token(self, mock_api_wrapper):
        """Test login failure when no token is found in response"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.return_value = (
            {'message': 'Authentication failed'}, 200
        )

        with pytest.raises(SystemExit):
            stargate_login(module, 'https://stargate.example.com', 'admin', 'wrongpassword')

        module.fail_json.assert_called_once()
        call_msg = module.fail_json.call_args[1]['msg']
        assert 'No token found' in call_msg

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_login_exception(self, mock_api_wrapper):
        """Test login when API wrapper raises an exception"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.side_effect = Exception('Network error')

        with pytest.raises(SystemExit):
            stargate_login(module, 'https://stargate.example.com', 'admin', 'password')

        module.fail_json.assert_called_once()
        call_msg = module.fail_json.call_args[1]['msg']
        assert 'Login failed' in call_msg


class TestStargateLogout:
    """Tests for stargate_logout function"""

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_logout_success(self, mock_api_wrapper):
        """Test successful logout"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_logout

        module = MagicMock()
        module.params = {}
        module.warn = MagicMock()

        mock_api_wrapper.return_value = (
            {'message': 'Logged out successfully'}, 200
        )

        response, status = stargate_logout(module, 'https://stargate.example.com', 'token-abc')

        assert status == 200
        assert response['message'] == 'Logged out successfully'
        mock_api_wrapper.assert_called_once()
        call_kwargs = mock_api_wrapper.call_args[1]
        assert call_kwargs['method'] == 'POST'
        assert 'Bearer token-abc' in call_kwargs['headers']['Authorization']

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_logout_failure_non_critical(self, mock_api_wrapper):
        """Test logout failure is non-critical and returns warning"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_logout

        module = MagicMock()
        module.params = {}
        module.warn = MagicMock()

        mock_api_wrapper.side_effect = Exception('Connection refused')

        response, status = stargate_logout(module, 'https://stargate.example.com', 'token-abc')

        assert status == 0
        assert response['message'] == 'Logout attempted'
        module.warn.assert_called_once()
        warn_msg = module.warn.call_args[0][0]
        assert 'Logout failed' in warn_msg


class TestStargateApiWrapper:
    """Tests for stargate_api_wrapper function"""

    def test_missing_server_param(self):
        """Test failure when server parameter is missing"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {'server': None}
        module.fail_json = MagicMock(side_effect=SystemExit)

        with pytest.raises(SystemExit):
            stargate_api_wrapper(module, 'GET', '/api/status')

        module.fail_json.assert_called_once()
        call_msg = module.fail_json.call_args[1]['msg']
        assert 'server parameter is required' in call_msg

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.fetch_url')
    def test_successful_get_request(self, mock_fetch_url):
        """Test successful GET request"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {
            'server': 'https://stargate.example.com',
            'token': 'test-token',
            'validate_certs': True,
            'use_ssl': True,
            'api_version': '11.7.0'
        }
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_response = MockResponse('{"status": "healthy", "version": "11.7.0"}')
        mock_fetch_url.return_value = (mock_response, MockInfo(200))

        result, status = stargate_api_wrapper(module, 'GET', '/api/status')

        assert status == 200
        assert result['status'] == 'healthy'
        mock_fetch_url.assert_called_once()
        call_kwargs = mock_fetch_url.call_args[1]
        assert call_kwargs['method'] == 'GET'
        assert call_kwargs['url'] == 'https://stargate.example.com/api/status'

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.fetch_url')
    def test_successful_post_request(self, mock_fetch_url):
        """Test successful POST request"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {
            'server': 'https://stargate.example.com',
            'token': 'test-token',
            'validate_certs': True,
            'use_ssl': True,
            'api_version': '11.7.0'
        }
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_response = MockResponse('{"id": "123", "name": "test-service"}')
        mock_fetch_url.return_value = (mock_response, MockInfo(201))

        result, status = stargate_api_wrapper(
            module, 'POST', '/api/services',
            data={'name': 'test-service'}
        )

        assert status == 201
        assert result['id'] == '123'
        call_kwargs = mock_fetch_url.call_args[1]
        assert call_kwargs['method'] == 'POST'
        assert '"name": "test-service"' in call_kwargs['data']

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.fetch_url')
    def test_http_500_error(self, mock_fetch_url):
        """Test handling of HTTP 500 server error"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {
            'server': 'https://stargate.example.com',
            'token': 'test-token',
            'validate_certs': True,
            'use_ssl': True,
            'api_version': '11.7.0'
        }
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_response = MockResponse('{"error": "Internal server error", "message": "Database connection failed"}')
        mock_fetch_url.return_value = (mock_response, MockInfo(500))

        with pytest.raises(SystemExit):
            stargate_api_wrapper(module, 'GET', '/api/services')

        module.fail_json.assert_called_once()
        call_kwargs = module.fail_json.call_args[1]
        assert call_kwargs['status_code'] == 500
        assert 'Internal server error' in call_kwargs['msg']

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.fetch_url')
    def test_http_401_with_retry(self, mock_fetch_url):
        """Test retry on 401 Unauthorized when token is provided"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {
            'server': 'https://stargate.example.com',
            'token': 'expired-token',
            'validate_certs': True,
            'use_ssl': True,
            'api_version': '11.7.0'
        }
        module.fail_json = MagicMock(side_effect=SystemExit)
        module.warn = MagicMock()

        mock_response = MockResponse('{"error": "Unauthorized"}')
        mock_fetch_url.return_value = (mock_response, MockInfo(401))

        with pytest.raises(SystemExit):
            stargate_api_wrapper(module, 'GET', '/api/status', retries=3, retry_delay=0)

        module.warn.assert_called()
        assert mock_fetch_url.call_count >= 1

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.fetch_url')
    def test_connection_error_with_retry(self, mock_fetch_url):
        """Test retry on connection errors"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {
            'server': 'https://stargate.example.com',
            'token': 'test-token',
            'validate_certs': True,
            'use_ssl': True,
            'api_version': '11.7.0'
        }
        module.fail_json = MagicMock(side_effect=SystemExit)

        # Simulate connection failure (None response)
        mock_fetch_url.return_value = (None, MockInfo(0, 'Connection refused'))

        with pytest.raises(SystemExit):
            stargate_api_wrapper(module, 'GET', '/api/status', retries=3, retry_delay=0)

        # Should have retried retries times
        assert mock_fetch_url.call_count == 3

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.fetch_url')
    def test_custom_headers(self, mock_fetch_url):
        """Test that custom headers are merged with defaults"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {
            'server': 'https://stargate.example.com',
            'token': 'test-token',
            'validate_certs': True,
            'use_ssl': True,
            'api_version': '11.7.0'
        }
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_response = MockResponse('{"result": "ok"}')
        mock_fetch_url.return_value = (mock_response, MockInfo(200))

        stargate_api_wrapper(
            module, 'GET', '/api/custom',
            headers={'X-Custom-Header': 'custom-value', 'Accept': 'application/xml'}
        )

        call_kwargs = mock_fetch_url.call_args[1]
        headers = call_kwargs['headers']
        assert headers['X-Custom-Header'] == 'custom-value'
        # Accept should be overridden by custom header
        assert headers['Accept'] == 'application/xml'
        # But standard headers should still be present
        assert headers['Content-Type'] == 'application/json'
        assert headers['X-API-Version'] == '11.7.0'
        assert 'Bearer test-token' in headers['Authorization']

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.fetch_url')
    def test_http_204_no_content(self, mock_fetch_url):
        """Test handling of HTTP 204 No Content response"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {
            'server': 'https://stargate.example.com',
            'token': 'test-token',
            'validate_certs': True,
            'use_ssl': True,
            'api_version': '11.7.0'
        }
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_response = MockResponse('', 204)
        mock_fetch_url.return_value = (mock_response, MockInfo(204))

        result, status = stargate_api_wrapper(module, 'DELETE', '/api/resource/123')

        assert status == 204
        assert result == {}

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.fetch_url')
    def test_non_json_response(self, mock_fetch_url):
        """Test handling of non-JSON response"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_api_wrapper

        module = MagicMock()
        module.params = {
            'server': 'https://stargate.example.com',
            'token': 'test-token',
            'validate_certs': True,
            'use_ssl': True,
            'api_version': '11.7.0'
        }
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_response = MockResponse('Plain text response')
        mock_fetch_url.return_value = (mock_response, MockInfo(200))

        result, status = stargate_api_wrapper(module, 'GET', '/api/status')

        assert status == 200
        assert result['raw'] == 'Plain text response'


class TestTokenExtraction:
    """Tests for token extraction from various response formats"""

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_token_at_root_level(self, mock_api_wrapper):
        """Test token extraction when token is at root level of response"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        responses = [
            {'token': 'root-token-1'},
            {'sessionToken': 'root-token-2'},
            {'accessToken': 'root-token-3'},
            {'session_id': 'root-token-4'},
        ]

        for response in responses:
            mock_api_wrapper.return_value = (response, 200)
            result = stargate_login(module, 'https://stargate.example.com', 'user', 'pass')
            assert result.startswith('root-token')

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_token_in_data_object(self, mock_api_wrapper):
        """Test token extraction when token is inside 'data' object"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        responses = [
            {'data': {'token': 'data-token-1'}},
            {'data': {'sessionToken': 'data-token-2'}},
        ]

        for response in responses:
            mock_api_wrapper.return_value = (response, 200)
            result = stargate_login(module, 'https://stargate.example.com', 'user', 'pass')
            assert result.startswith('data-token')

    @patch('ansible_collections.company.stargate.plugins.module_utils.stargate_utils.stargate_api_wrapper')
    def test_token_priority(self, mock_api_wrapper):
        """Test that token field takes priority over other fields"""
        from ansible_collections.company.stargate.plugins.module_utils.stargate_utils import stargate_login

        module = MagicMock()
        module.params = {}
        module.fail_json = MagicMock(side_effect=SystemExit)

        mock_api_wrapper.return_value = (
            {
                'token': 'primary-token',
                'sessionToken': 'secondary-token',
                'accessToken': 'tertiary-token',
                'session_id': 'quaternary-token',
            },
            200
        )

        result = stargate_login(module, 'https://stargate.example.com', 'user', 'pass')
        assert result == 'primary-token'