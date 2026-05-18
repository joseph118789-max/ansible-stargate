# reports role

Generates operational reports from Stargate API data - summarizing alarms, nodes, and services with counts by status/severity. Optionally includes raw data and saves reports to disk.

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
| `report_type` | Type of report to generate | `full` |
| `report_dest_path` | Directory for saved reports | `/var/reports/stargate` |
| `report_file_mode` | Report file permissions | `0644` |
| `report_save` | Save report to file | `true` |
| `report_include_raw` | Include raw data in report | `false` |

## Report Types

- `alarms` - Alarm summary by severity
- `nodes` - Node summary by status
- `services` - Service summary by status
- `full` - All three summaries combined (default)

## Example Playbook

```yaml
- hosts: stargate
  gather_facts: true
  roles:
    - role: company.stargate.login
  tasks:
    - name: Generate full operational report
      include_role:
        name: company.stargate.reports
      vars:
        report_type: full
        report_include_raw: false
        report_dest_path: "/var/reports/stargate"

    - name: Generate alarms report with raw data
      include_role:
        name: company.stargate.reports
      vars:
        report_type: alarms
        report_include_raw: true
        report_dest_path: "/var/reports/stargate"

    - name: Email report summary
      ansible.builtin.mail:
        host: smtp.example.com
        to: ops@example.com
        subject: "Stargate Report {{ ansible_date_time.iso8601 }}"
        body: |
          Alarm Summary: {{ stargate_report.alarms.total }} total
            Critical: {{ stargate_report.alarms.critical }}
            High: {{ stargate_report.alarms.high }}
          Node Summary: {{ stargate_report.nodes.online }}/{{ stargate_report.nodes.total }} online
          Service Summary: {{ stargate_report.services.running }}/{{ stargate_report.services.total }} running
        attach: "{{ report_path }}"
      when: stargate_report is defined
```

## Output Variables

| Variable | Description |
|----------|-------------|
| `stargate_report` | Full report data structure |
| `alarm_severity_summary` | Counts by severity |
| `node_uptime_summary` | Counts by node status |
| `service_status_summary` | Counts by service status |
| `report_path` | Path to saved report file |