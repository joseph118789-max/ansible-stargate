# backup role

Backs up Stargate configuration, nodes, services, and optionally triggers an API-level backup.

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
| `stargate_version` | Stargate version | `11.7.0` |
| `backup_dest_path` | Local backup directory | `/var/backups/stargate` |
| `backup_file_mode` | Backup file permissions | `0600` |
| `backup_description` | Backup description | `Manual Ansible backup` |
| `backup_include_config` | Include config in backup | `true` |
| `backup_include_nodes` | Include nodes in backup | `true` |
| `backup_include_services` | Include services in backup | `true` |
| `backup_include_alarms` | Include alarms in backup | `true` |
| `backup_include_history` | Include alarm history | `false` |
| `backup_save_local` | Save backup to local file | `true` |
| `backup_trigger_api` | Trigger API-based backup | `false` |

## Example Playbook

```yaml
- hosts: stargate
  gather_facts: true
  roles:
    - role: company.stargate.login
  tasks:
    - role: company.stargate.backup
      vars:
        backup_dest_path: "/var/backups/stargate"
        backup_description: "Pre-upgrade backup"
        backup_include_history: true

    - name: Verify backup was created
      ansible.builtin.stat:
        path: "{{ backup_path }}"
      register: backup_file

    - name: Copy backup to remote storage
      ansible.builtin.copy:
        src: "{{ backup_path }}"
        dest: "/mnt/nas/stargate/backups/"
        mode: "0644"
      when: backup_file.stat.exists
```

## Output Variables

| Variable | Description |
|----------|-------------|
| `backup_timestamp` | ISO8601 timestamp of backup |
| `backup_path` | Full path to backup file |
| `backup_manifest` | Full backup data dictionary |