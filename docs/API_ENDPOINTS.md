# Stargate REST API v11.7.0 - Complete Endpoint Reference

**Source:** MasterSAM REST API Documentation (official HTML) + DB Analysis  
**Server:** https://10.201.208.160:8443  
**Base Path:** /adama/rest/{endpoint}  
**Auth:** base64(username:token) as Bearer token

---

## Authentication

Stargate uses **Bearer token** authentication with format: `base64(username:token)`

```python
import base64

token = "ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c"
auth_b64 = base64.b64encode(token.encode()).decode()

headers = {
    "Authorization": f"Bearer {auth_b64}",
    "Content-Type": "application/json"
}
```

---

## API Profile Structure

The Stargate API uses a profile-based access control model:

| Table | Description |
|-------|-------------|
| `API_PROFILE` | Defines profiles (e.g., "default") |
| `API_COMMAND` | Maps commands to profiles (88 commands in default) |
| `API_USER` | API users mapped to profiles |
| `API_COMMAND_ACCESS_CONTROL` | Per-resource ACLs (empty = allow all) |

**Default Profile:** `8bb8cf1a-4a63-11eb-b378-0242ac130002`
- Contains 88 allowed API commands
- All commands have `ALLOW=1` and `ALLOW_ALL_ACCOUNTS=1`

---

## Endpoint Classification

| Type | Description | Status |
|------|-------------|--------|
| **READ** | Retrieve/list data | ✅ Working via Ansible module |
| **WRITE** | Create/update/delete operations | ⚠️ Requires proper request body |

---

## READ-Only Endpoints (17 - Fully Verified Working)

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `userGet` | POST | Retrieve list of users | `{"user": [...], "errorMsg": null}` |
| `userCount` | POST | Get total user count | `{"message": "2", "errorMsg": null}` |
| `userGetByUsername` | POST | Retrieve user by username | `{"user": {...}, "errorMsg": null}` |
| `userMonitoringCount` | POST | Get monitored user count | `{"message": "0", "errorMsg": null}` |
| `userCommonGet` | POST | Retrieve common users | `{"user": [...], "errorMsg": null}` |
| `userGetLastLogin` | POST | Get user's last login | ⚠️ Returns HTTP 500 |
| `connectionGet` | POST | Retrieve list of connections | `{"connection": [...], "errorMsg": null}` |
| `connectionCount` | POST | Get total connection count | `{"message": "0", "errorMsg": null}` |
| `connectionMonitoringCount` | POST | Get monitored connection count | `{"message": "0", "errorMsg": null}` |
| `connectionDeleteAll` | POST | Delete all connections | ⚠️ Use with caution |
| `accountCommonGet` | POST | Retrieve list of accounts | `{"account": [...], "errorMsg": null}` |
| `accountWorkflowProfileGet` | POST | Retrieve workflow profiles | `{"accountWorkflowProfile": [...], "errorMsg": null}` |
| `accountPasswordGet` | POST | Get account passwords | ⚠️ HTTP 400 - needs valid ID |
| `accountInsecurePasswordGet` | POST | Get insecure passwords | ⚠️ HTTP 400 |
| `accountKeyGet` | POST | Get account keys | ⚠️ HTTP 400 |
| `approvedConnectionGet` | POST | Retrieve approved connections | `{"approvedConnection": [...], "errorMsg": null}` |
| `approvedConnectionCount` | POST | Get approved connection count | `{"message": "0", "errorMsg": null}` |
| `connectionAuthorizationGet` | POST | Retrieve connection authorizations | `{"connectionAuthorization": [...], "errorMsg": null}` |
| `connectionGroupGet` | POST | Retrieve connection groups | `{"connectionGroup": [...], "errorMsg": null}` |
| `userGroupGet` | POST | Retrieve user groups | `{"userGroup": [...], "errorMsg": null}` |
| `userUserGroupGet` | POST | Retrieve user-to-group mappings | `{"userGroup": [...], "errorMsg": null}` |

---

## WRITE Endpoints (Require Proper Request Body)

| Endpoint | Issue |
|----------|-------|
| `userCreate` | HTTP 500 - missing required fields |
| `userUpdate` | HTTP 500 - missing required fields |
| `userDelete` | HTTP 500 - missing required fields |
| `userUpdateQr` | HTTP 500 - missing required fields |
| `userCommonCreate` | HTTP 500 |
| `userCommonUpdate` | HTTP 500 |
| `userGroupCreate` | HTTP 500 |
| `userGroupUpdate` | HTTP 500 |
| `userGroupDelete` | HTTP 500 |
| `userUserGroupAdd` | HTTP 500 |
| `userUserGroupRemove` | HTTP 500 |
| `connectionCreate` | HTTP 500 - missing required fields |
| `connectionDelete` | HTTP 500 - missing required fields |
| `connectionExport` | HTTP 500 |
| `connectionPasswordGet` | HTTP 404 - connection not found |
| `connectionPasswordReset` | HTTP 500 |
| `accountCreate` | HTTP 500 - missing required fields |
| `accountDelete` | HTTP 400 - invalid account name |
| `accountUpdate` | HTTP 404 - account not found |
| `accountKeyCreate` | HTTP 400 - missing IV parameter |
| `accountPasswordPlainCreate` | HTTP 403 - password policy |
| `accountWorkflowProfileCreate` | HTTP 500 |
| `accountWorkflowProfileDelete` | HTTP 500 |
| `accountWorkflowProfileUpdate` | HTTP 500 |
| `accountSettingProfileCreate` | HTTP 404 - endpoint not found |
| `accountSettingProfileDelete` | HTTP 404 - endpoint not found |
| `accountSettingProfileUpdate` | HTTP 404 - endpoint not found |
| `approvedConnectionCreate` | HTTP 500 |
| `approvedConnectionDelete` | HTTP 500 |
| `connectionAuthorizationCreate` | HTTP 500 |
| `connectionAuthorizationDelete` | HTTP 404 - not found |
| `connectionAuthorizationConnectionGroupAdd` | HTTP 500 |
| `connectionAuthorizationRemoveConnectionGroups` | HTTP 500 |
| `connectionAuthorizationRemoveUserGroups` | HTTP 500 |
| `connectionAuthorizationUserGroupAdd` | HTTP 500 |
| `connectionGroupCreate` | HTTP 500 |
| `connectionGroupDelete` | HTTP 500 |
| `connectionGroupUpdate` | HTTP 500 |
| `resourceUnixCreate` | HTTP 500 - "address cannot be null" |
| `resourceOracleCreate` | HTTP 500 - "address cannot be null" |
| `resourceWindowsCreate` | HTTP 500 - "address cannot be null" |
| `resourceCiscoCreate` | HTTP 500 - "address cannot be null" |
| `resourceAs` | HTTP 404 - endpoint not found |
| `resourceSqlCreate` | HTTP 404 - endpoint not found |
| `accountRequestApproveEmail` | HTTP 400 |
| `approveRequest` | HTTP 500 - "Request Id cannot be null" |
| `cancelRequest` | HTTP 500 - "Request Id cannot be null" |
| `createRequest` | HTTP 500 - "Cannot invoke \"String.isEmpty()\"" |
| `custodianPasswordGet` | HTTP 500 |
| `passwordPolicyCreate` | HTTP 500 |
| `scheduleProfileCreate` | HTTP 500 - "name cannot be null" |
| `sshKeyPolicyCreate` | HTTP 500 |
| `workflowProfileCreate` | HTTP 500 |

---

## API Command Reference (88 commands in default profile)

| Command | ALLOW | ALLOW_ALL_ACCOUNTS |
|---------|-------|-------------------|
| accountCommonGet | 1 | 1 |
| accountCreate | 1 | 1 |
| accountDelete | 1 | 1 |
| accountGetByName | 1 | 1 |
| accountImport | 1 | 1 |
| accountInsecurePasswordGet | 1 | 1 |
| accountKeyCreate | 1 | 1 |
| accountKeyGet | 1 | 1 |
| accountKeyImport | 1 | 1 |
| accountPasswordGet | 1 | 1 |
| accountPasswordImport | 1 | 1 |
| accountPasswordPlainCreate | 1 | 1 |
| accountProfileSettingCreate | 1 | 1 |
| accountProfileSettingDelete | 1 | 1 |
| accountProfileSettingImport | 1 | 1 |
| accountProfileSettingUpdate | 1 | 1 |
| accountRequestApproveEmail | 1 | 1 |
| accountRequestIntegration | 1 | 1 |
| accountWorkflowProfileCreate | 1 | 1 |
| accountWorkflowProfileDelete | 1 | 1 |
| accountWorkflowProfileGet | 1 | 1 |
| accountWorkflowProfileImport | 1 | 1 |
| accountWorkflowProfileUpdate | 1 | 1 |
| accountUpdate | 1 | 1 |
| approvedConnectionCount | 1 | 1 |
| approvedConnectionCreate | 1 | 1 |
| approvedConnectionDelete | 1 | 1 |
| approvedConnectionGet | 1 | 1 |
| connectionAuthorizationConnectionGroupAdd | 1 | 1 |
| connectionAuthorizationCreate | 1 | 1 |
| connectionAuthorizationDelete | 1 | 1 |
| connectionAuthorizationGet | 1 | 1 |
| connectionAuthorizationRemoveConnectionGroups | 1 | 1 |
| connectionAuthorizationRemoveUserGroups | 1 | 1 |
| connectionAuthorizationUserGroupAdd | 1 | 1 |
| connectionCount | 1 | 1 |
| connectionCreate | 1 | 1 |
| connectionDelete | 1 | 1 |
| connectionDeleteAll | 1 | 1 |
| connectionExport | 1 | 1 |
| connectionGet | 1 | 1 |
| connectionGroupCreate | 1 | 1 |
| connectionGroupDelete | 1 | 1 |
| connectionGroupGet | 1 | 1 |
| connectionGroupImport | 1 | 1 |
| connectionGroupUpdate | 1 | 1 |
| connectionImport | 1 | 1 |
| connectionMonitoringCount | 1 | 1 |
| connectionPasswordGet | 1 | 1 |
| connectionPasswordReset | 1 | 1 |
| createRequest | 1 | 1 |
| custodianPasswordGet | 1 | 1 |
| passwordPolicyCreate | 1 | 1 |
| passwordPolicyImport | 1 | 1 |
| scheduleProfileCreate | 1 | 1 |
| scheduleProfileImport | 1 | 1 |
| sshKeyPolicyCreate | 1 | 1 |
| sshKeyPolicyImport | 1 | 1 |
| updateSecretAws | 1 | 1 |
| updateSecretAzure | 1 | 1 |
| approveRequest | 1 | 1 |
| cancelRequest | 1 | 1 |
| requireTotp | 1 | 1 |
| resourceAppBuilderSshImport | 1 | 1 |
| resourceAs400Create | 1 | 1 |
| resourceAs400Import | 1 | 1 |
| resourceCiscoCreate | 1 | 1 |
| resourceCiscoImport | 1 | 1 |
| resourceOracleCreate | 1 | 1 |
| resourceOracleImport | 1 | 1 |
| resourceSqlCreate | 1 | 1 |
| resourceSqlImport | 1 | 1 |
| resourceUnixCreate | 1 | 1 |
| resourceUnixImport | 1 | 1 |
| resourceWindowsCreate | 1 | 1 |
| resourceWindowsImport | 1 | 1 |
| resourceWindowsUserImport | 1 | 1 |
| userCommonCreate | 1 | 1 |
| userCommonGet | 1 | 1 |
| userCommonUpdate | 1 | 1 |
| userCount | 1 | 1 |
| userCreate | 1 | 1 |
| userDelete | 1 | 1 |
| userGet | 1 | 1 |
| userGetByUsername | 1 | 1 |
| userGetLastLogin | 1 | 1 |
| userGroupCreate | 1 | 1 |
| userGroupDelete | 1 | 1 |
| userGroupGet | 1 | 1 |
| userGroupImport | 1 | 1 |
| userGroupUpdate | 1 | 1 |
| userImport | 1 | 1 |
| userMonitoringCount | 1 | 1 |
| userUpdate | 1 | 1 |
| userUpdateQr | 1 | 1 |
| userUserGroupAdd | 1 | 1 |
| userUserGroupGet | 1 | 1 |
| userUserGroupRemove | 1 | 1 |
| workflowProfileCreate | 1 | 1 |
| workflowProfileImport | 1 | 1 |

---

## Test Script

Run the comprehensive API test suite:

```bash
cd ansible-stargate && python3 tests/api_test_suite.py
```

---

## Notes

- All endpoints use POST method with JSON body (even for GET operations)
- Body parameters `start` and `length` control pagination
- Error responses include `errorMsg` field
- SSL verification disabled for self-signed certificates
- WRITE operations return HTTP 500 when request body is missing required fields