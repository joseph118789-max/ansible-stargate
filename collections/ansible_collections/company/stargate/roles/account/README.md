# account role

Manage Stargate account operations via REST API.

## Requirements

- ansible >= 2.9
- python >= 3.8

## Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `stargate_server` | Stargate server URL | `https://YOUR_SERVER_IP:8443` |
| `stargate_token` | Authentication token | `""` |
| `stargate_validate_certs` | Validate SSL certificates | `false` |
| `stargate_use_ssl` | Use SSL/TLS | `true` |
| `stargate_timeout` | Request timeout | `30` |
| `account_operation` | Operation to perform | `get` |
| `account_start` | Pagination start index | `0` |
| `account_length` | Pagination page size | `10` |
| `account_data` | Account data dict for create/password operations | `{}` |

### Operations

- `get` - Get accounts with pagination
- `create` - Create a new account
- `get_password` - Get account password

## Dependencies

- `company.stargate.login` - Runs first if `stargate_token` is not set

## Output Variables

| Variable | Description |
|----------|-------------|
| `accounts` | List of accounts from get operation |
| `created_account` | Created account data |
| `account_password` | Password data from password operation |

## Example Playbook

```yaml
- hosts: stargate
  gather_facts: false
  roles:
    - role: company.stargate.login
      vars:
        stargate_username: ansible
        stargate_password: "{{ lookup('env', 'STARTOKEN') }}"
  tasks:
    - role: company.stargate.account
      vars:
        account_operation: get
        account_length: 50

    - name: Create a new account
      role: company.stargate.account
      vars:
        account_operation: create
        account_data:
          name: testaccount
          password: SecurePass123

    - name: Get account password
      role: company.stargate.account
      vars:
        account_operation: get_password
        account_data:
          id: 123
```