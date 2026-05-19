# ansible-stargate

> Ansible collection for MasterSAM Stargate REST API v11.7.0 automation

## Quick Links

| Resource | Link |
|----------|------|
| **Collection README** | [`collections/ansible_collections/company/stargate/README.md`](collections/ansible_collections/company/stargate/README.md) |
| **API Documentation** | [`collections/ansible_collections/company/stargate/docs/API_ENDPOINTS.md`](collections/ansible_collections/company/stargate/docs/API_ENDPOINTS.md) |
| **galaxy.yml** | [`collections/ansible_collections/company/stargate/galaxy.yml`](collections/ansible_collections/company/stargate/galaxy.yml) |
| **GitHub Repository** | https://github.com/joseph118789-max/ansible-stargate |
| **Report Issues** | https://github.com/joseph118789-max/ansible-stargate/issues |

## Installation

```bash
# From Galaxy (once published)
ansible-galaxy collection install company.stargate

# From source
git clone https://github.com/joseph118789-max/ansible-stargate.git
cd ansible-stargate
ansible-galaxy collection build
ansible-galaxy collection install company-stargate-*.tar.gz --force
```

## Project Statistics

| Category | Count |
|----------|-------|
| Modules | 11 |
| Roles | 10 |
| Playbooks | 5 |
| Unit Tests | 123 (all passing) |
| API Endpoints Documented | 88 |
| Molecule Scenarios | 3 |

## Usage

```yaml
- name: Get users from Stargate
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Retrieve users
      company.stargate.stargate_get:
        server: "https://10.201.208.160:8443"
        token: "ansible:YOUR_TOKEN_HERE"
        endpoint: "/userGet"
        data:
          start: "0"
          length: "10"
```

## Testing

```bash
# Unit tests
python3 -m pytest tests/unit/ -v

# Integration tests
ansible-playbook tests/integration/test_negative.yml

# Molecule tests
cd tests/molecule/default && molecule test
```

## License

GPL-3.0-or-later

## Support

For issues and questions, open an issue at:
https://github.com/joseph118789-max/ansible-stargate/issues