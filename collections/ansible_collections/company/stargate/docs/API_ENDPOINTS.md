# Stargate REST API v11.7.0 - Documentation

> Complete API reference for MasterSAM Stargate REST API v11.7.0

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Formats](#requestresponse-formats)
5. [Error Handling](#error-handling)
6. [Pagination](#pagination)
7. [Rate Limiting](#rate-limiting)

---

## Architecture Overview

```mermaid
graph TB
    subgraph Client
        A[Ansible Collection<br/>company.stargate]
        B[Custom Modules]
        C[Playbooks]
    end
    
    subgraph Stargate_API
        D[REST API<br/>/adama/rest/*]
        E[Web API<br/>/adama/client/api/*]
        F[GWT-RPC<br/>/adama/adama/auth]
    end
    
    subgraph Backend
        G[Tomcat<br/>Java Backend]
        H[MariaDB<br/>APP Database]
        I[MaxScale<br/>Database Proxy]
    end
    
    A -->|HTTPS| D
    A -->|Bearer Token| D
    C --> B
    B --> D
    D --> G
    G -->|JDBC| I
    I --> H
```

### System Components

| Component | Host | Port | Description |
|-----------|------|------|-------------|
| Stargate Server | YOUR_SERVER_IP | 8443 | Main application server |
| Tomcat | localhost | 8080 | Java servlet container |
| MariaDB | localhost | 3306 | Primary database |
| MaxScale | localhost | 4006 | Database proxy/load balancer |

---

## Authentication

```mermaid
sequenceDiagram
    participant Client
    participant Stargate_API
    participant Database
    
    Client->>Stargate_API: POST /adama/rest/userGet
    Note over Client,Stargate_API: Authorization: Bearer base64(user:token)
    
    Stargate_API->>Database: Validate token
    Database-->>Stargate_API: User found
    Stargate_API-->>Client: 200 OK + JSON response
```

### Authentication Methods

**REST API (Bearer Token):**

```bash
# Format: base64("username:token")
TOKEN=$(echo -n "ansible:YOUR_TOKEN" | base64)
# YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM=

curl -X POST https://YOUR_SERVER_IP:8443/adama/rest/userGet \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"start": "0", "length": "10"}'
```

**GWT-RPC (Browser Only):**
- Requires browser session with permutation headers
- Protected by XSRF token validation
- Cannot be used from CLI

### Token Format

| Field | Value |
|-------|-------|
| Username | ansible |
| Token | YOUR_TOKEN |
| Base64 | YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM= |
| Header | Authorization: Bearer YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM= |

---

## API Endpoints

### Base URL

```
https://YOUR_SERVER_IP:8443/adama/rest/
```

### Endpoint Categories

| Category | Count | Status |
|----------|-------|--------|
| User Management | 12 | ✅ Working |
| Connection Management | 8 | ✅ Working |
| Account Management | 4 | ✅ Working |
| Resource Management | 6 | ✅ Working |
| Alarm Management | 2 | ❌ Not Implemented |
| Node Management | 2 | ❌ Not Implemented |
| Service Management | 1 | ❌ Not Implemented |
| Backup | 1 | ❌ Not Implemented |
| Reports | 1 | ❌ Not Implemented |

---

### User Endpoints

#### userGet

**Purpose:** Retrieve list of users with pagination

**Method:** POST

**Endpoint:** `/adama/rest/userGet`

**Request:**
```json
{
  "userName": "mgadmin",
  "start": "0",
  "length": "10"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| userName | string | No | Filter by username |
| start | string | Yes | Pagination start (string!) |
| length | string | Yes | Page size (string!) |

**Response:**
```json
{
  "user": [
    {
      "id": "1",
      "username": "mgadmin",
      "type": "0",
      "isAdmin": "1",
      "isActive": "1"
    }
  ],
  "errorMsg": null
}
```

**Status Codes:**
| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 500 | Server Error (NPE) |

---

#### userCount

**Purpose:** Get total user count

**Method:** POST

**Endpoint:** `/adama/rest/userCount`

**Request:** `{}`

**Response:**
```json
{
  "message": "5",
  "errorMsg": null
}
```

---

#### userCreate

**Purpose:** Create new user

**Method:** POST

**Endpoint:** `/adama/rest/userCreate`

**Request:**
```json
{
  "username": "newuser",
  "password": "Password123",
  "type": "0"
}
```

**Response:**
```json
{
  "message": "created",
  "errorMsg": null
}
```

**Status Codes:**
| Code | Description |
|------|-------------|
| 201 | Created |
| 400 | Validation failed |
| 409 | User already exists |
| 500 | Server Error (NPE) |

---

#### userDelete

**Purpose:** Delete user

**Method:** POST

**Endpoint:** `/adama/rest/userDelete`

**Request:**
```json
{
  "userName": "olduser"
}
```

**Response:**
```json
{
  "message": "deleted",
  "errorMsg": null
}
```

---

#### userGroupCreate

**Purpose:** Create user group

**Method:** POST

**Endpoint:** `/adama/rest/userGroupCreate`

**Request:**
```json
{
  "name": "Developers"
}
```

**Response:**
```json
{
  "message": "created",
  "errorMsg": null
}
```

---

### Connection Endpoints

#### connectionGet

**Purpose:** Retrieve connections with pagination

**Method:** POST

**Endpoint:** `/adama/rest/connectionGet`

**Request:**
```json
{
  "start": "0",
  "length": "50"
}
```

**Response:**
```json
{
  "connection": [
    {
      "id": "conn-123",
      "name": "prod-rdp",
      "protocol": "1",
      "hostname": "192.168.1.100",
      "port": "3389"
    }
  ],
  "errorMsg": null
}
```

---

#### connectionCreate

**Purpose:** Create new connection

**Method:** POST

**Endpoint:** `/adama/rest/connectionCreate`

**Request (RDP):**
```json
{
  "name": "windows-prod",
  "protocol": "1",
  "hostname": "192.168.1.100",
  "port": "3389",
  "loginWith": "Username and Password",
  "colorDepth": "16"
}
```

**Request (SSH):**
```json
{
  "name": "linux-prod",
  "protocol": "2",
  "hostname": "192.168.1.50",
  "port": "22"
}
```

**Request (VNC):**
```json
{
  "name": "vnc-prod",
  "protocol": "3",
  "hostname": "192.168.1.60",
  "port": "5900"
}
```

**Response:**
```json
{
  "message": "created",
  "errorMsg": null
}
```

**Protocol Values:**
| Protocol | Value |
|----------|-------|
| RDP | 1 |
| SSH | 2 |
| VNC | 3 |

---

#### connectionPasswordGet

**Purpose:** Get connection password

**Method:** POST

**Endpoint:** `/adama/rest/connectionPasswordGet`

**Request:**
```json
{
  "connectionName": "prod-rdp"
}
```

**Response:**
```json
{
  "message": "PlainTextPassword123",
  "errorMsg": null
}
```

**Note:** Returns plain text password (not encrypted).

---

#### connectionDelete

**Purpose:** Delete connection

**Method:** POST

**Endpoint:** `/adama/rest/connectionDelete`

**Request:**
```json
{
  "connectionName": "old-conn"
}
```

**Response:**
```json
{
  "message": "deleted",
  "errorMsg": null
}
```

---

#### connectionDeleteAll

**Purpose:** Delete all connections

**Method:** POST

**Endpoint:** `/adama/rest/connectionDeleteAll`

**Request:** `{}`

**Response:**
```json
{
  "message": "all connections deleted",
  "errorMsg": null
}
```

---

### Resource Endpoints

#### resourceUnixCreate

**Purpose:** Create Unix resource

**Method:** POST

**Endpoint:** `/adama/rest/resourceUnixCreate`

**Request:**
```json
{
  "name": "unix-server-01",
  "address": "192.168.1.50",
  "type": "Unix",
  "loginUser": "admin",
  "password": "SecretPass123",
  "promptStatement": "$",
  "privilegedPromptStatment": "#"
}
```

**Response:**
```json
{
  "message": "created",
  "errorMsg": null
}
```

---

#### resourceWindowsCreate

**Purpose:** Create Windows resource

**Method:** POST

**Endpoint:** `/adama/rest/resourceWindowsCreate`

**Request:**
```json
{
  "name": "windows-server-01",
  "address": "192.168.1.100",
  "type": "aws-win-agent",
  "privilegedUser": "Administrator",
  "privilegedPassword": "SecretPass123"
}
```

**Response:**
```json
{
  "message": "created",
  "errorMsg": null
}
```

---

#### resourceOracleCreate

**Purpose:** Create Oracle database resource

**Method:** POST

**Endpoint:** `/adama/rest/resourceOracleCreate`

**Request:**
```json
{
  "name": "oracle-db-01",
  "address": "192.168.1.70",
  "type": "ORACLE",
  "serviceName": "ORCL",
  "user": "system",
  "password": "SecretPass123",
  "port": "1521"
}
```

**Response:**
```json
{
  "message": "created",
  "errorMsg": null
}
```

---

### Account Endpoints

#### accountCommonGet

**Purpose:** Retrieve accounts with pagination

**Method:** POST

**Endpoint:** `/adama/rest/accountCommonGet`

**Request:**
```json
{
  "start": "0",
  "length": "50"
}
```

**Response:**
```json
{
  "account": [
    {
      "id": "acc-123",
      "name": "root",
      "type": "Unix",
      "profileId": "56bac408"
    }
  ],
  "errorMsg": null
}
```

---

#### accountPasswordGet

**Purpose:** Get account password (encrypted)

**Method:** POST

**Endpoint:** `/adama/rest/accountPasswordGet`

**Request:**
```json
{
  "accountName": "root",
  "profileId": "56bac408"
}
```

**Response:**
```json
{
  "message": "RPRYvTY9WfA1lrndJOihl6pKFLjPFTNjvGb+AOwq/88=",
  "errorMsg": null
}
```

**Note:** Returns encrypted password. Decryption requires `api-security` key.

---

### Group Endpoints

#### userGroupGet

**Purpose:** Get user groups

**Method:** POST

**Endpoint:** `/adama/rest/userGroupGet`

**Request:** `{}`

**Response:**
```json
{
  "userGroup": [
    {
      "id": "grp-123",
      "name": "Developers"
    }
  ],
  "errorMsg": null
}
```

---

#### connectionGroupCreate

**Purpose:** Create connection group

**Method:** POST

**Endpoint:** `/adama/rest/connectionGroupCreate`

**Request:**
```json
{
  "name": "Production"
}
```

**Response:**
```json
{
  "message": "created",
  "errorMsg": null
}
```

---

### Monitoring Endpoints

#### userMonitoringCount

**Purpose:** Get monitored user count

**Method:** POST

**Endpoint:** `/adama/rest/userMonitoringCount`

**Request:** `{}`

**Response:**
```json
{
  "message": "3",
  "errorMsg": null
}
```

---

#### connectionMonitoringCount

**Purpose:** Get monitored connection count

**Method:** POST

**Endpoint:** `/adama/rest/connectionMonitoringCount`

**Request:** `{}`

**Response:**
```json
{
  "message": "5",
  "errorMsg": null
}
```

---

## Request/Response Formats

### Request Format

All POST requests must include:
- `Content-Type: application/json`
- `Authorization: Bearer <base64_token>`

**Body:** JSON object with endpoint-specific parameters

### Response Format

**Success:**
```json
{
  "data_key": "value",
  "errorMsg": null
}
```

**Error:**
```json
{
  "data_key": null,
  "errorMsg": "Error description"
}
```

**List Response:**
```json
{
  "listKey": [
    {"id": "1", "name": "item1"},
    {"id": "2", "name": "item2"}
  ],
  "errorMsg": null
}
```

**Count Response:**
```json
{
  "message": "42",
  "errorMsg": null
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | Resource created |
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Check token |
| 404 | Not Found | Check endpoint |
| 409 | Conflict | Resource already exists |
| 500 | Server Error | Retry or report bug |

### Error Response Format

```json
{
  "errorMsg": "connection not exist",
  "message": null
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "api user is not exist" | Invalid token | Check username:token |
| "connection not exist" | Resource not found | Verify connection name |
| "XSRF attack" | GWT-RPC without browser | Use REST API instead |
| HTTP 500 | Server-side NPE | Document as known issue |

---

## Pagination

### Critical Requirement

**Pagination parameters MUST be strings, not integers.**

```json
{"start": "0", "length": "10"}     ✅ Correct
{"start": 0, "length": 10}         ❌ Wrong (causes 500 error)
```

### Pagination Flow

```mermaid
graph LR
    A[Request page 1] --> B[start=0, length=10]
    B --> C[Response 10 items]
    C --> D{More data?}
    D -->|Yes| E[Request page 2]
    E --> F[start=10, length=10]
    F --> G[Response 10 items]
    D -->|No| H[Done]
```

### Pagination Example

```python
# Get all users by iterating pages
page = 0
page_size = 50
all_users = []

while True:
    response = stargate_get(
        endpoint="/userGet",
        data={"start": str(page * page_size), "length": str(page_size)}
    )
    
    users = response.get("user", [])
    all_users.extend(users)
    
    if len(users) < page_size:
        break  # Last page
    
    page += 1
```

---

## Rate Limiting

### No Official Rate Limit

The Stargate API does not document a rate limit. For production use:

- Implement exponential backoff on failures
- Use connection pooling where possible
- Consider caching frequently-accessed data

### Retry Strategy

```python
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

for attempt in range(MAX_RETRIES):
    try:
        response = api_call()
        break
    except (ConnectionError, TimeoutError):
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
        else:
            raise
```

---

## Known Server-Side Bugs

These issues are in the Stargate server code and cannot be fixed without source access:

| Endpoint | Bug | Symptom |
|-----------|-----|---------|
| alarmGet | NPE | HTTP 500 |
| nodeGet | NPE | HTTP 500 |
| nodeCount | NPE | HTTP 500 |
| serviceStatusGet | NPE | HTTP 500 |
| backupGet | NPE | HTTP 500 |
| reportsGet | NPE | HTTP 500 |
| userCreate | NPE in SshKeyPolicyService | HTTP 500 |
| accountCreate | NPE in AccountProfileSettingService | HTTP 500 |

---

## Appendix: Quick Reference

### Endpoint Summary Table

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /userGet | POST | List users |
| /userCount | POST | Count users |
| /userCreate | POST | Create user |
| /userDelete | POST | Delete user |
| /userGroupCreate | POST | Create user group |
| /userGroupGet | POST | List user groups |
| /userUserGroupGet | POST | Get user's groups |
| /connectionGet | POST | List connections |
| /connectionCount | POST | Count connections |
| /connectionCreate | POST | Create connection |
| /connectionDelete | POST | Delete connection |
| /connectionDeleteAll | POST | Delete all connections |
| /connectionPasswordGet | POST | Get connection password |
| /connectionGroupCreate | POST | Create connection group |
| /connectionGroupGet | POST | List connection groups |
| /approvedConnectionGet | POST | List approved connections |
| /approvedConnectionCount | POST | Count approved connections |
| /connectionAuthorizationGet | POST | Get connection auth |
| /accountCommonGet | POST | List accounts |
| /accountPasswordGet | POST | Get account password |
| /accountWorkflowProfileGet | POST | Get workflow profile |
| /resourceUnixCreate | POST | Create Unix resource |
| /resourceWindowsCreate | POST | Create Windows resource |
| /resourceOracleCreate | POST | Create Oracle resource |
| /userMonitoringCount | POST | Count monitored users |
| /connectionMonitoringCount | POST | Count monitored connections |

### Token Generation

```bash
# Generate Bearer token
echo -n "ansible:YOUR_TOKEN" | base64
# Output: YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM=
```

### Curl Examples

```bash
# Get user count
curl -X POST https://YOUR_SERVER_IP:8443/adama/rest/userCount \
  -H "Authorization: Bearer YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM=" \
  -H "Content-Type: application/json" \
  -d '{}'

# Get connections
curl -X POST https://YOUR_SERVER_IP:8443/adama/rest/connectionGet \
  -H "Authorization: Bearer YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM=" \
  -H "Content-Type: application/json" \
  -d '{"start": "0", "length": "50"}'
```