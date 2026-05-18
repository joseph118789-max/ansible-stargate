# Company.Stargate Ansible Collection

Ansible Collection for automating **Stargate / MasterSAM REST API** operations.

Supports connection management, account password retrieval, user management, and resource provisioning for enterprise PAM environments.

## Requirements

- Ansible 2.9+
- Python 3.8+

## Installation

```bash
# Install from GitHub
ansible-galaxy collection install git+https://github.com/joseph118789-max/ansible-stargate.git

# Or from Galaxy (when published)
ansible-galaxy collection install company.stargate
```

## Quick Start

### Authentication

Stargate REST API uses **base64(username:api_secret)** as Bearer token:

```yaml
- hosts: localhost
  gather_facts: no
  tasks:
    - name: Get connections
      company.stargate.stargate_get:
        server: "https://10.201.208.160:8443"
        token: "ansible:d147ef1f-896d-487c-833e-28154903afc5"
        endpoint: "/connectionGet"
        data:
          start: 0
          length: 10
      register: result

    - debug:
        var: result.data.connection
```

## Verified Endpoints

| Endpoint | Description |
|----------|-------------|
| `userGet` | List users |
| `userCount` | Count users |
| `connectionGet` | List connections |
| `connectionCount` | Count connections |
| `connectionCreate` | Create connection |
| `connectionDelete` | Delete connection |
| `accountPasswordGet` | Get account password |
| `accountPasswordPlainCreate` | Create plain password |
| `accountInsecurePasswordGet` | Get insecure password |
| `accountCommonGet` | Get account common data |
| `accountCreate` | Create account |
| `resourceOracleCreate` | Create Oracle resource |
| `resourceUnixCreate` | Create Unix resource |
| `resourceWindowsCreate` | Create Windows resource |

## Example Playbook

```yaml
- name: Manage Stargate Connections
  hosts: localhost
  gather_facts: no
  vars:
    stargate_server: "https://10.201.208.160:8443"
    stargate_token: "ansible:d147ef1f-896d-487c-833e-28154903afc5"

  tasks:
    - name: Get all connections
      company.stargate.stargate_get:
        server: "{{ stargate_server }}"
        token: "{{ stargate_token }}"
        endpoint: "/connectionGet"
        data:
          start: 0
          length: 50
      register: connections

    - name: Display connections
      ansible.builtin.debug:
        msg: "Found {{ connections.data.connection | length }} connections"

    - name: Get users
      company.stargate.stargate_get:
        server: "{{ stargate_server }}"
        token: "{{ stargate_token }}"
        endpoint: "/userGet"
        data:
          start: 0
          length: 50
      register: users

    - name: Display users
      ansible.builtin.debug:
        msg: "Found {{ users.data.user | length }} users"
```

## Authentication Details

Stargate uses **base64(username:token)** encoded as Bearer token:

```python
import base64

# Token format: "username:api_secret"
token = "ansible:d147ef1f-896d-487c-833e-28154903afc5"
auth_b64 = base64.b64encode(token.encode()).decode()

# Use in header:
headers = {
    "Authorization": f"Bearer {auth_b64}",
    "Content-Type": "application/json"
}
```

## API Base URL

```
https://{server}:{port}/adama/rest/{endpoint}
```

## Collection Structure

```
company.stargate/
├── plugins/
│   ├── modules/
│   │   ├── stargate_login.py
│   │   ├── stargate_get.py
│   │   ├── stargate_post.py
│   │   └── stargate_delete.py
│   └── module_utils/
│       └── stargate_utils.py
├── roles/
│   ├── login/
│   ├── alarms/
│   ├── nodes/
│   ├── services/
│   ├── backup/
│   ├── monitoring/
│   └── reports/
├── playbooks/
└── docs/
```

## Server Configuration

| Parameter | Value |
|-----------|-------|
| Server | https://10.201.208.160:8443 |
| API User | ansible |
| Token | d147ef1f-896d-487c-833e-28154903afc5 |

## License

GPL-3.0-or-later

## Author

Company Automation Team