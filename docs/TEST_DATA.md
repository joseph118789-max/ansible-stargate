# Stargate REST API 11.7.0 - Test Data Reference

## API Authentication
- **Format:** `Authorization: Bearer <base64(username:token)>`
- **Username:** `ansible`
- **Token:** `YOUR_TOKEN`
- **Base64:** `YW5zYmxlOmQxNDdlZGYxLTIxNDYtNDg3Yy04MzNlLTI4MTU0OTAzYWZjNQ==`

## Server
- **URL:** `https://YOUR_SERVER_IP:8443/adama/rest/{endpoint}`
- **Auth:** JAAS with Bearer token (base64 encoded)

---

## Working Endpoints (17)

### Account Endpoints
| Endpoint | Method | Test Data | Response |
|----------|--------|-----------|----------|
| `accountCommonGet` | GET | `{"start": 0, "length": 10}` | User list |
| `accountPasswordPlainCreate` | POST | `{"accountId": "<id>", "password": "TestPass123!"}` | Password set |
| `accountUpdate` | POST | `{"id": "<id>", "name": "updated"}` | Account updated |

### Approved Connection Endpoints
| Endpoint | Method | Test Data | Response |
|----------|--------|-----------|----------|
| `approvedConnectionCount` | GET | `{}` | Count: 0 |
| `approvedConnectionGet` | GET | `{"start": 0, "length": 10}` | Empty list |

### Connection Endpoints
| Endpoint | Method | Test Data | Response |
|----------|--------|-----------|----------|
| `connectionCount` | GET | `{}` | Count: 1 |
| `connectionDelete` | POST | `{"id": "<conn_id>"}` | Deleted |
| `connectionDeleteAll` | POST | `{}` | All deleted |
| `connectionGet` | GET | `{"start": 0, "length": 10}` | Connection list |
| `connectionMonitoringCount` | GET | `{}` | Count: 0 |

### Connection Group Endpoints
| Endpoint | Method | Test Data | Response |
|----------|--------|-----------|----------|
| `connectionGroupCreate` | POST | `{"name": "test-group"}` | Created |
| `connectionGroupGet` | GET | `{"start": 0, "length": 10}` | Group list |

### User Endpoints
| Endpoint | Method | Test Data | Response |
|----------|--------|-----------|----------|
| `userCount` | GET | `{}` | Count: 3 |
| `userGet` | GET | `{"start": 0, "length": 10}` | User list |
| `userMonitoringCount` | GET | `{}` | Count: 0 |

### User Common Endpoints
| Endpoint | Method | Test Data | Response |
|----------|--------|-----------|----------|
| `userCommonGet` | GET | `{"start": 0, "length": 10}` | User list |

### User Group Endpoints
| Endpoint | Method | Test Data | Response |
|----------|--------|-----------|----------|
| `userGroupCreate` | POST | `{"name": "test-group"}` | Created |
| `userGroupGet` | GET | `{"start": 0, "length": 10}` | Group list |
| `userUserGroupGet` | GET | `{"start": 0, "length": 10}` | User-group mapping |

---

## Endpoints Requiring Proper Data (44)

### Account Endpoints (need valid account ID)
```
accountDelete         → {"name": "system"} or {"id": "<id>"}
accountGetByName      → {"name": "system"}  (account must exist)
accountInsecurePasswordGet → {"accountId": "<valid_id>"}
accountKeyCreate      → {"accountId": "<valid_id>"} (needs IV parameter)
accountKeyGet         → {"accountId": "<valid_id>"}
accountPasswordGet    → {"accountId": "<valid_id>"} (API user lacks permission)
```

### Approved Connection Endpoints (need valid IDs)
```
approvedConnectionCreate → {
  "connectionId": "<valid_conn_id>",
  "userId": "<valid_user_id>",
  "duration": 60
}
approvedConnectionDelete → {"id": "<valid_id>"}
```

### Connection Endpoints (need valid data)
```
connectionCreate → {
  "name": "new-conn",
  "hostname": "192.168.1.50",
  "protocol": 1,  # SSH=1, RDP=2
  "port": 22,
  "username": "admin"
}
connectionPasswordGet → {"connectionId": "<valid_id>"} (needs approved connection)
connectionPasswordReset → {"connectionId": "<valid_id>"} (needs approved connection)
connectionExport → {} (may need params)
```

### Connection Group Endpoints (need valid group ID)
```
connectionGroupDelete → {"id": "<valid_group_id>"}
connectionGroupUpdate → {"id": "<valid_group_id>", "name": "new-name"}
```

### User Endpoints (need valid user data)
```
userCreate → {
  "username": "newuser",
  "password": "Password123!",
  "displayname": "New User",
  "isActive": true,
  "normalUser": true,
  "type": 0
}
userDelete → {"id": "<valid_user_id>"}
userGetByUsername → {"userName": "mgadmin"}  (returns 500 - endpoint issue)
userGetLastLogin → {"userId": "<valid_user_id>"}  (returns 500 - endpoint issue)
userUpdate → {"id": "<valid_user_id>", "displayname": "New Name"}
userUpdateQr → {"id": "<valid_user_id>"}  (2FA related)
```

### User Common Endpoints
```
userCommonCreate → {
  "username": "testuser",
  "displayname": "Test User",
  "type": 0
}  (returns 500 - needs more fields)
userCommonUpdate → {"id": "<valid_user_id>", ...}
```

### User Group Endpoints (need valid group ID)
```
userGroupDelete → {"id": "<valid_group_id>"}
userGroupUpdate → {"id": "<valid_group_id>", "name": "new-name"}
userUserGroupAdd → {"userId": "<valid_id>", "userGroupId": "<valid_id>"}
userUserGroupRemove → {"userId": "<valid_id>", "userGroupId": "<valid_id>"}
```

### Request Workflow Endpoints
```
accountRequestApproveEmail → {"id": "<valid_request_id>"}
approveRequest → {"id": "<valid_request_id>"}
cancelRequest → {"id": "<valid_request_id>"}
createRequest → {
  "type": "password",
  "accountId": "<valid_account_id>",
  "requester": "<valid_user_id>",
  "reason": "test request"
}
```

### Resource Endpoints (need resource_type)
```
resourceAs400Create → {"name": "as400", "address": "192.168.1.10", "resource_type": "AS400"}
resourceCiscoCreate → {"name": "cisco", "address": "192.168.1.11", "resource_type": "CISCO"}
resourceOracleCreate → {"name": "oracle", "address": "192.168.1.12", "resource_type": "ORACLE"}
resourceSQLCreate → {"name": "sql", "address": "192.168.1.13", "resource_type": "SQL"}
resourceUnixCreate → {"name": "unix", "address": "192.168.1.14", "resource_type": "UNIX"}
resourceWindowsCreate → {"name": "windows", "address": "192.168.1.15", "resource_type": "WINDOWS"}
```

### Ungrouped Endpoints
```
custodianPasswordGet → {"userId": "<valid_user_id>"}
passwordPolicyCreate → {"name": "policy", "minLength": 8, ...}
scheduleProfileCreate → {"name": "schedule", "interval": "daily", ...}
sshKeyPolicyCreate → {"name": "key-policy", ...}
workflowProfileCreate → {"name": "workflow", ...}
```

---

## Known Issues
1. **alarmGet, nodeGet, serviceStatusGet** - Return 404 (REST module not deployed)
2. **connectionPasswordGet** - Returns "connection not exist" even with valid ID (needs approved connection)
3. **userGetByUsername, userGetLastLogin** - Return 500 (endpoint implementation issue)
4. **Many create/update endpoints** - Return 500 due to missing required fields (not documented)

---

## Test Data Created
- **Users:** mgadmin, user, testuser
- **Resources:** test-unix-server, test-win-server, test-db-server, test-app-server
- **Accounts:** system, test, test-admin, test-user, win-admin, db-admin, app-admin
- **Connections:** test-ssh-connection (temporary, deleted during tests)
- **User Groups:** test-group, test-conn-group