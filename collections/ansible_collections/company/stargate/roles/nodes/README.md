# nodes role

Discovers, registers, and manages nodes in Stargate. Supports status queries, configuration updates, and maintenance mode.

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
| `node_operation` | Operation to perform | `list` |
| `node_id` | Specific node ID | `""` |
| `node_status` | Filter by status | `""` |
| `node_site` | Filter by site | `""` |
| `node_labels` | Labels to set/update | `{}` |
| `node_discover_ip` | IP range for discovery | `""` |

## Operations

- `list` - List all nodes (default)
- `discover` - Perform node discovery scan
- `maintenance` - Set node to maintenance mode
- `update` - Update node labels
- `delete` - Delete a node

## Example Playbook

```yaml
- hosts: stargate
  gather_facts: false
  roles:
    - role: company.stargate.login
  tasks:
    - role: company.stargate.nodes
      vars:
        node_operation: list
        node_status: online

    - name: Report online nodes
      ansible.builtin.debug:
        msg: "Found {{ node_count }} online nodes"
        verbosity: 0

    - name: Enable maintenance on specific node
      include_role:
        name: company.stargate.nodes
      vars:
        node_operation: maintenance
        node_id: "node-001"
```

## Output Variables

| Variable | Description |
|----------|-------------|
| `nodes` | List of node objects |
| `node_count` | Number of nodes returned |
| `target_node` | Single node object (when ID specified) |