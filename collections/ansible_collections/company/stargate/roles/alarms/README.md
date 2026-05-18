# alarms role

Retrieves, filters, acknowledges, clears, and exports alarms from the Stargate API.

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
| `alarm_operation` | Operation to perform | `list` |
| `alarm_id` | Specific alarm ID | `""` |
| `alarm_status` | Filter by status | `""` |
| `alarm_severity` | Filter by severity | `""` |
| `alarm_export` | Export alarms to file | `false` |
| `alarm_export_path` | Export file path | `/tmp/alarms.json` |

## Operations

- `list` - List all alarms (default)
- `acknowledge` - Acknowledge specific alarm by ID
- `clear` - Clear specific alarm by ID
- `acknowledge_all` - Bulk acknowledge all matching filters
- `clear_all` - Bulk clear all matching filters
- `delete` - Delete specific alarm by ID

## Example Playbook

```yaml
- hosts: stargate
  gather_facts: false
  roles:
    - role: company.stargate.login
  tasks:
    - role: company.stargate.alarms
      vars:
        alarm_operation: list
        alarm_status: active
        alarm_severity: critical
        alarm_export: true
        alarm_export_path: "/tmp/critical_alarms.json"

    - name: Report critical alarm count
      ansible.builtin.debug:
        msg: "Found {{ alarm_count }} critical active alarms"
```

## Output Variables

| Variable | Description |
|----------|-------------|
| `alarms` | List of alarm objects |
| `alarm_count` | Number of alarms returned |
| `latest_alarm` | Single alarm object (when ID specified) |