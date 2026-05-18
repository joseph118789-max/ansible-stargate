# Stargate REST API 11.7.0 - Complete Test Results (75 Endpoints)

**Server:** `https://10.201.208.160:8443`
**Auth:** `Authorization: Bearer <base64("ansible:d147ef1f-896d-487c-833e-28154903afc5")>`
**Test Date:** 2026-05-18

## Summary
| Status | Count |
|--------|-------|
| ✅ Working | **19** |
| ❌ Failed | **56** |
| **Total** | **75** |

---

## ✅ WORKING Endpoints (19)

| Endpoint | Method | Test Data |
|----------|--------|-----------|
| `accountCommonGet` | POST | `{"start": 0, "length": 10}` |
| `accountWorkflowProfileGet` | POST | `{"start": 0, "length": 10}` |
| `approvedConnectionCount` | POST | `{}` |
| `approvedConnectionGet` | POST | `{"start": 0, "length": 10}` |
| `connectionAuthorizationGet` | POST | `{"start": 0, "length": 10}` |
| `connectionCount` | POST | `{}` |
| `connectionDelete` | POST | `{"id": "<id>"}` |
| `connectionDeleteAll` | POST | `{}` |
| `connectionGet` | POST | `{"start": 0, "length": 10}` |
| `connectionMonitoringCount` | POST | `{}` |
| `connectionGroupCreate` | POST | `{"name": "api-conn-grp"}` |
| `connectionGroupGet` | POST | `{"start": 0, "length": 10}` |
| `userCount` | POST | `{}` |
| `userGet` | POST | `{"start": 0, "length": 10}` |
| `userMonitoringCount` | POST | `{}` |
| `userCommonGet` | POST | `{"start": 0, "length": 10}` |
| `userGroupCreate` | POST | `{"name": "api-ug"}` |
| `userGroupGet` | POST | `{"start": 0, "length": 10}` |
| `userUserGroupGet` | POST | `{"start": 0, "length": 10}` |

---

## ❌ FAILED Endpoints (56)

### Account (13)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `accountCreate` | 500 HTML | Missing required fields |
| `accountDelete` | "Invalid account" | Account not found by name |
| `accountGetByName` | "Invalid account" | Account not found by name |
| `accountInsecurePasswordGet` | "Invalid account" | Permission issue |
| `accountKeyCreate` | "Iv Parameter is null" | Missing IV param |
| `accountKeyGet` | "Invalid account" | Permission issue |
| `accountPasswordGet` | "Invalid account" | Permission issue |
| `accountPasswordPlainCreate` | "Account is not exist" | Needs valid account ID |
| `accountUpdate` | "Account is not exist" | Needs valid account ID |
| `accountSettingProfileCreate` | 500 HTML | Missing required fields |
| `accountSettingProfileDelete` | 500 HTML | Needs valid ID |
| `accountSettingProfileUpdate` | 500 HTML | Needs valid ID |
| `accountWorkflowProfileCreate` | 500 HTML | Missing required fields |
| `accountWorkflowProfileDelete` | 500 HTML | Needs valid ID |
| `accountWorkflowProfileUpdate` | "error when updating" | Needs valid ID |

### Approved Connection (2)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `approvedConnectionCreate` | 500 HTML | Missing required fields |
| `approvedConnectionDelete` | 500 HTML | Needs valid ID |

### Connection (6)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `connectionCreate` | 500 HTML | Missing required fields |
| `connectionExport` | 500 HTML | Missing required fields |
| `connectionPasswordGet` | "connection not exist" | Permission issue |
| `connectionPasswordReset` | 500 HTML | Needs valid ID |
| `connectionAuthorizationConnectionGroupAdd` | 500 HTML | Missing fields |
| `connectionAuthorizationCreate` | 500 HTML | Missing fields |
| `connectionAuthorizationDelete` | "Connection Authorization" | Needs valid ID |
| `connectionAuthorizationRemoveConnectionGroups` | 500 HTML | Missing fields |
| `connectionAuthorizationRemoveUserGroups` | 500 HTML | Missing fields |
| `connectionAuthorizationUserGroupAdd` | 500 HTML | Missing fields |

### Connection Group (2)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `connectionGroupDelete` | "None" | Needs valid group ID |
| `connectionGroupUpdate` | "connection group id does not exists" | Needs valid group ID |

### Request/Workflow (4)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `accountRequestApproveEmail` | "None" | Request ID null |
| `approveRequest` | "Request Id cannot be null" | Missing request ID |
| `cancelRequest` | "Request Id cannot be null" | Missing request ID |
| `createRequest` | "getAccount() is null" | Server NPE bug |

### Resource (6)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `resourceAs400Create` | 500 HTML | Missing required fields |
| `resourceCiscoCreate` | "String.toLowerCase() NPE" | Missing name |
| `resourceOracleCreate` | "String.toLowerCase() NPE" | Missing name |
| `resourceSQLCreate` | 500 HTML | Missing required fields |
| `resourceUnixCreate` | "String.toLowerCase() NPE" | Missing name |
| `resourceWindowsCreate` | "String.toLowerCase() NPE" | Missing name |

### User (8)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `userCreate` | 500 HTML | Missing required fields |
| `userDelete` | 500 HTML | Needs valid user ID |
| `userGetByUsername` | 500 HTML | Endpoint bug |
| `userGetLastLogin` | 500 HTML | Endpoint bug |
| `userUpdate` | 500 HTML | Needs valid user ID |
| `userUpdateQr` | 500 HTML | Needs valid user ID |
| `userCommonCreate` | 500 HTML | Missing required fields |
| `userCommonUpdate` | 500 HTML | Needs valid user ID |

### User Group (4)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `userGroupDelete` | "user group id does not exists" | Needs valid group ID |
| `userGroupUpdate` | 500 HTML | Needs valid group ID |
| `userUserGroupAdd` | 500 HTML | Missing fields |
| `userUserGroupRemove` | 500 HTML | Missing fields |

### Other (5)
| Endpoint | Error | Cause |
|----------|-------|-------|
| `custodianPasswordGet` | 500 HTML | Endpoint bug |
| `passwordPolicyCreate` | 500 HTML | Missing required fields |
| `scheduleProfileCreate` | "For input string: daily" | Wrong param type |
| `sshKeyPolicyCreate` | 500 HTML | Missing required fields |
| `workflowProfileCreate` | 500 HTML | Missing required fields |

---

## Notes

1. **alarmGet, nodeGet, serviceStatusGet** - Return 404 (REST module not deployed on server)

2. **500 HTML errors** - Server returns generic HTML when Hibernate validation fails

3. **"String.toLowerCase() NPE"** - Resource endpoints expect `resource_type` field but it's being called with `name=null`

4. **connectionPasswordGet** - Always "connection not exist" - API user lacks password retrieval permission

5. **createRequest** - Server-side bug: `getAccount()` NPE - needs ACCOUNT NAME not ID

6. **userGetByUsername, userGetLastLogin, custodianPasswordGet** - 500 HTML - endpoint implementation issue

---

## Test Data IDs Used
- **Connection ID:** 9f870988-5290-11f1-9b86-005056afa2d7 (test-ssh-conn)
- **User ID:** af48a024-528a-11f1-9b86-005056afa2d7 (testuser)
- **Account ID:** 8b906fda-528e-11f1-9b86-005056afa2d7 (app-admin)
- **User Group ID:** 00e94110-6f3c-4a7e-afaf-c95c54cf26c3 (test-group)
- **Resource Name:** test-unix-server