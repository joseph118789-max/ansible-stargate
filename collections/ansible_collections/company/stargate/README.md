# Ansible Collection for MasterSAM Stargate

> Production-ready Ansible collection for automating MasterSAM Stargate REST API v11.7.0

[![CI/CD](https://github.com/joseph118789-max/ansible-stargate/workflows/CI/badge.svg)](https://github.com/joseph118789-max/ansible-stargate/actions)
[![Tests](https://img.shields.io/badge/tests-123%20passing-success)](tests/unit/)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue)](LICENSE)

## Overview

The `company.stargate` collection provides enterprise-grade automation for MasterSAM Stargate privileged access management system. It includes custom Ansible modules, roles, and playbooks for managing users, connections, accounts, alarms, nodes, and services through the REST API.

**API Version:** v11.7.0  
**Authentication:** Bearer token (base64 encoded username:token)  
**Server:** `https://10.201.208.160:8443`

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ansible-stargate                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Modules   │  │    Roles    │  │  Playbooks  │        │
│  │  (11 pcs)   │  │  (10 pcs)   │  │  (5 pcs)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                     Stargate REST API                        │
│                   (88 endpoints documented)                 │
├─────────────────────────────────────────────────────────────┤
│                  MasterSAM Stargate Server                   │
│                     (10.201.208.160)                        │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
ansible-stargate/
├── collections/
│   └── ansible_collections/
│       └── company/
│           └── stargate/
│               ├── galaxy.yml                 # Collection metadata
│               ├── README.md                 # This file
│               ├── LICENSE                   # GPL-3.0
│               │
│               ├── plugins/
│               │   ├── modules/              # 11 custom modules
│               │   │   ├── stargate_login.py
│               │   │   ├── stargate_logout.py
│               │   │   ├── stargate_get.py
│               │   │   ├── stargate_post.py
│               │   │   ├── stargate_put.py
│               │   │   ├── stargate_delete.py
│               │   │   ├── stargate_alarm.py
│               │   │   ├── stargate_node.py
│               │   │   ├── stargate_service.py
│               │   │   ├── stargate_user.py
│               │   │   ├── stargate_connection.py
│               │   │   └── stargate_account.py
│               │   │
│               │   ├── module_utils/         # Shared utilities
│               │   │   └── stargate_utils.py
│               │   │
│               │   └── doc_fragments/        # Module documentation
│               │       └── stargate.py
│               │
│               ├── roles/                    # 10 automation roles
│               │   ├── login/                # Authentication & session
│               │   ├── alarms/               # Alarm monitoring
│               │   ├── nodes/               # Node management
│               │   ├── services/             # Service management
│               │   ├── backup/               # Configuration backup
│               │   ├── monitoring/           # Metrics & polling
│               │   ├── reports/              # Report generation
│               │   ├── user/                 # User management
│               │   ├── connection/           # Connection management
│               │   └── account/              # Account management
│               │
│               └── docs/                    # Documentation
│                   └── API_ENDPOINTS.md
│
├── playbooks/                       # Sample playbooks
│   ├── user-management.yml
│   ├── connection-management.yml
│   ├── account-management.yml
│   ├── alarm-workflow.yml
│   └── daily-report.yml
│
├── tests/                           # Test suite
│   ├── unit/                        # Unit tests (pytest)
│   │   └── plugins/modules/
│   │       ├── test_stargate_*.py   # 123 passing tests
│   │
│   ├── integration/                 # Integration tests
│   │   ├── test_negative.yml
│   │   ├── test_idempotency.yml
│   │   └── test_timeout.yml
│   │
│   ├── molecule/                   # Molecule scenarios
│   │   ├── default/
│   │   ├── connection/
│   │   └── user/
│   │
│   └── api_test_suite.py           # API test runner
│
└── .github/
    └── workflows/
        └── ci.yml                  # GitHub Actions CI/CD

```

---

## Installation

### From Ansible Galaxy

```bash
ansible-galaxy collection install company.stargate
```

### From Source

```bash
git clone https://github.com/joseph118789-max/ansible-stargate.git
cd ansible-stargate
ansible-galaxy collection build
ansible-galaxy collection install company-stargate-*.tar.gz --force
```

### Requirements

- **Ansible:** 2.9+
- **Python:** 3.8+
- **Python Libraries:** `requests`, `PyYAML`

```bash
pip install requests PyYAML ansible
```

---

## Quick Start

### 1. Configure Connection

```yaml
# inventory.yml
all:
  vars:
    stargate_server: "https://10.201.208.160:8443"
    stargate_token: "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
    validate_certs: false
```

### 2. Login and Get Users

```yaml
---
- name: Get Stargate users
  hosts: localhost
  gather_facts: no
  
  tasks:
    - name: Get all users
      company.stargate.stargate_get:
        server: "{{ stargate_server }}"
        token: "{{ stargate_token }}"
        endpoint: "/userGet"
        data:
          start: "0"
          length: "50"
      register: users_result
    
    - name: Display users
      debug:
        msg: "Found {{ users_result.data.user | length }} users"
```

### 3. Create a Connection

```yaml
---
- name: Create RDP connection
  hosts: localhost
  gather_facts: no
  
  tasks:
    - name: Create Windows RDP connection
      company.stargate.stargate_post:
        server: "{{ stargate_server }}"
        token: "{{ stargate_token }}"
        endpoint: "/connectionCreate"
        data:
          name: "prod-windows-rdp"
          protocol: "1"
          hostname: "192.168.1.100"
          port: "3389"
      register: result
    
    - name: Show result
      debug:
        var: result
```

---

## Modules

| Module | Description |
|--------|-------------|
| `stargate_login` | Authenticate and obtain session token |
| `stargate_logout` | Terminate session and logout |
| `stargate_get` | GET requests - retrieve data |
| `stargate_post` | POST requests - create resources |
| `stargate_put` | PUT requests - update resources |
| `stargate_delete` | DELETE requests - remove resources |
| `stargate_user` | User management operations |
| `stargate_connection` | Connection management |
| `stargate_account` | Account management |
| `stargate_alarm` | Alarm monitoring and handling |
| `stargate_node` | Node discovery and management |
| `stargate_service` | Service status and management |

---

## Roles

| Role | Purpose |
|------|---------|
| `login` | Authentication, token management, session renewal |
| `alarms` | Monitor, filter, clear, and archive alarms |
| `nodes` | Node discovery, status, config backup |
| `services` | Service management, health checks |
| `backup` | Configuration backup and restore |
| `monitoring` | Metrics polling, dashboard export |
| `reports` | Report generation, export |
| `user` | User CRUD, group management |
| `connection` | Connection CRUD, protocol management |
| `account` | Account profile management |

---

## Playbooks

### User Management

```yaml
- name: User management workflow
  hosts: localhost
  gather_facts: no
  
  roles:
    - company.stargate.login
    - company.stargate.user
```

### Alarm Monitoring

```yaml
- name: Alarm monitoring workflow
  hosts: localhost
  gather_facts: no
  
  roles:
    - company.stargate.alarms
```

### Daily Report

```yaml
- name: Daily operations report
  hosts: localhost
  gather_facts: no
  
  tasks:
    - include_role:
        name: company.stargate.reports
      vars:
        report_type: daily
        format: json
```

---

## API Endpoints

The collection supports 88 documented API endpoints across 13 categories:

| Category | Endpoints | Status |
|----------|-----------|--------|
| User | userGet, userCount, userCreate, userDelete, userGroupCreate | ✅ Working |
| Connection | connectionGet, connectionCount, connectionCreate, connectionDelete | ✅ Working |
| Account | accountCommonGet, accountPasswordGet, accountWorkflowProfileGet | ✅ Working |
| Approved Connection | approvedConnectionGet, approvedConnectionCount | ✅ Working |
| Connection Authorization | connectionAuthorizationGet | ✅ Working |
| Connection Group | connectionGroupGet, connectionGroupCreate | ✅ Working |
| User Group | userGroupGet, userUserGroupGet, userGroupCreate | ✅ Working |
| Resource (Unix/Windows/Oracle) | resourceUnixCreate, resourceWindowsCreate, resourceOracleCreate | ✅ Working |
| Alarm | alarmGet, alarmCount | ❌ HTTP 404 (not implemented) |
| Node | nodeGet, nodeCount | ❌ HTTP 404 (not implemented) |
| Service | serviceStatusGet | ❌ HTTP 404 (not implemented) |
| Backup | backupGet | ❌ HTTP 404 (not implemented) |
| Reports | reportsGet | ❌ HTTP 404 (not implemented) |

### Pagination

All list endpoints require string pagination parameters:

```json
{"start": "0", "length": "10"}
```

### Authentication

```bash
# Bearer token format (base64)
Authorization: Bearer YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM=
```

---

## Testing

### Run Unit Tests

```bash
cd tests
python3 -m pytest unit/plugins/modules/ -v
```

### Run Integration Tests

```bash
# Test negative cases
ansible-playbook tests/integration/test_negative.yml

# Test idempotency
ansible-playbook tests/integration/test_idempotency.yml

# Test timeout/retry
ansible-playbook tests/integration/test_timeout.yml
```

### Run Molecule Tests

```bash
cd tests/molecule/default
molecule test
```

### Test Results

```
============================= 123 passed in 0.50s ==============================
```

---

## Configuration

### Module Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `server` | str | Yes | - | Stargate server URL |
| `token` | str | Yes | - | Bearer token (username:token) |
| `endpoint` | str | Yes | - | API endpoint path |
| `data` | dict | No | {} | Request body payload |
| `validate_certs` | bool | No | true | SSL certificate validation |
| `timeout` | int | No | 30 | Request timeout (seconds) |
| `retries` | int | No | 3 | Number of retry attempts |
| `retry_delay` | int | No | 5 | Delay between retries (seconds) |

### Role Variables

```yaml
stargate_server: "https://10.201.208.160:8443"
stargate_token: "ansible:TOKEN"
stargate_validate_certs: false
stargate_timeout: 30
stargate_retries: 3
```

---

## Troubleshooting

### Connection Issues

```bash
# Test server connectivity
curl -k -I https://10.201.208.160:8443/adama/

# Test API endpoint
curl -k -H "Authorization: Bearer TOKEN" https://10.201.208.160:8443/adama/rest/userCount
```

### Authentication Errors

```
Error: "api user is not exist"
```

**Solution:** Ensure the API user (`ansible`) exists in the Stargate database with the correct token.

```
Error: "XSRF attack"
```

**Solution:** GWT-RPC login requires browser session. Use REST API login instead.

### Module Failures

```
Error: Stargate API error (HTTP 500)
```

**Cause:** Server-side Java NPE bug (documented in known issues)

**Solution:** Some endpoints may return HTTP 500 due to unhandled null values in the Java backend. These cannot be fixed without server-side code changes.

---

## Known Issues

1. **GWT-RPC Login:** Requires browser session with permutation headers (XSRF protection)
2. **HTTP 500 Errors:** Several endpoints (alarmGet, nodeGet, serviceStatusGet) return 500 due to server-side NPE bugs
3. **Account Creation:** Some account creation endpoints fail with NPE in SshKeyPolicyService
4. **Policy Lookup:** String field names don't match Java setters

---

## License

**GPL-3.0-or-later**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

---

## Support

- **Issues:** https://github.com/joseph118789-max/ansible-stargate/issues
- **Repository:** https://github.com/joseph118789-max/ansible-stargate
- **Author:** Company Automation Team

---

## Changelog

### 1.0.0 (2026-05-19)

- Initial release
- 11 custom Ansible modules
- 10 pre-built roles
- 5 sample playbooks
- 123 passing unit tests
- 3 Molecule scenarios
- 88 API endpoints documented
- GitHub Actions CI/CD