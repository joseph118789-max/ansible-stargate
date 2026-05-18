# Company.Stargate Ansible Collection

Ansible Collection for automating **Stargate / MasterSAM REST API** operations.

Supports authentication, alarm management, node discovery, service monitoring, backup, and reporting for NOC/telecom environments.

## Requirements

- Ansible 2.9+
- Python 3.8+
- `requests` Python library

## Installation

### Git install (latest)

```bash
ansible-galaxy collection install git+https://github.com/joseph118789-max/ansible-stargate.git
```

### From Galaxy

```bash
ansible-galaxy collection install company.stargate
```

### Manual

Clone into your Ansible collections path:

```bash
git clone https://github.com/joseph118789-max/ansible-stargate.git
# Copy or symlink to ~/.ansible/collections/ansible_collections/company/stargate
```

## Quick Start

### 1. Login

```yaml
- hosts: localhost
  gather_facts: no
  tasks:
    - name: Login to Stargate
      company.stargate.stargate_login:
        server: "https://pms.tony.lab.ctc-g.com.my:9443"
        username: "admin"
        password: "password"
      register: login_result

    - name: Fetch active alarms
      company.stargate.stargate_alarm:
        server: "https://pms.tony.lab.ctc-g.com.my:9443"
        token: "{{ login_result.token }}"
        state: present
      register: alarms
```

### 2. Discover Nodes

```yaml
- hosts: localhost
  tasks:
    - name: Get all nodes
      company.stargate.stargate_node:
        server: "https://pms.tony.lab.ctc-g.com.my:9443"
        token: "{{ hostvars['localhost']['stargate_token'] }}"
        state: list
```

### 3. Backup Node Config

```yaml
- hosts: stargate_nodes
  roles:
    - role: company.stargate.backup
      vars:
        stargate_server: "https://pms.tony.lab.ctc-g.com.my:9443"
        stargate_token: "{{ hostvars['localhost']['stargate_token'] }}"
```

## Collection Structure

```
company.stargate/
├── plugins/
│   ├── modules/
│   │   ├── stargate_login.py
│   │   ├── stargate_logout.py
│   │   ├── stargate_get.py
│   │   ├── stargate_post.py
│   │   ├── stargate_put.py
│   │   ├── stargate_delete.py
│   │   ├── stargate_alarm.py
│   │   ├── stargate_node.py
│   │   └── stargate_service.py
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
├── tests/
│   ├── unit/
│   ├── integration/
│   └── molecule/
└── docs/
```

## Module List

| Module | Description |
|--------|-------------|
| `stargate_login` | Authenticate and get session token |
| `stargate_logout` | Terminate session |
| `stargate_get` | Generic GET request |
| `stargate_post` | Generic POST request |
| `stargate_put` | Generic PUT request |
| `stargate_delete` | Generic DELETE request |
| `stargate_alarm` | Alarm CRUD operations |
| `stargate_node` | Node management |
| `stargate_service` | Service management |

## Role List

| Role | Description |
|------|-------------|
| `login` | Authenticate and store token |
| `alarms` | Get, filter, clear, export alarms |
| `nodes` | Discover and manage nodes |
| `services` | Service lifecycle management |
| `backup` | Backup node configurations |
| `monitoring` | Polling and metrics collection |
| `reports` | Generate and export reports |

## Authentication

Stargate uses **Bearer token** authentication. Tokens are obtained via `/api/auth/login`:

```bash
curl -X POST https://stargate.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires": "2024-12-31T23:59:59Z"
}
```

## Common Patterns

### Reuse Token in Playbook

```yaml
- hosts: localhost
  gather_facts: no
  tasks:
    - name: Login
      company.stargate.stargate_login:
        server: "{{ stargate_server }}"
        username: "{{ stargate_username }}"
        password: "{{ stargate_password }}"
      register: login

- hosts: stargate
  gather_facts: no
  tasks:
    - name: Get alarms
      company.stargate.stargate_alarm:
        server: "{{ stargate_server }}"
        token: "{{ hostvars['localhost']['stargate_token'] }}"
      register: alarms
```

### Workflow Playbook

```yaml
- name: Stargate NOC Workflow
  hosts: localhost
  gather_facts: no
  vars:
    stargate_server: "https://pms.tony.lab.ctc-g.com.my:9443"
    stargate_username: "admin"
    stargate_password: "password"

  tasks:
    - name: Login
      company.stargate.stargate_login:
        server: "{{ stargate_server }}"
        username: "{{ stargate_username }}"
        password: "{{ stargate_password }}"
      register: login

    - name: Discover nodes
      company.stargate.stargate_node:
        server: "{{ stargate_server }}"
        token: "{{ login.token }}"
        state: list
      register: nodes

    - name: Collect alarms
      company.stargate.stargate_alarm:
        server: "{{ stargate_server }}"
        token: "{{ login.token }}"
        state: present
      register: alarms

    - name: Generate report
      ansible.builtin.debug:
        msg: "Found {{ alarms.alarms | length }} active alarms"

    - name: Backup all nodes
      include_role:
        name: company.stargate.backup
      loop: "{{ nodes.nodes }}"
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STARGATE_SERVER` | Stargate server URL | - |
| `STARGATE_USERNAME` | API username | - |
| `STARGATE_PASSWORD` | API password | - |
| `STARGATE_TOKEN` | Bearer token | - |
| `STARGATE_VALIDATE_CERTS` | Validate SSL certs | `true` |

## Error Handling

All modules include:
- Automatic retry on transient failures (3 retries, 5s delay)
- SSL certificate validation toggle
- Token refresh on 401 responses
- Detailed error messages with HTTP status codes

## API Version

Default API version: **11.7.0**

Set via `api_version` parameter or `X-API-Version` header.

## License

GPL-3.0-or-later

## Author

Company Automation Team