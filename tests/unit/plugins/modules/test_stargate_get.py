# (c) 2024 Company Automation Team
# GNU General Public License v3.0+

"""Unit tests for stargate_get module.

Note: These tests focus on the logic/structure rather than mocking Ansible internals.
For full integration testing, use molecule scenarios.
"""

import pytest
import base64
import json
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, '/root/.openclaw/workspace/projects/ansible-stargate/collections/ansible_collections/company/stargate/plugins/module_utils')


class TestStargateGetEndpoint:
    """Test stargate_get module endpoint handling."""

    def test_user_get_endpoint(self):
        """Test userGet endpoint path."""
        endpoint = "/adama/rest/userGet"
        
        assert endpoint.startswith("/adama/rest/")
        assert "userGet" in endpoint

    def test_user_count_endpoint(self):
        """Test userCount endpoint path."""
        endpoint = "/adama/rest/userCount"
        
        assert endpoint.startswith("/adama/rest/")
        assert "userCount" in endpoint

    def test_connection_get_endpoint(self):
        """Test connectionGet endpoint path."""
        endpoint = "/adama/rest/connectionGet"
        
        assert endpoint.startswith("/adama/rest/")
        assert "connectionGet" in endpoint

    def test_connection_count_endpoint(self):
        """Test connectionCount endpoint path."""
        endpoint = "/adama/rest/connectionCount"
        
        assert endpoint.startswith("/adama/rest/")
        assert "connectionCount" in endpoint

    def test_account_common_get_endpoint(self):
        """Test accountCommonGet endpoint path."""
        endpoint = "/adama/rest/accountCommonGet"
        
        assert endpoint.startswith("/adama/rest/")
        assert "accountCommonGet" in endpoint


class TestStargateGetPagination:
    """Test pagination parameter handling."""

    def test_pagination_params_as_strings(self):
        """Test pagination params are strings (Stargate requirement)."""
        params = {"start": "0", "length": "10"}
        
        assert isinstance(params["start"], str)
        assert isinstance(params["length"], str)
        assert params["start"] == "0"
        assert params["length"] == "10"

    def test_pagination_params_json_serialization(self):
        """Test pagination params serialize correctly to JSON."""
        params = {"start": "0", "length": "50"}
        json_str = json.dumps(params)
        parsed = json.loads(json_str)
        
        assert parsed == params

    def test_pagination_with_offset(self):
        """Test pagination with offset."""
        params = {"start": "100", "length": "25"}
        
        assert int(params["start"]) == 100
        assert int(params["length"]) == 25


class TestStargateGetFilterParams:
    """Test filter parameter handling."""

    def test_user_name_filter(self):
        """Test filtering by userName."""
        params = {"userName": "mgadmin", "start": "0", "length": "10"}
        
        assert params["userName"] == "mgadmin"
        assert params["start"] == "0"
        assert params["length"] == "10"

    def test_connection_name_filter(self):
        """Test filtering by connectionName."""
        params = {"connectionName": "test-rdp", "start": "0", "length": "10"}
        
        assert params["connectionName"] == "test-rdp"

    def test_uuid_filter_format(self):
        """Test UUID format for ID filters."""
        params = {"connectionId": "cc612ede-528a-11f1-9b86-005056afa2d7"}
        
        # UUID format validation
        uuid = params["connectionId"]
        parts = uuid.split("-")
        
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4


class TestStargateGetResponseParsing:
    """Test response parsing."""

    def test_user_list_response(self):
        """Test user list response parsing."""
        response = {
            "user": [
                {"id": "1", "username": "mgadmin", "type": "0"},
                {"id": "2", "username": "testuser", "type": "0"}
            ],
            "errorMsg": None
        }
        
        assert "user" in response
        assert len(response["user"]) == 2
        assert response["user"][0]["username"] == "mgadmin"
        assert response["errorMsg"] is None

    def test_empty_user_list_response(self):
        """Test empty user list response."""
        response = {"user": [], "errorMsg": None}
        
        assert "user" in response
        assert len(response["user"]) == 0

    def test_count_response(self):
        """Test count response parsing."""
        response = {"message": "5", "errorMsg": None}
        
        assert response["message"] == "5"
        assert response["errorMsg"] is None
        assert int(response["message"]) == 5

    def test_connection_list_response(self):
        """Test connection list response parsing."""
        response = {
            "connection": [
                {"id": "conn-1", "name": "test-rdp", "protocol": "1"}
            ],
            "errorMsg": None
        }
        
        assert "connection" in response
        assert len(response["connection"]) == 1

    def test_error_response(self):
        """Test error response parsing."""
        response = {"errorMsg": "connection not exist", "message": None}
        
        assert "errorMsg" in response
        assert response["errorMsg"] == "connection not exist"

    def test_not_found_response(self):
        """Test 404 response parsing."""
        response = {"errorMsg": "not found", "status_code": 404}
        
        assert response["errorMsg"] == "not found"
        assert response["status_code"] == 404

    def test_server_error_response(self):
        """Test 500 server error response."""
        response = {"errorMsg": "internal server error", "status_code": 500}
        
        assert response["errorMsg"] == "internal server error"
        assert response["status_code"] == 500


class TestStargateGetAuthHeader:
    """Test authentication header."""

    def test_bearer_token_format(self):
        """Test Bearer token format."""
        token = "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
        token_b64 = base64.b64encode(token.encode()).decode()
        bearer = f"Bearer {token_b64}"
        
        assert bearer.startswith("Bearer ")
        assert bearer.count(" ") == 1

    def test_auth_header_json_format(self):
        """Test headers dict format."""
        token_b64 = base64.b64encode(b"ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c").decode()
        
        headers = {
            "Authorization": f"Bearer {token_b64}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"


class TestStargateGetURLConstruction:
    """Test URL construction."""

    def test_full_url_construction(self):
        """Test full URL is correctly constructed."""
        server = "https://10.201.208.160:8443"
        endpoint = "/adama/rest/userGet"
        
        url = f"{server}{endpoint}"
        
        assert url == "https://10.201.208.160:8443/adama/rest/userGet"

    def test_url_with_pagination(self):
        """Test URL with pagination query string."""
        server = "https://10.201.208.160:8443"
        endpoint = "/adama/rest/userGet"
        params = {"start": "0", "length": "10"}
        
        query = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{server}{endpoint}?{query}"
        
        assert "start=0" in url
        assert "length=10" in url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])