# Contributing to ansible-stargate

Thank you for your interest in contributing to the ansible-stargate collection!

This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.9 or later
- Ansible 2.9 or later
- Docker (for Molecule testing)
- Git

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/company/ansible-stargate.git
   cd ansible-stargate
   ```

2. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install ansible ansible-lint yamllint flake8 pytest pytest-ansible pyyaml
   ```

4. Install the collection in development mode:
   ```bash
   ansible-galaxy collection build --force
   ansible-galaxy collection install company-stargate-*.tar.gz -p ./collections
   ```

## Making Changes

### Branching Strategy

1. Create a feature branch from `master`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards below.

3. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of what changed"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a Pull Request against `master`.

### Coding Standards

#### Ansible Modules

- Use `ansible.module_utils.basic` imports correctly
- Document all parameters with proper `module` argument specifications
- Use `module.fail_json()` for errors with meaningful messages
- Use `module.exit_json()` for successful completion
- Include `check_mode` support where applicable
- Always set `diff: no` unless diff support is explicitly needed

#### Python Code (module_utils)

- Follow PEP 8 style guidelines
- Maximum line length: 120 characters
- Use `from __future__ import` for Python 2/3 compatibility
- Add `__metaclass__ = type` for Python 2/3 compatibility
- Document all functions with docstrings
- Use type hints where appropriate

#### YAML Files

- Use 4-space indentation
- Keep lines under 120 characters when possible
- Use descriptive names for hosts, tasks, and variables

### Linting

Run all linters before submitting:

```bash
# Ansible lint
ansible-lint

# YAML lint
yamllint .

# Python lint
flake8 . --max-line-length=120 --extend-ignore=E203,W503
```

## Testing

### Running Unit Tests

```bash
pytest tests/unit/ -v
```

### Running Integration Tests

```bash
ansible-playbook tests/integration/test_integration.yml --extra-vars "stargate_server=https://your-server.com"
```

### Running Molecule Tests

```bash
cd tests/molecule/default
molecule test
```

Or for a faster converge only:
```bash
molecule converge
```

### Running All CI Checks Locally

```bash
# Install CI dependencies
pip install ansible ansible-lint yamllint flake8 pytest pytest-ansible pyyaml

# Run all checks
ansible-lint
yamllint .
flake8 . --max-line-length=120 --extend-ignore=E203,W503
pytest tests/unit/ -v
```

## Pull Request Process

1. Ensure all tests pass and linters are clean.
2. Update documentation if your change affects usage.
3. Add entries to `CHANGELOG.md` under an appropriate heading (Added, Changed, Fixed, Removed).
4. Your PR should target the `master` branch.
5. PRs require at least one review before merging.

## Module Documentation

When adding or modifying modules, update the `DOCUMENTATION` string with:

```python
DOCUMENTATION = '''
module: module_name
author: Your Name
short_description: One-line description
description:
  - Longer description of what the module does
options:
  parameter_name:
    description:
      - Description of the parameter
    type: str
    required: true
    aliases: []
extends_documentation_fragment:
  - company.stargate.stargate
'''
```

## Reporting Issues

When reporting issues, include:
- Ansible version
- Python version
- Collection version
- Full error message and traceback
- Minimal reproduction case

## Questions

For questions or discussions, open an issue with the label `question`.

---

Thank you for contributing to ansible-stargate!