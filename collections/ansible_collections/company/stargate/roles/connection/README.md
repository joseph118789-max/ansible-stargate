# connection role

Manage Stargate connection operations via REST API.

## Requirements

- ansible >= 2.9
- python >= 3.8

## Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `stargate_server` | Stargate server URL | `https://10.201.208.160:8443` |
| `stargate_token` | Authentication token | `""` |
| `stargate_validate_certs` | Validate SSL certificates | `false` |
| `stargate_use_ssl` | Use SSL/TLS | `true` |
| `stargate_timeout` | Request timeout | `30` |
| `connection_operation` | Operation to perform | `get` |
| `connection_start` | Pagination start index | `0` |
| `connection_length` | Pagination page size | `10` |
| `connection_data` | Connection data dict for create/delete | `{}` |

### Operations

- `get` - Get connections with pagination
- `count` - Count all connections
- `create` - Create a new connection
- `delete` - Delete a connection

## Dependencies

- `company.stargate.login` - Runs first if `stargate_token` is not set

## Output Variables

| Variable | Description |
|----------|-------------|
| `connections` | List of connections from get operation |
| `connection_count` | Connection count from count operation |
| `created_connection` | Created connection data |
| `deleted_connection` | Deleted connection data |

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
    - role: company.stargate.connection
      vars:
        connection_operation: get
        connection_length: 50

    - name: Create a new connection
      role: company.stargate.connection
      vars:
        connection_operation: create
        connection_data:
          name: TestConnection
          type: oracle
          host: db.example.com
          port: 1521
```