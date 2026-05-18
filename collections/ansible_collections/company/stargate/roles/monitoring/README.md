# monitoring role

Polls Stargate API to collect current alarm, node, and service status metrics. Can enforce thresholds and fail if conditions exceed configured limits.

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
| `monitor_critical_threshold` | Fail if critical >= this | `1` |
| `monitor_high_threshold` | Alert if high >= this | `10` |
| `monitor_offline_node_threshold` | Alert if offline >= this | `1` |
| `monitor_verbose` | Print summary debug output | `true` |

## Example Playbook

```yaml
- hosts: stargate
  gather_facts: false
  roles:
    - role: company.stargate.login
  tasks:
    - role: company.stargate.monitoring
      vars:
        monitor_critical_threshold: 0
        monitor_verbose: true

    - name: Store metrics for history
      ansible.builtin.copy:
        content: "{{ monitoring_metrics | to_nice_json }}"
        dest: "/var/lib/stargate/metrics/{{ ansible_date_time.epoch }}.json"
        mode: "0644"
```

## Output Variables

| Variable | Description |
|----------|-------------|
| `monitoring_metrics` | Dictionary with all counts |
| `alert_critical_alarms` | True if critical >= threshold |
| `alert_high_alarms` | True if high >= threshold |
| `alert_nodes_offline` | True if offline >= threshold |
| `critical_count` | Count of critical alarms |
| `high_count` | Count of high-severity alarms |
| `online_nodes` | Count of online nodes |
| `running_services` | Count of running services |