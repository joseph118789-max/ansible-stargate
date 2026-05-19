# Troubleshooting Guide

## Common Issues and Solutions

### 1. Authentication Errors

#### Error: "api user is not exist"

**Cause:** The API user doesn't exist in the Stargate database or the token is incorrect.

**Solution:**
1. Verify the API user exists in the Stargate database:
   ```sql
   SELECT * FROM USER WHERE USERNAME = 'ansible';
   ```
2. Check the token is correct (should be `YOUR_TOKEN`)
3. Ensure the token format is correct: `ansible:YOUR_TOKEN`

#### Error: "XSRF attack"

**Cause:** GWT-RPC endpoint requires browser session with permutation headers.

**Solution:** Use REST API (`/adama/rest/*`) instead of GWT-RPC (`/adama/adama/auth`).

#### Error: "Bearer token invalid"

**Cause:** Base64 encoding is incorrect.

**Solution:**
```bash
# Correct token generation
echo -n "ansible:YOUR_TOKEN" | base64
# Output: YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM=
```

---

### 2. Connection Issues

#### Error: "Connection timeout"

**Solution:**
1. Check server is reachable:
   ```bash
   curl -k -I https://YOUR_SERVER_IP:8443/adama/
   ```
2. Verify firewall rules
3. Increase timeout in playbook:
   ```yaml
   - name: Get users
     company.stargate.stargate_get:
       server: "{{ stargate_server }}"
       token: "{{ stargate_token }}"
       endpoint: "/userGet"
       timeout: 60
   ```

#### Error: "SSL certificate verify failed"

**Solution:**
```yaml
- name: Get users
  company.stargate.stargate_get:
    server: "{{ stargate_server }}"
    token: "{{ stargate_token }}"
    endpoint: "/userGet"
    validate_certs: false  # Set to false for self-signed certs
```

---

### 3. API Errors

#### HTTP 500 Errors

**Cause:** Server-side Java NPE bugs.

**Affected Endpoints:**
- `/adama/rest/alarmGet`
- `/adama/rest/nodeGet`
- `/adama/rest/nodeCount`
- `/adama/rest/serviceStatusGet`
- `/adama/rest/backupGet`
- `/adama/rest/reportsGet`

**Solution:** These are documented server-side bugs. Workarounds:
1. Use alternative endpoints where available
2. Report to MasterSAM support
3. Implement error handling in playbooks

#### HTTP 404 Errors

**Cause:** Endpoint not implemented in server version.

**Solution:** Check API documentation for available endpoints.

#### Error: "connection not exist"

**Cause:** Trying to operate on non-existent connection.

**Solution:**
1. List all connections first:
   ```yaml
   - name: Get connections
     company.stargate.stargate_get:
       server: "{{ stargate_server }}"
       token: "{{ stargate_token }}"
       endpoint: "/connectionGet"
       data:
         start: "0"
         length: "50"
   ```
2. Verify connection name exists

---

### 4. Pagination Issues

#### Error: "Empty response" or "HTTP 500"

**Cause:** Pagination parameters are integers instead of strings.

**Solution:**
```yaml
# ❌ Wrong - causes HTTP 500
data:
  start: 0
  length: 10

# ✅ Correct - strings
data:
  start: "0"
  length: "10"
```

---

### 5. Module Execution Issues

#### Module Not Found

**Solution:**
1. Install the collection:
   ```bash
   ansible-galaxy collection install company.stargate
   ```
2. Or build from source:
   ```bash
   cd collections/ansible_collections/company/stargate
   ansible-galaxy collection build
   ansible-galaxy collection install company-stargate-*.tar.gz --force
   ```

#### Missing Required Parameters

**Solution:** Check module documentation for required parameters:
```yaml
# Required: server, token, endpoint
- name: Get users
  company.stargate.stargate_get:
    server: "https://YOUR_SERVER_IP:8443"  # Required
    token: "ansible:YOUR_TOKEN"  # Required
    endpoint: "/userGet"  # Required
    data:  # Optional
      start: "0"
      length: "10"
```

---

### 6. Role Execution Issues

#### Role Not Found

**Solution:**
1. Ensure collection is installed:
   ```bash
   ansible-galaxy collection list | grep stargate
   ```
2. Use full role path:
   ```yaml
   - name: Run login role
     hosts: localhost
     roles:
       - company.stargate.login
   ```

---

### 7. Test Failures

#### pytest: Module Not Found

**Solution:**
```bash
# Install test dependencies
pip install pytest pytest-ansible pyyaml requests mock

# Run tests
cd /root/.openclaw/workspace/projects/ansible-stargate
python3 -m pytest tests/unit/ -v
```

#### molecule: Docker Not Available

**Solution:**
```bash
# Install Docker
sudo apt-get install docker.io

# Add user to docker group
sudo usermod -aG docker $USER

# Restart session
newgrp docker
```

---

### 8. Playbook Performance Issues

#### Slow Execution

**Solution:**
1. Use pagination to limit results:
   ```yaml
   - name: Get users
     company.stargate.stargate_get:
       server: "{{ stargate_server }}"
       token: "{{ stargate_token }}"
       endpoint: "/userGet"
       data:
         start: "0"
         length: "50"  # Limit page size
   ```
2. Add retries with delay:
   ```yaml
   - name: Get users
     company.stargate.stargate_get:
       server: "{{ stargate_server }}"
       token: "{{ stargate_token }}"
       endpoint: "/userGet"
       retries: 3
       retry_delay: 5
   ```

---

## Debug Mode

### Enable Verbose Output

```bash
# Run playbook with verbose output
ansible-playbook playbooks/user-management.yml -v

# More verbose
ansible-playbook playbooks/user-management.yml -vv

# Extreme verbose
ansible-playbook playbooks/user-management.yml -vvv
```

### Enable Module Debug

```yaml
- name: Get users
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Retrieve users
      company.stargate.stargate_get:
        server: "https://YOUR_SERVER_IP:8443"
        token: "ansible:YOUR_TOKEN"
        endpoint: "/userGet"
        data:
          start: "0"
          length: "10"
      register: result
    
    - name: Debug output
      debug:
        var: result
```

### Check API Server Status

```bash
# Check server is up
curl -k -I https://YOUR_SERVER_IP:8443/adama/

# Test API endpoint directly
curl -k -X POST https://YOUR_SERVER_IP:8443/adama/rest/userCount \
  -H "Authorization: Bearer YW5zaWJsZTpmOGFiMmM4My0wYmNiLTRkMTUtYjVkYS1hZmJjMTljYmI0MWM=" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## Getting Help

1. **Check API Documentation:** [`docs/API_ENDPOINTS.md`](collections/ansible_collections/company/stargate/docs/API_ENDPOINTS.md)
2. **Review Collection README:** [`README.md`](collections/ansible_collections/company/stargate/README.md)
3. **Open an Issue:** https://github.com/joseph118789-max/ansible-stargate/issues
4. **Check Existing Issues:** https://github.com/joseph118789-max/ansible-stargate/issues?q=is%3Aissue