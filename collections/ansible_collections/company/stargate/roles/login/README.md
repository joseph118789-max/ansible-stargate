# login role

Authenticates with the Stargate REST API and stores the session token for reuse in subsequent tasks within the same play.

## Requirements

- ansible >= 2.9
- python >= 3.8

## Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `stargate_server` | Stargate server URL | `https://localhost:9443` |
| `stargate_username` | Username for authentication | `admin` |
| `stargate_password` | Password for authentication | `admin` |
| `stargate_validate_certs` | Validate SSL certificates | `false` |
| `stargate_use_ssl` | Use SSL/TLS for connections | `true` |
| `stargate_timeout` | Request timeout in seconds | `30` |
| `stargate_token` | Existing token (skip login if set) | `""` |
| `stargate_force_login` | Force new login even if token exists | `false` |

## Dependencies

None.

## Example Playbook

```yaml
- hosts: stargate
  gather_facts: false
  roles:
    - role: company.stargate.login
      vars:
        stargate_server: "https://pms.example.com:9443"
        stargate_username: "admin"
        stargate_password: "secret"
```

After this role runs, `stargate_token` fact is available for all subsequent tasks in the play.