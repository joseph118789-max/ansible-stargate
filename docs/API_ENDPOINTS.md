# Stargate REST API v11.7.0 - Complete Endpoint Reference

**Source:** MasterSAM REST API Documentation (official HTML)  
**Server:** https://10.201.208.160:8443  
**Base Path:** /adama/rest/{endpoint}  
**Auth:** base64(username:token) as Bearer token

---

## Authentication

Stargate uses **Bearer token** authentication with format: `base64(username:token)`

```python
import base64

token = "ansible:d147ef1f-896d-487c-833e-28154903afc5"
auth_b64 = base64.b64encode(token.encode()).decode()

headers = {
    "Authorization": f"Bearer {auth_b64}",
    "Content-Type": "application/json"
}
```

---

## Endpoint Summary

| Category | Count |
|----------|-------|
| Account | 10 |
| AccountSettingProfile | 3 |
| AccountWorkflowProfile | 4 |
| ApprovedConnection | 4 |
| Connection | 9 |
| ConnectionAuthorization | 7 |
| ConnectionGroup | 4 |
| RequestWorkflow | 4 |
| Resources | 6 |
| Ungrouped | 5 |
| User | 9 |
| UserCommon | 3 |
| UserGroup | 7 |
| **TOTAL** | **75** |

---

## Account (10 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `accountCommonGet` | GET | Retrieve account Common |
| `accountCreate` | POST | Create account |
| `accountDelete` | POST | Delete account |
| `accountGetByName` | GET | Retrieve account ByName |
| `accountInsecurePasswordGet` | GET | Retrieve account InsecurePassword |
| `accountKeyCreate` | POST | Create accountKey |
| `accountKeyGet` | GET | Retrieve account Key |
| `accountPasswordGet` | GET | Retrieve account Password |
| `accountPasswordPlainCreate` | POST | Create accountPasswordPlain |
| `accountUpdate` | POST | Update account |

## AccountSettingProfile (3 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `accountSettingProfileCreate` | POST | Create accountSettingProfile |
| `accountSettingProfileDelete` | POST | Delete accountSettingProfile |
| `accountSettingProfileUpdate` | POST | Update accountSettingProfile |

## AccountWorkflowProfile (4 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `accountWorkflowProfileCreate` | POST | Create accountWorkflowProfile |
| `accountWorkflowProfileDelete` | POST | Delete accountWorkflowProfile |
| `accountWorkflowProfileGet` | GET | Retrieve account WorkflowProfile |
| `accountWorkflowProfileUpdate` | POST | Update accountWorkflowProfile |

## ApprovedConnection (4 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `approvedConnectionCount` | GET | approvedConnectionCount |
| `approvedConnectionCreate` | POST | Create approvedConnection |
| `approvedConnectionDelete` | POST | Delete approvedConnection |
| `approvedConnectionGet` | GET | Retrieve approvedConnection |

## Connection (9 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `connectionCount` | GET | connectionCount |
| `connectionCreate` | POST | Create connection |
| `connectionDelete` | POST | Delete connection |
| `connectionDeleteAll` | POST | Delete connectionAll |
| `connectionExport` | POST | connectionExport |
| `connectionGet` | GET | Retrieve connection  |
| `connectionMonitoringCount` | GET | connectionMonitoringCount |
| `connectionPasswordGet` | GET | Retrieve connection Password |
| `connectionPasswordReset` | POST | connectionPasswordReset |

## ConnectionAuthorization (7 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `connectionAuthorizationConnectionGroupAdd` | POST | connectionAuthorizationConnectionGroupAdd |
| `connectionAuthorizationCreate` | POST | Create connectionAuthorization |
| `connectionAuthorizationDelete` | POST | Delete connectionAuthorization |
| `connectionAuthorizationGet` | GET | Retrieve connection Authorization |
| `connectionAuthorizationRemoveConnectionGroups` | POST | connectionAuthorizationRemoveConnectionGroups |
| `connectionAuthorizationRemoveUserGroups` | POST | connectionAuthorizationRemoveUserGroups |
| `connectionAuthorizationUserGroupAdd` | POST | connectionAuthorizationUserGroupAdd |

## ConnectionGroup (4 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `connectionGroupCreate` | POST | Create connectionGroup |
| `connectionGroupDelete` | POST | Delete connectionGroup |
| `connectionGroupGet` | GET | Retrieve connection Group |
| `connectionGroupUpdate` | POST | Update connectionGroup |

## RequestWorkflow (4 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `accountRequestApproveEmail` | POST | accountRequestApproveEmail |
| `approveRequest` | GET | approveRequest |
| `cancelRequest` | GET | cancelRequest |
| `createRequest` | POST | createRequest |

## Resources (6 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `resourceAs` | POST | resourceAs |
| `resourceCiscoCreate` | POST | Create resourceCisco |
| `resourceOracleCreate` | POST | Create resourceOracle |
| `resourceSQLCreate` | POST | Create resourceSQL |
| `resourceUnixCreate` | POST | Create resourceUnix |
| `resourceWindowsCreate` | POST | Create resourceWindows |

## Ungrouped (5 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `custodianPasswordGet` | GET | Retrieve custodianPassword |
| `passwordPolicyCreate` | POST | Create passwordPolicy |
| `scheduleProfileCreate` | POST | Create scheduleProfile |
| `sshKeyPolicyCreate` | POST | Create sshKeyPolicy |
| `workflowProfileCreate` | POST | Create workflowProfile |

## User (9 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `userCount` | GET | userCount |
| `userCreate` | POST | Create user |
| `userDelete` | POST | Delete user |
| `userGet` | GET | Retrieve user  |
| `userGetByUsername` | GET | Retrieve user ByUsername |
| `userGetLastLogin` | GET | Retrieve user LastLogin |
| `userMonitoringCount` | GET | userMonitoringCount |
| `userUpdate` | POST | Update user |
| `userUpdateQr` | POST | Update userQr |

## UserCommon (3 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `userCommonCreate` | POST | Create userCommon |
| `userCommonGet` | GET | Retrieve user Common |
| `userCommonUpdate` | POST | Update userCommon |

## UserGroup (7 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `userGroupCreate` | POST | Create userGroup |
| `userGroupDelete` | POST | Delete userGroup |
| `userGroupGet` | GET | Retrieve user Group |
| `userGroupUpdate` | POST | Update userGroup |
| `userUserGroupAdd` | POST | userUserGroupAdd |
| `userUserGroupGet` | GET | Retrieve user UserGroup |
| `userUserGroupRemove` | POST | userUserGroupRemove |

---

## Verified Working Endpoints

The following endpoints have been tested and confirmed working:

| Endpoint | Method | Status |
|----------|--------|--------|
| `userGet` | GET | ✅ Verified |
| `userCount` | GET | ✅ Verified |
| `connectionGet` | GET | ✅ Verified |
| `connectionCount` | GET | ✅ Verified |
| `connectionCreate` | POST | ✅ Verified |
| `connectionDelete` | POST | ✅ Verified |
| `accountPasswordGet` | GET | ✅ Verified |
| `accountPasswordPlainCreate` | POST | ✅ Verified |
| `accountCommonGet` | GET | ✅ Verified |
| `accountCreate` | POST | ✅ Verified |

---

## Example Usage

### Get Users
```bash
curl -sk -X POST https://10.201.208.160:8443/adama/rest/userGet \
  -H "Authorization: Bearer YW5zaWJsZTpkMTQ3ZWYxZi04OTZkLTQ4N2MtODMzZS0yODE1NDkwM2FmYzU=" \
  -H "Content-Type: application/json" \
  -d '{"start":"0","length":"10"}'
```

### Response Format
```json
{
  "user": [...],
  "errorMsg": null
}
```

---

## Notes

- All endpoints use POST method with JSON body (even for GET operations)
- Body parameters `start` and `length` control pagination
- Error responses include `errorMsg` field
- SSL verification disabled for self-signed certificates
