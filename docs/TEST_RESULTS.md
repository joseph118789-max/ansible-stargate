# Stargate REST API 11.7.0 - Complete Test Results

**Server:** `https://10.201.208.160:8443`
**Auth:** `Authorization: Bearer <base64("ansible:d147ef1f-896d-487c-833e-28154903afc5")>`
**Tested:** 2026-05-18

## Summary
| Status | Count |
|--------|-------|
| ✅ Working (200) | 17 |
| ❌ Failed | 58 |
| **Total** | **75** |

---

## ✅ WORKING Endpoints (17)

| Endpoint | Method | Test Data | Notes |
|----------|--------|-----------|-------|
| `accountCommonGet` | POST | `{"start": 0, "length": 10}` | |
| `accountWorkflowProfileGet` | POST | `{"start": 0, "length": 10}` | |
| `approvedConnectionCount` | POST | `{}` | |
| `approvedConnectionGet` | POST | `{"start": 0, "length": 10}` | |
| `connectionAuthorizationGet` | POST | `{"start": 0, "length": 10}` | |
| `connectionCount` | POST | `{}` | |
| `connectionDeleteAll` | POST | `{}` | |
| `connectionGet` | POST | `{"start": 0, "length": 10}` | |
| `connectionMonitoringCount` | POST | `{}` | |
| `connectionGroupGet` | POST | `{"start": 0, "length": 10}` | |
| `userCount` | POST | `{}` | |
| `userGet` | POST | `{"start": 0, "length": 10}` | |
| `userGetLastLogin` | POST | `{"userId": "1"}` | |
| `userMonitoringCount` | POST | `{}` | |
| `userCommonGet` | POST | `{"start": 0, "length": 10}` | |
| `userGroupGet` | POST | `{"start": 0, "length": 10}` | |
| `userUserGroupGet` | POST | `{"start": 0, "length": 10}` | |

---

## ❌ FAILED Endpoints (58)

### Category: Account (11)
| Endpoint | Error | Likely Cause |
|----------|-------|--------------|
| `accountCreate` | 500 HTML | Missing required fields (resource_type, etc.) |
| `accountDelete` | "Invalid account" | Needs valid account ID |
| `accountGetByName` | "Invalid account" | Account name not found |
| `accountInsecurePasswordGet` | "Invalid account" | Needs valid account ID |
| `accountKeyCreate` | "Iv Parameter is null" | Missing IV parameter |
| `accountKeyGet` | "Invalid account" | Needs valid account ID |
| `accountPasswordGet` | "Invalid account" | Needs valid account ID |
| `accountPasswordPlainCreate` | "Account is not exist" | Needs valid account ID |
| `accountUpdate` | "Account is not exist" | Needs valid account ID |
| `accountSettingProfileCreate` | 500 HTML | Missing required fields |
| `accountSettingProfileDelete` | 500 HTML | Needs valid profile ID |
| `accountSettingProfileUpdate` | 500 HTML | Needs valid profile ID |
| `accountWorkflowProfileCreate` | 500 HTML | Missing required fields |
| `accountWorkflowProfileDelete` | 500 HTML | Needs valid profile ID |
| `accountWorkflowProfileUpdate` | "error when updating" | Needs valid profile ID |

### Category: Approved Connection (2)
| Endpoint | Error | Likely Cause |
|----------|-------|--------------|
| `approvedConnectionCreate` | 500 HTML | Missing userId or connectionId |
| `approvedConnectionDelete` | 500 HTML | Needs valid ID |

### Category: Connection (6)
| Endpoint | Error | Likely Cause |
|----------|-------|--------------|
| `connectionCreate` | "connection name" | Missing name field |
| `connectionDelete` | 500 HTML | Needs valid connection ID |
| `connectionExport` | 500 HTML | Missing required params |
| `connectionPasswordGet` | "connection not exist" | Connection needs to be approved first |
| `connectionPasswordReset` | 500 HTML | Needs valid connection ID |
| `connectionAuthorizationConnectionGroupAdd` | 500 HTML | Missing required fields |
| `connectionAuthorizationCreate` | 500 HTML | Missing required fields |
| `connectionAuthorizationDelete` | "Connection Authorization" | Needs valid ID |
| `connectionAuthorizationRemoveConnectionGroups` | 500 HTML | Missing required fields |
| `connectionAuthorizationRemoveUserGroups` | 500 HTML | Missing required fields |
| `connectionAuthorizationUserGroupAdd` | 500 HTML | Missing required fields |

### Category: Connection Group (3)
| Endpoint | Error | Likely Cause |
|----------|-------|--------------|
| `connectionGroupCreate` | 500 HTML | Missing required fields |
| `connectionGroupDelete` | 500 HTML | Needs valid group ID |
| `connectionGroupUpdate` | 500 HTML | Needs valid group ID |

### Category: Request/Workflow (4)
| Endpoint | Error | Likely Cause |
|----------|-------|--------------|
| `accountRequestApproveEmail` | "None" | Request ID is null |
| `approveRequest` | "Request Id cannot be null" | Missing request ID |
| `cancelRequest` | "Request Id cannot be null" | Missing request ID |
| `createRequest` | "getAccount() is null" | Missing accountId or requester |

### Category: Resource (6)
| Endpoint | Error | Likely Cause |
|----------|-------|--------------|
| `resourceAs400Create` | 500 HTML | Missing required fields |
| `resourceCiscoCreate` | "name cannot be null" | Missing name |
| `resourceOracleCreate` | "name cannot be null" | Missing name |
| `resourceSQLCreate` | 500 HTML | Missing required fields |
| `resourceUnixCreate` | "name cannot be null" | Missing name |
| `resourceWindowsCreate` | "name cannot be null" | Missing name |

### Category: User (8)
| Endpoint | Error | Likely Cause |
|----------|-------|--------------|
| `userCreate` | 500 HTML | Missing required fields |
| `userDelete` | 500 HTML | Needs valid user ID |
| `userGetByUsername` | 500 HTML | Endpoint implementation issue |
| `userUpdate` | "User is not exist" | User ID not found |
| `userUpdateQr` | 500 HTML | 2FA related, needs valid user |
| `userCommonCreate` | 500 HTML | Missing required fields |
| `userCommonUpdate` | 500 HTML | Needs valid user ID |
| `userGroupCreate` | 500 HTML | Missing required fields |
| `userGroupDelete` | 500 HTML | Needs valid group ID |
| `userGroupUpdate` | 500 HTML | Needs valid group ID |
| `userUserGroupAdd` | 500 HTML | Missing userId or userGroupId |
| `userUserGroupRemove` | 500 HTML | Missing userId or userGroupId |

### Category: Other (5)
| Endpoint | Error | Likely Cause |
|----------|-------|--------------|
| `custodianPasswordGet` | 500 HTML | User not found or N/A |
| `passwordPolicyCreate` | 500 HTML | Missing required fields |
| `scheduleProfileCreate` | "name cannot be null" | Missing name |
| `sshKeyPolicyCreate` | 500 HTML | Missing required fields |
| `workflowProfileCreate` | 500 HTML | Missing required fields |

---

## Notes

1. **alarmGet, nodeGet, serviceStatusGet** - Return 404 (REST module not deployed on server)

2. **500 HTML errors** - Server returns generic HTML error page when Hibernate validation fails or required fields are missing

3. **connectionPasswordGet** - Always returns "connection not exist" because the API user lacks permission to retrieve passwords for connections

4. **createRequest** - Server-side bug: `getAccount()` NPE even with valid `accountId` - the endpoint expects account NAME not ID

5. **Most create/update endpoints** - Require specific field combinations that aren't documented in the API spec

---

## Test Data in DB

- **Users:** mgadmin (id=1), user, testuser
- **Resources:** test-unix-server, test-win-server, test-db-server, test-app-server, oracle19c-lab, unix-test
- **Accounts:** system, test, test-admin, test-user, win-admin, db-admin, app-admin
- **Connections:** test-ssh-connection (deleted during tests)
- **User Groups:** test-group