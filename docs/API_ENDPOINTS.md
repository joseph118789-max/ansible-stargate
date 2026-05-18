# Stargate REST API v11.7.0 - Endpoint Mapping

## API Base URL
```
https://{server}:{port}/adama/rest/{endpoint}
```

## Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| Auth via MasterSAM UI | Browser-based | Session cookie + JWT token |

## Endpoint Categories

### Account (10 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `accountCommonGet` | GET | Retrieve accounts common data |
| `accountCreate` | POST | Create account |
| `accountDelete` | DELETE | Delete account |
| `accountGetByName` | GET | Get account by name |
| `accountInsecurePasswordGet` | GET | Retrieve account key |
| `accountKeyCreate` | POST | Create SSH Key for account |
| `accountKeyGet` | GET | Retrieve account SSH Key |
| `accountPasswordGet` | GET | Retrieve account password |
| `accountPasswordPlainCreate` | POST | Create password for account |
| `accountUpdate` | PUT | Update account |

### Account Setting Profile (3 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `accountSettingProfileCreate` | POST | Create setting profile |
| `accountSettingProfileDelete` | DELETE | Delete setting profile |
| `accountSettingProfileUpdate` | PUT | Update setting profile |

### Account Workflow Profile (4 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `accountWorkflowProfileCreate` | POST | Create workflow profile |
| `accountWorkflowProfileDelete` | DELETE | Delete workflow profile |
| `accountWorkflowProfileGet` | GET | Retrieve workflow profile |
| `accountWorkflowProfileUpdate` | PUT | Update workflow profile |

### Approved Connection (4 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `approvedConnectionCount` | GET | Count approved connections |
| `approvedConnectionCreate` | POST | Create approved connection |
| `approvedConnectionDelete` | DELETE | Delete approved connection |
| `approvedConnectionGet` | GET | Retrieve approved connection |

### Connection (10 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `connectionCount` | GET | Count connections |
| `connectionCreate` | POST | Create connection |
| `connectionDelete` | DELETE | Delete connection |
| `connectionDeleteAll` | DELETE | Delete all connections |
| `connectionExport` | POST | Export connections |
| `connectionGet` | GET | Retrieve connections |
| `connectionMonitoringCount` | GET | Count monitoring connections |
| `connectionPasswordGet` | GET | Retrieve connection password |
| `connectionPasswordReset` | POST | Reset connection password |

### Connection Authorization (7 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `connectionAuthorizationConnectionGroupAdd` | POST | Add connection group |
| `connectionAuthorizationCreate` | POST | Create connection authorization |
| `connectionAuthorizationDelete` | DELETE | Delete connection authorization |
| `connectionAuthorizationGet` | GET | Retrieve connection authorization |
| `connectionAuthorizationRemoveConnectionGroups` | POST | Remove connection groups |
| `connectionAuthorizationRemoveUserGroups` | POST | Remove user groups |
| `connectionAuthorizationUserGroupAdd` | POST | Add user group |

### Connection Group (4 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `connectionGroupCreate` | POST | Create connection group |
| `connectionGroupDelete` | DELETE | Delete connection group |
| `connectionGroupGet` | GET | Retrieve connection groups |
| `connectionGroupUpdate` | PUT | Update connection group |

### Request Workflow (4 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `accountRequestApproveEmail` | POST | Send approval email |
| `approveRequest` | POST | Approve request |
| `cancelRequest` | POST | Cancel request |
| `createRequest` | POST | Create request |

### Resources (6 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `resourceAs400Create` | POST | Create AS/400 resource |
| `resourceCiscoCreate` | POST | Create Cisco resource |
| `resourceOracleCreate` | POST | Create Oracle resource |
| `resourceSqlCreate` | POST | Create SQL resource |
| `resourceUnixCreate` | POST | Create Unix resource |
| `resourceWindowsCreate` | POST | Create Windows resource |

### User (9 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `userCount` | GET | Count users |
| `userCreate` | POST | Create user |
| `userDelete` | DELETE | Delete user |
| `userGet` | GET | Return all users |
| `userGetByUsername` | GET | Get user by username |
| `userGetLastLogin` | GET | Get user's last login |
| `userMonitoringCount` | GET | Count monitoring users |
| `userUpdate` | PUT | Update user |
| `userUpdateQr` | PUT | Update user QR code |

### User Common (3 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `userCommonCreate` | POST | Create user with common details |
| `userCommonGet` | GET | Return users with common info |
| `userCommonUpdate` | PUT | Update user's common details |

### User Group (7 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `userGroupCreate` | POST | Create user group |
| `userGroupDelete` | DELETE | Delete user group |
| `userGroupGet` | GET | Return user groups |
| `userGroupUpdate` | PUT | Update user group |
| `userUserGroupAdd` | POST | Add user to group |
| `userUserGroupGet` | GET | Return users and groups |
| `userUserGroupRemove` | POST | Remove user from group |

### Ungrouped (5 endpoints)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `custodianPasswordGet` | GET | Retrieve custodian password |
| `passwordPolicyCreate` | POST | Create password policy |
| `scheduleProfileCreate` | POST | Create schedule profile |
| `sshKeyPolicyCreate` | POST | Create SSH key policy |
| `workflowProfileCreate` | POST | Create workflow profile |

## Common Request/Response Patterns

### Pagination (accountCommonGet, userGet, connectionGet)
```json
// Request
{
  "start": "integer",
  "length": "integer"
}

// Response
{
  "account": [...],
  "total": "integer"
}
```

### Account Object
```json
{
  "id": "uuid",
  "name": "string",
  "resource": "string",
  "description": "string",
  "passwordPolicy": "string",
  "sshKeyPolicy": "string",
  "scheduleProfileVerify": "string",
  "scheduleProfileReset": "string",
  "scheduleProfileSshKeyReset": "string",
  "accountWorkflowProfile": ["string"],
  "disableManualPasswordResetPropagation": "boolean",
  "disableWorkflowPasswordResetTrigger": "boolean",
  "adminToResetPassword": "boolean",
  "requestorToViewPassword": "boolean",
  "enableEmailNotification": "string"
}
```

### User Object
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "fullName": "string",
  "isActive": "boolean",
  "userGroups": ["string"],
  "lastLogin": "datetime"
}
```

### Connection Object
```json
{
  "id": "uuid",
  "name": "string",
  "account": "string",
  "resource": "string",
  "host": "string",
  "port": "integer",
  "protocol": "string",
  "status": "string"
}
```

## Notes
- All endpoints use `/adama/rest/` prefix (NOT `/api/`)
- Authentication: Browser-based MasterSAM UI session + JWT
- API runs on port 8443 by default
- All requests return JSON
- Pagination uses `start` and `length` parameters