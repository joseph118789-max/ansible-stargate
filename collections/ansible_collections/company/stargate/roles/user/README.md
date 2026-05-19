# user role

Manage Stargate user operations via REST API.

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
| `user_operation` | Operation to perform | `get` |
| `user_start` | Pagination start index | `0` |
| `user_length` | Pagination page size | `10` |
| `user_data` | User data dict for create/update/delete | `{}` |

### Operations

- `get` - Get users with pagination
- `count` - Count all users
- `create` - Create a new user
- `update` - Update an existing user
- `delete` - Delete a user

## Dependencies

- `company.stargate.login` - Runs first if `stargate_token` is not set

## Output Variables

| Variable | Description |
|----------|-------------|
| `users` | List of users from get operation |
| `user_count` | User count from count operation |
| `created_user` | Created user data |
| `updated_user` | Updated user data |
| `deleted_user` | Deleted user data |

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
    - role: company.stargate.user
      vars:
        user_operation: get
        user_start: 0
        user_length: 50

    - name: Create a new user
      role: company.stargate.user
      vars:
        user_operation: create
        user_data:
          name: testuser
          password: SecurePass123
          enabled: true
```