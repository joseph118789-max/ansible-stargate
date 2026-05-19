# Stargate REST API - Final Test Report
**Date:** 2026-05-18  
**Server:** https://10.201.208.160:8443  
**API Version:** 11.7.0

---

## Summary

| Category | Count |
|----------|-------|
| ✅ PASS | 16 |
| ❌ FAIL (Server Bug) | 8 |
| ⚠️  NOT FOUND (404) | 19 |
| ❌ BAD REQUEST (400) | 4 |
| **TOTAL TESTED** | **47** |

---

## ✅ Working Endpoints (16)

### READ Operations
| Endpoint | Method | Notes |
|----------|--------|-------|
| userGet | GET | Paginated: `{"start": 0, "length": 50}` |
| userCount | GET | Paginated |
| userCommonGet | GET | |
| userGroupGet | GET | |
| accountCommonGet | GET | |
| connectionGet | GET | |
| connectionCount | GET | |
| connectionAuthorizationGet | GET | |
| connectionGroupGet | GET | |
| approvedConnectionGet | GET | |
| approvedConnectionCount | GET | |

### CREATE Operations
| Endpoint | Method | Required Fields |
|----------|--------|-----------------|
| userGroupCreate | POST | `name`, `description` |
| connectionGroupCreate | POST | `name` |
| resourceUnixCreate | POST | `name`, `address`, `type: "Unix"`, `loginUser`, `password`, `promptStatement`, `privilegedPromptStatment` |
| resourceWindowsCreate | POST | `name`, `address`, `type: "aws-win-agent"`, `privilegedUser`, `privilegedPassword` |
| resourceOracleCreate | POST | `name`, `address`, `type: "ORACLE"`, `serviceName`, `user`, `password`, `port` |

---

## ❌ Server Bugs (Cannot Fix via API)

### accountCreate - HTTP 500
**Error:** `NullPointerException: Cannot invoke "String.toLowerCase()" because "name" is null`  
**Location:** `SshKeyPolicyService.retrieveByName()` line 88 and `AccountProfileSettingService.retrieveByName()` line 299  
**Root Cause:** Server-side Java bug - methods call `name.toLowerCase()` without null check  
**Fix Required:** Java source code patch

### userCreate / userDelete - HTTP 500
**Error:** HTML 500 Internal Server Error  
**Root Cause:** Server-side Java bug

---

## ⚠️  Not Found (404)

These endpoints are documented but NOT implemented in this API version:
- userLastLoginGet, userMonitoringGet
- connectionMonitoringGet
- resourceGet, resourceCount
- alarmGet, alarmCount, alarmHistoryGet
- nodeGet, nodeCount, nodeHistoryGet, nodeAlertGet
- serviceStatusGet, backupGet, reportsGet
- userAllGet, accountGet, accountAllGet, connectionAllGet
- auditTrailGet, auditTrailCount
- licenseGet, licenseCount, systemInfoGet
- resourceGroupGet, resourceGroupCount
- accountPasswordReset, accountPasswordVerify

---

## ❌ Bad Request (400)

These endpoints exist but require specific parameters or data:
- accountWorkflowProfileGet
- accountDelete
- connectionDeleteAll
- accountPasswordGet

---

## Authentication

**Format:** `Authorization: Bearer <base64("username:token")>`  
**Credentials:** `ansible:f8ab2c83-0bcb-4d15-b5da-afbc19cbb41c`  
**Base64:** `YW5zaWJsZTpkMTQ3ZWYxZi04OTZkLTQ4N2MtODMzZS0yODE1NDkwM2FmYzU=`

---

## Key Discoveries

### Field Name Typos in Server Code
The Java DTOs have typos that must be matched exactly:
- `privilegedPromptStatment` (not `privilegedPromptStatement`)

### Resource Types
- Unix: `type: "Unix"`
- Windows: `type: "aws-win-agent"`
- Oracle: `type: "ORACLE"`

### Password Policies
Available: `simple`, `Standard Password Policy`, `Strong Password Policy`

### SSH Key Policies
Available: `DSA 1024`, `RSA 2048`, `api-ssh-key`, `SSHKey999`
