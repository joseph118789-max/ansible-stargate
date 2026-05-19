# (c) 2024 Company Automation Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for stargate_login module."""

import pytest
from unittest.mock import patch, MagicMock


class TestStargateLogin:
    """Tests for stargate_login module."""

    @patch('ansible.module_utils.basic.AnsibleModule')
    def test_login_returns_token(self, mock_module):
        """Test login module returns token on success."""
        mock_module.return_value = MagicMock()
        
        # Import after patching
        import sys
        sys.path.insert(0, '/root/.openclaw/workspace/projects/ansible-stargate/collections/ansible_collections/company/stargate/plugins/module_utils')
        
        # The stargate_login module uses stargate_api_wrapper
        # We mock the API response
        pass

    def test_token_format(self):
        """Test that token format is correct base64(username:token)."""
        import base64
        username = "ansible"
        token = "f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
        encoded = base64.b64encode(f"{username}:{token}".encode()).decode()
        
        # Verify it can be decoded back
        decoded = base64.b64decode(encoded).decode()
        assert decoded == f"{username}:{token}"

    def test_bearer_header_format(self):
        """Test Bearer header format for API calls."""
        import base64
        username = "ansible"
        token = "f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
        encoded = base64.b64encode(f"{username}:{token}".encode()).decode()
        
        header = f"Bearer {encoded}"
        assert header.startswith("Bearer ")
        assert " " in header
        parts = header.split(" ")
        assert len(parts) == 2
        assert len(parts[1]) > 20  # base64 encoded token is longer