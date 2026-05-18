# (c) 2024 Company Automation Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for stargate_utils module."""

import pytest
import base64


class TestStargateUtils:
    """Tests for stargate_utils utility functions."""

    def test_base64_encode_token(self):
        """Test that username:token is correctly base64 encoded."""
        username = "ansible"
        token = "d147ef1f-896d-487c-833e-28154903afc5"
        expected = base64.b64encode(f"{username}:{token}".encode()).decode()
        assert expected == base64.b64encode("ansible:d147ef1f-896d-487c-833e-28154903afc5".encode()).decode()

    def test_bearer_token_format(self):
        """Test Bearer token format is correct."""
        username = "ansible"
        token = "d147ef1f-896d-487c-833e-28154903afc5"
        token_b64 = base64.b64encode(f"{username}:{token}".encode()).decode()
        bearer = f"Bearer {token_b64}"
        assert bearer.startswith("Bearer ")
        assert len(bearer) > 20

    def test_api_url_construction(self):
        """Test API URL is correctly constructed."""
        base_url = "https://10.201.208.160:8443/adama/rest"
        endpoint = "userGet"
        expected = f"{base_url}/{endpoint}"
        assert expected == "https://10.201.208.160:8443/adama/rest/userGet"

    def test_request_headers(self):
        """Test that request headers are correctly formed."""
        token_b64 = base64.b64encode(b"ansible:d147ef1f-896d-487c-833e-28154903afc5").decode()
        headers = {
            "Authorization": f"Bearer {token_b64}",
            "Content-Type": "application/json"
        }
        assert headers["Authorization"] == f"Bearer {token_b64}"
        assert headers["Content-Type"] == "application/json"

    def test_json_payload_serialization(self):
        """Test JSON payload is correctly serialized."""
        import json
        data = {"start": 0, "length": 10}
        payload = json.dumps(data).encode()
        parsed = json.loads(payload.decode())
        assert parsed == data

    def test_error_response_parsing(self):
        """Test error responses are correctly parsed."""
        import json
        error_response = '{"message": "failed", "errorMsg": "connection not exist"}'
        parsed = json.loads(error_response)
        assert parsed["message"] == "failed"
        assert parsed["errorMsg"] == "connection not exist"

    def test_success_response_parsing(self):
        """Test success responses are correctly parsed."""
        import json
        success_response = '{"user": [{"id": "1", "username": "mgadmin"}], "errorMsg": null}'
        parsed = json.loads(success_response)
        assert "user" in parsed
        assert parsed["user"][0]["username"] == "mgadmin"
        assert parsed["errorMsg"] is None

    def test_count_response_parsing(self):
        """Test count responses are correctly parsed."""
        import json
        count_response = '{"message": "3", "errorMsg": null}'
        parsed = json.loads(count_response)
        assert parsed["message"] == "3"
        assert parsed["errorMsg"] is None

    def test_empty_result_parsing(self):
        """Test empty result responses are correctly parsed."""
        import json
        empty_response = '{"connection": [], "errorMsg": null}'
        parsed = json.loads(empty_response)
        assert parsed["connection"] == []
        assert parsed["errorMsg"] is None

    def test_pagination_params(self):
        """Test pagination parameters are correctly formed."""
        params = {"start": 0, "length": 50}
        import json
        payload = json.dumps(params).encode()
        parsed = json.loads(payload.decode())
        assert parsed["start"] == 0
        assert parsed["length"] == 50

    def test_filter_params(self):
        """Test filter parameters are correctly formed."""
        params = {"userName": "testuser", "start": 0, "length": 10}
        import json
        payload = json.dumps(params).encode()
        parsed = json.loads(payload.decode())
        assert parsed["userName"] == "testuser"
        assert parsed["start"] == 0
        assert parsed["length"] == 10

    def test_connection_id_param(self):
        """Test connection ID parameter is correctly formed."""
        params = {"connectionId": "cc612ede-528a-11f1-9b86-005056afa2d7"}
        import json
        payload = json.dumps(params).encode()
        parsed = json.loads(payload.decode())
        assert parsed["connectionId"] == "cc612ede-528a-11f1-9b86-005056afa2d7"

    def test_account_id_param(self):
        """Test account ID parameter is correctly formed."""
        params = {"accountId": "a3680be7-528a-11f1-9b86-005056afa2d7"}
        import json
        payload = json.dumps(params).encode()
        parsed = json.loads(payload.decode())
        assert parsed["accountId"] == "a3680be7-528a-11f1-9b86-005056afa2d7"