# Stargate REST API v11.7.0 - Endpoint Mapping

**Server:** https://10.201.208.160:8443
**Base Path:** /adama/rest/{endpoint}
**Auth:** base64(username:token) as Bearer token

## Verified Working Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `userGet` | POST | Get users | ✅ Working |
| `userCount` | POST | Count users | ✅ Working |
| `connectionGet` | POST | Get connections | ✅ Working |
| `connectionCount` | POST | Count connections | ✅ Working |
| `connectionCreate` | POST | Create connection | ✅ Working |
| `connectionDelete` | POST | Delete connection | ✅ Working |
| `accountPasswordGet` | POST | Get account password | ✅ Working |
| `accountPasswordPlainCreate` | POST | Create plain password | ✅ Working |
| `accountInsecurePasswordGet` | POST | Get insecure password | ✅ Working |
| `accountCommonGet` | POST | Get account common data | ✅ Working |
| `accountCreate` | POST | Create account | ✅ Working |
| `resourceOracleCreate` | POST | Create Oracle resource | ✅ Working |
| `resourceUnixCreate` | POST | Create Unix resource | ✅ Working |
| `resourceWindowsCreate` | POST | Create Windows resource | ✅ Working |

## Request/Response Format

All endpoints use POST with JSON body:
```json
{
  "start": "0",
  "length": "10"
}
```

Response format:
```json
{
  "<resource>": [...],
  "errorMsg": null
}
```

## Authentication

```python
import base64

# Format: username:api_token
token = "ansible:d147ef1f-896d-487c-833e-28154903afc5"
auth_b64 = base64.b64encode(token.encode()).decode()

headers = {
    "Authorization": f"Bearer {auth_b64}",
    "Content-Type": "application/json"
}
```

## Example: Get Connections

```bash
curl -sk -X POST https://10.201.208.160:8443/adama/rest/connectionGet \
  -H "Authorization: Bearer YW5zaWJsZTpkMTQ3ZWYxZi04OTZkLTQ4N2MtODMzZS0yODE1NDkwM2FmYzU=" \
  -H "Content-Type: application/json" \
  -d '{"start":"0","length":"5"}'
```
