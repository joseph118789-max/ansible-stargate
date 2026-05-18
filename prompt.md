
**AI Prompt: Generate Production-Ready Ansible Collection / Roles for Stargate REST API Automation**

Act as a **Senior Ansible Architect, Python API Developer, QA Engineer, Technical Writer, and Enterprise Automation Lead**.

Input source:

* Use **Stargate / MasterSAM REST API documentation v11.7.0**
* Parse API endpoints, authentication methods, request/response payloads, status codes, and examples from the provided API documentation.

Objective:

Create a **production-ready Ansible project** to automate Stargate REST API operations.

Deliverables required:

---

# 1. Project Structure

Generate full project structure:

```bash
ansible-stargate/
├── collections/
│   └── ansible_collections/
│       └── company/
│           └── stargate/
│               ├── galaxy.yml
│               ├── README.md
│               ├── plugins/
│               │   ├── modules/
│               │   │   ├── stargate_login.py
│               │   │   ├── stargate_logout.py
│               │   │   ├── stargate_get.py
│               │   │   ├── stargate_post.py
│               │   │   ├── stargate_put.py
│               │   │   ├── stargate_delete.py
│               │   │   ├── stargate_alarm.py
│               │   │   ├── stargate_node.py
│               │   │   ├── stargate_service.py
│               │   │   └── ...
│               │
│               ├── roles/
│               │   ├── login/
│               │   ├── alarms/
│               │   ├── services/
│               │   ├── nodes/
│               │   ├── reports/
│               │   └── backup/
│               │
│               ├── tests/
│               │   ├── unit/
│               │   ├── integration/
│               │   └── molecule/
│               │
│               ├── docs/
│               └── playbooks/
```

---

# 2. API Discovery

Read API documentation and automatically identify:

* Authentication endpoints
* Session management
* Token handling
* CRUD endpoints
* Alarm APIs
* Node APIs
* Monitoring APIs
* Service APIs
* Inventory APIs
* Reporting APIs
* Search APIs

Create endpoint mapping table:

| Module         | Endpoint    | Method | Purpose         |
| -------------- | ----------- | ------ | --------------- |
| stargate_login | /auth/login | POST   | Authentication  |
| stargate_alarm | /alarm      | GET    | Retrieve alarms |

Include:

Request body examples

Response samples

Error handling

Pagination

Rate limits

Retries

---

# 3. Generate Ansible Modules

Create fully working custom modules.

Example:

```python
#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests

def run_module():

    module_args = dict(
        server=dict(type='str', required=True),
        token=dict(type='str', required=False, no_log=True),
        state=dict(type='str', default='present')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {
        "changed": False
    }

    endpoint="/api/alarm"

    r=requests.get(
        f"{module.params['server']}{endpoint}",
        headers={
            "Authorization":
            f"Bearer {module.params['token']}"
        }
    )

    result["response"]=r.json()

    module.exit_json(**result)

run_module()
```

Requirements:

* Idempotent
* Check mode support
* Error handling
* Timeout handling
* Retry mechanism
* Session reuse
* SSL validation option
* Pagination support
* Token refresh support

---

# 4. Create Roles

Generate roles:

## login role

Tasks:

Authenticate

Get token

Store fact

Renew session

Logout

---

## alarm role

Tasks:

Get active alarms

Filter severity

Export reports

Clear alarms

Archive alarms

---

## node role

Tasks:

Discover nodes

Get status

Update config

Backup config

Health check

---

## monitoring role

Tasks:

Polling

Metrics retrieval

Dashboard export

Report generation

---

# 5. Tests

Generate:

Unit tests

```bash
pytest
ansible-test units
```

Integration:

```bash
molecule test
```

Create:

Mock API tests

Negative tests

Timeout tests

Authentication failures

Retry tests

Idempotency tests

Load tests

---

# 6. Sample Usage

Generate playbooks:

Login:

```yaml
- hosts: localhost

  tasks:

  - stargate_login:
      server: https://server
      username: admin
      password: password
```

Alarm collection:

```yaml
- hosts: localhost

  roles:
    - alarms
```

Node backup:

```yaml
- hosts: stargate

  roles:
    - backup
```

Workflow example:

```yaml
Authenticate
→ Discover nodes
→ Collect alarms
→ Export report
→ Backup configs
→ Logout
```

---

# 7. Documentation

Generate:

README.md

Installation guide

Galaxy install

Role documentation

API mapping document

Architecture diagram (Mermaid)

Sequence diagram

Troubleshooting guide

Examples:

```bash
ansible-galaxy collection install company.stargate
```

---

# 8. CI/CD

Generate:

GitHub Actions

```yaml
lint
pytest
ansible-test
molecule
build collection
publish
```

Include:

ansible-lint

yamllint

flake8

pytest coverage

---

# 9. Deliver Final Output

Produce:

1. Full source code

2. Folder tree

3. Roles

4. Modules

5. Tests

6. Documentation

7. Sample inventory

8. CI pipeline

9. Example execution output

10. Galaxy packaging files

11. Release notes

12. Changelog

Use enterprise standards suitable for telecom / NOC / monitoring environments.

Use API information extracted from Stargate REST API documentation version 11.7.0 provided as source.

