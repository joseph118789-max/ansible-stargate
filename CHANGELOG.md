# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added
- Initial release of ansible-stargate collection
- `stargate_login` module for authentication with Stargate API
- `stargate_logout` module for session termination
- `stargate_get` module for GET requests to Stargate API
- `stargate_post` module for POST requests to Stargate API
- `stargate_put` module for PUT requests to Stargate API
- `stargate_delete` module for DELETE requests to Stargate API
- `stargate_service` module for service management
- `stargate_node` module for node management
- `stargate_alarm` module for alarm management
- `stargate_utils` module_utils with shared functions for API communication
- Retry logic with configurable retries and delay for API calls
- Token-based authentication with Bearer token support
- Support for custom headers and API versioning
- Integration test playbook
- Molecule test scenario for containerized testing
- Unit tests for stargate_utils module
- CI/CD workflow with ansible-lint, yamllint, flake8, and pytest
- Contributing guide and changelog documentation