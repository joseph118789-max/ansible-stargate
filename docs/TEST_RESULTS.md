# Stargate REST API 11.7.0 - Complete Test Results

**Server:** `https://10.201.208.160:8443`
**Auth:** `Authorization: Bearer <base64("ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c")>`
**Test Date:** 2026-05-18

## Summary
| Status | Count |
|--------|-------|
| ✅ Working (200) | **27** |
| ❌ Failed | **48** |
| **Total** | **75** |

---

## ✅ WORKING Endpoints (27)

### Account
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `accountCommonGet` | POST | `{"start": 0, "length": 10}` |

### Account Workflow Profile
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `accountWorkflowProfileGet` | POST | `{"start": 0, "length": 10}` |

### Approved Connection
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `approvedConnectionCount` | POST | `{}` |
| `approvedConnectionGet` | POST | `{"start": 0, "length": 10}` |

### Connection
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `connectionCount` | POST | `{}` |
| `connectionDeleteAll` | POST | `{}` |
| `connectionExport` | POST | `{"fileOuput": "/tmp/conexport.csv"}` |
| `connectionGet` | POST | `{"start": 0, "length": 10}` |
| `connectionMonitoringCount` | POST | `{}` |

### Connection Authorization
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `connectionAuthorizationGet` | POST | `{"start": 0, "length": 10}` |

### Connection Group
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `connectionGroupCreate` | POST | `{"name": "SSH Admin"}` |
| `connectionGroupGet` | POST | `{"start": 0, "length": 10}` |

### Resources
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `resourceOracleCreate` | POST | Full doc format (type=Oracle) |

### User
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `userCount` | POST | `{}` |
| `userGet` | POST | `{"start": 0, "length": 10}` |
| `userGetByUsername` | POST | `{"username": "mgadmin"}` |
| `userGetLastLogin` | POST | `{"start": "0", "length": "5"}` |
| `userMonitoringCount` | POST | `{}` |
| `userUpdate` | POST | Full doc format with `id` + all fields |
| `userUpdateQr` | POST | `{"name": "username"}` |

### User Common
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `userCommonCreate` | POST | `{"username": "name", "displayName": "Name", "isActive": "true", "emailAddress": "email@test.com"}` |
| `userCommonGet` | POST | `{"start": 0, "length": 10}` |

### User Group
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `userGroupCreate` | POST | `{"name": "NewUG"}` |
| `userGroupGet` | POST | `{"start": 0, "length": 10}` |
| `userUserGroupGet` | POST | `{"start": 0, "length": 10}` |

### Profile/Settings
| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `scheduleProfileCreate` | POST | Full doc format (intervalType=Hours) |
| `sshKeyPolicyCreate` | POST | `{"name": "name", "typeOfKeyToGenerate": "RSA", "numberOfBits": "4096"}` |

---

## ❌ FAILED Endpoints (48)

### Account (16) - 500 errors / missing required fields
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `accountCreate` | 500 | Needs more fields |
| `accountDelete` | "Invalid account name or resource" | Resource/account not found |
| `accountGetByName` | "Invalid account name or resource" | Resource/account not found |
| `accountInsecurePasswordGet` | "Invalid account or resource" | Permission/resource issue |
| `accountKeyCreate` | "Invalid Iv Parameter" | IV file path issue |
| `accountKeyGet` | "Invalid account or resource" | Permission issue |
| `accountPasswordGet` | "Invalid account or resource" | Permission issue |
| `accountPasswordPlainCreate` | "Account is not exist" | Needs valid account |
| `accountUpdate` | "Account is not exist" | Needs valid account |
| `accountSettingProfileCreate` | 500 | Needs more fields |
| `accountSettingProfileDelete` | 500 | Profile not found |
| `accountSettingProfileUpdate` | 500 | Profile not found |
| `accountWorkflowProfileCreate` | 500 | Needs more fields |
| `accountWorkflowProfileDelete` | 500 | Profile not found |
| `accountWorkflowProfileUpdate` | "error when updating" | Profile not found |

### Approved Connection (2)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `approvedConnectionCreate` | 500 | Needs valid connection + user |
| `approvedConnectionDelete` | 500 | ID not found |

### Connection (4)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `connectionCreate` | 500 | Needs more fields from doc |
| `connectionDelete` | 500 | ID not found |
| `connectionPasswordGet` | "connection not exist" | Permission issue |
| `connectionPasswordReset` | 500 | Needs valid connection |

### Connection Authorization (6)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `connectionAuthorizationConnectionGroupAdd` | "Connection Authorization Id does not exist" | ID not found |
| `connectionAuthorizationCreate` | "User group does not exist" | Group name issue |
| `connectionAuthorizationDelete` | "Connection Authorization Id does not exist" | ID not found |
| `connectionAuthorizationRemoveConnectionGroups` | 500 | Needs valid IDs |
| `connectionAuthorizationRemoveUserGroups` | 500 | Needs valid IDs |
| `connectionAuthorizationUserGroupAdd` | "Connection Authorization Id does not exist" | ID not found |

### Connection Group (2)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `connectionGroupDelete` | "None" | ID not found |
| `connectionGroupUpdate` | "connection group id does not exists" | ID not found |

### Request/Workflow (4)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `accountRequestApproveEmail` | "None" | Request ID null |
| `approveRequest` | "This request id: 99999 is not valid" | Needs valid request ID |
| `cancelRequest` | "Request Id is not exist" | Needs valid request ID |
| `createRequest` | "error in creating request, Can" | Needs complete data |

### Resources (5)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `resourceAs400Create` | "resource type not exist" | AS400 type not supported |
| `resourceCiscoCreate` | "resource type not exist" | Cisco type not supported |
| `resourceSQLCreate` | 500 | SQL type needs more fields |
| `resourceUnixCreate` | "prompt statement cannot be null" | Needs `promptStatement` field |
| `resourceWindowsCreate` | "resource type not exist" | Windows type not supported |

### User (4)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `userCreate` | 500 | Needs more fields |
| `userDelete` | 500 | User ID not found |
| `userCommonUpdate` | "username already exist" | User already exists |
| `userUserGroupAdd` | "user group not exist" | Group name issue |
| `userUserGroupRemove` | "user does not belong to Custodian1" | Already removed |

### User Group (3)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `userGroupDelete` | "user group id does not exists" | ID not found |
| `userGroupUpdate` | "user group id does not exists" | ID not found |
| `userUserGroupRemove` | "user does not belong to Custodian1" | Not in group |

### Other (5)
| Endpoint | Error | Fix Required |
|----------|-------|--------------|
| `custodianPasswordGet` | "/opt/mastersam/etc/acts.conf" | Config file issue |
| `passwordPolicyCreate` | 500 | Needs more fields |
| `workflowProfileCreate` | 500 | Needs more fields |

---

## Key Learnings

### Working Data Formats (from API doc examples)

**userUpdate:**
```json
{"id": "50", "username": "Name", "displayName": "Name", "isAdmin": "true", ...}
```

**userCommonCreate:**
```json
{"username": "Aaron Taylor", "displayName": "Aaron", "isActive": "true", "emailAddress": "aaron@api.com"}
```

**resourceOracleCreate:**
```json
{"name": "Oracle Admin", "description": "oracle", "address": "192.168.56.180", "type": "Oracle", "user": "admin", "password": "PAsww0rd!@#$", "passwordPlainCheckbox": "false", "port": "1521", "databaseName": "XE"}
```

### Server Limitations
1. **alarmGet, nodeGet, serviceStatusGet** - 404 (REST module not deployed)
2. **connectionPasswordGet** - Always "connection not exist" - API user lacks permission
3. **Resource types** - Only Oracle works, AS400/Cisco/SQL/Windows/Unix return "resource type not exist"
4. **SSH Key operations** - Need actual key file paths on server

### Required Field Patterns
- **account*** uses `resourceName` + `accountName` (not IDs)
- **resourceCreate** needs `type` matching server-supported types
- **userUpdate** needs `id` field + full user object
- **createRequest** needs `requester` username (not ID) + resource + account names