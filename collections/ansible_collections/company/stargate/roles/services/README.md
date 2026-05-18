# services role

Manages services in Stargate - start, stop, restart, and query service status.

## Requirements

- ansible >= 2.9
- python >= 3.8

## Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `stargate_server` | Stargate server URL | `https://localhost:9443` |
| `stargate_token` | Authentication token | `""` |
| `stargate_validate_certs` | Validate SSL certificates | `false` |
| `stargate_use_ssl` | Use SSL/TLS | `true` |
| `stargate_timeout` | Request timeout | `30` |
| `service_operation` | Operation to perform | `list` |
| `service_id` | Specific service ID | `""` |
| `service_status` | Filter by status | `""` |
| `service_type` | Filter by type | `""` |

## Operations

- `list` - List all services (default)
- `start` - Start specific service
- `stop` - Stop specific service
- `restart` - Restart specific service
- `delete` - Delete specific service

## Example Playbook

```yaml
- hosts: stargate
  gather_facts: false
  roles:
    - role: company.stargate.login
  tasks:
    - name: List all services
      include_role:
        name: company.stargate.services
      vars:
        service_operation: list

    - name: Restart nginx service
      include_role:
        name: company.stargate.services
      vars:
        service_operation: restart
        service_id: "nginx-web"

    - name: Get running services
      include_role:
        name: company.stargate.services
      vars:
        service_operation: list
        service_status: running
```

## Output Variables

| Variable | Description |
|----------|-------------|
| `services` | List of service objects |
| `service_count` | Number of services returned |
| `target_service` | Single service object (when ID specified) |