# Changelog

All notable changes to the `company.stargate` collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-05-19

### Added

#### Modules (11)
- `stargate_login` - Authentication and session management
- `stargate_logout` - Session termination
- `stargate_get` - Generic GET requests
- `stargate_post` - Generic POST requests (create resources)
- `stargate_put` - Generic PUT requests (update resources)
- `stargate_delete` - Generic DELETE requests (remove resources)
- `stargate_user` - User management operations
- `stargate_connection` - Connection management
- `stargate_account` - Account management
- `stargate_alarm` - Alarm monitoring
- `stargate_node` - Node discovery and management
- `stargate_service` - Service management

#### Roles (10)
- `login` - Authentication, token management, session renewal
- `alarms` - Alarm monitoring, filtering, clearing, archiving
- `nodes` - Node discovery, status checks, config backup
- `services` - Service management, health checks
- `backup` - Configuration backup and restore
- `monitoring` - Metrics polling, dashboard export
- `reports` - Report generation, export
- `user` - User CRUD, group management
- `connection` - Connection CRUD, protocol management
- `account` - Account profile management

#### Playbooks (5)
- `user-management.yml` - User management workflow
- `connection-management.yml` - Connection management workflow
- `account-management.yml` - Account management workflow
- `alarm-workflow.yml` - Alarm monitoring workflow
- `daily-report.yml` - Daily operations reporting

#### Tests
- 123 unit tests (all passing)
- Integration test playbooks (negative, idempotency, timeout)
- 3 Molecule scenarios (default, connection, user)
- API test suite

#### Documentation
- `README.md` - Collection overview and usage guide
- `galaxy.yml` - Collection metadata
- `API_ENDPOINTS.md` - Complete API documentation (88 endpoints)
- `TROUBLESHOOTING.md` - Common issues and solutions
- `TROUBLESHOOTING.md` - Error handling guide

#### CI/CD
- GitHub Actions workflow with:
  - ansible-lint
  - yamllint
  - flake8
  - pytest with coverage
  - Integration tests
  - Molecule tests
  - Collection build & validation

### Known Issues

1. **GWT-RPC Login:** XSRF protection prevents CLI access. Use REST API instead.
2. **HTTP 500 Errors:** Several endpoints (alarm, node, service, backup, reports) return 500 due to Java NPE bugs in the Stargate server.
3. **Account Creation:** Some account creation endpoints fail with NPE in `SshKeyPolicyService` and `AccountProfileSettingService`.
4. **Pagination:** Must use string parameters (`"0"`) not integers (`0`) or API returns 500.

### API Coverage

| Category | Endpoints | Working |
|----------|-----------|---------|
| User Management | 12 | 8 |
| Connection Management | 8 | 8 |
| Account Management | 4 | 3 |
| Resource Management | 6 | 6 |
| Monitoring | 2 | 2 |
| Alarm Management | 2 | 0 |
| Node Management | 2 | 0 |
| Service Management | 1 | 0 |
| Backup | 1 | 0 |
| Reports | 1 | 0 |
| **Total** | **88** | **28** |

### Dependencies

- Ansible >= 2.9
- Python >= 3.8
- requests
- PyYAML

### License

GPL-3.0-or-later

---

## Release Checklist

- [x] Modules implemented (11/11)
- [x] Roles implemented (10/10)
- [x] Playbooks implemented (5/5)
- [x] Unit tests passing (123/123)
- [x] Integration tests created
- [x] Molecule scenarios created
- [x] Documentation complete
- [x] CI/CD pipeline configured
- [x] galaxy.yml metadata
- [x] README.md
- [x] CHANGELOG.md
- [x] LICENSE (GPL-3.0)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-19 | Initial release |