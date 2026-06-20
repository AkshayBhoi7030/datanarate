# DataNarrate - Security Plan

## 1. SQL Injection Protection

### Layered Defense Strategy

#### 1.1 SQL Validation & Sanitization
- **SQL Parsing**: Parse generated SQL using `sqlparse` to validate structure
- **Whitelisting**: Allow only safe SQL operations (SELECT, with restrictions)
- **Blocked Operations**: Prohibit INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE
- **Restricted Clauses**: Block UNION, subqueries in FROM, multiple statements
- **Table/Column Validation**: Verify all referenced tables/columns exist in schema

#### 1.2 Database User Permissions
- **Least Privilege Principle**: Create read-only database users for connections
- **No Write Access**: REVOKE INSERT, UPDATE, DELETE, ALTER permissions
- **Schema Restrictions**: Limit access to specific schemas/tables
- **Connection Limits**: Configure max connections per user

#### 1.3 Query Timeouts & Limits
- **Execution Timeouts**: Configure max query execution time (e.g., 30 seconds)
- **Row Limits**: Cap maximum rows returned (e.g., 10,000 rows)
- **Resource Limits**: Use database resource groups to prevent abuse

---

## 2. Query Validation Pipeline

```
Natural Language Query
       ↓
   LLM SQL Generation
       ↓
   [1] SQL Syntax Check
       ↓
   [2] Operation Type Check (SELECT only)
       ↓
   [3] Table/Column Existence Check
       ↓
   [4] Dangerous Pattern Detection
       ↓
   [5] Execution Plan Analysis (optional)
       ↓
   [6] User Approval (for complex queries, optional)
       ↓
   Query Execution
```

### Validation Checks

| Check | Description |
|-------|-------------|
| Syntax Check | Validate SQL syntax is correct |
| Operation Check | Ensure only SELECT statements |
| Schema Check | Verify all tables/columns exist |
| Pattern Check | Block comments, UNION, stacked queries |
| Function Check | Block dangerous functions (pg_sleep, etc.) |

---

## 3. Authentication Strategy

### 3.1 JWT-Based Authentication
- **Access Tokens**: Short-lived JWT tokens (15-30 minutes expiry)
- **Refresh Tokens**: Longer-lived refresh tokens (7 days)
- **Token Storage**: Secure HTTP-only cookies for refresh tokens
- **Token Signing**: RS256 asymmetric signing
- **Token Rotation**: Refresh token rotation on each use

### 3.2 Password Security
- **Hashing Algorithm**: bcrypt with work factor 12+
- **Password Complexity**: Min 8 chars, mix of letters, numbers, symbols
- **Password Rotation**: No forced rotation, but support for reset
- **Breach Detection**: Check passwords against HIBP database

### 3.3 Multi-Factor Authentication (MFA)
- **TOTP Support**: Time-based one-time passwords
- **Recovery Codes**: 10 one-time recovery codes
- **Optional**: SMS/email as secondary methods

---

## 4. Authorization Strategy

### 4.1 Role-Based Access Control (RBAC)

| Role | Permissions |
|------|-------------|
| **admin** | Full system access, user management, audit logs |
| **user** | Query execution, connection management, history, saved queries |
| **viewer** | Read-only access to shared queries and results |

### 4.2 Resource-Level Authorization
- **Connection Ownership**: Users can only access their own connections
- **Saved Query Visibility**: Private by default, optional public sharing
- **History Isolation**: Users can only view their own query history
- **Audit Log Access**: Only admins can access audit logs

### 4.3 API Authorization
- **Scope-Based Access**: JWT scopes for fine-grained control
- **Rate Limiting**: Per-user API rate limits
- **Request Validation**: Validate all input with Pydantic schemas

---

## 5. Secrets Management

### 5.1 Encryption at Rest
- **Algorithm**: AES-256-GCM for encryption
- **Key Management**: Use environment variables or KMS (AWS KMS, HashiCorp Vault)
- **Database Passwords**: Encrypted before storage, decrypted on use
- **Key Rotation**: Periodic key rotation policy

### 5.2 Environment Configuration
- **.env Files**: Never committed to version control
- **Production Secrets**: Use secure secret managers (not .env files)
- **Secret Scanning**: GitHub/GitLab secret scanning enabled

### 5.3 Sensitive Data Handling
- **Logging**: Never log passwords, API keys, PII
- **Error Messages**: Generic error messages to avoid information leakage
- **Data Redaction**: Redact sensitive data in logs/responses

---

## 6. Data in Transit Security

### 6.1 Encryption
- **TLS 1.3+**: Enforce TLS 1.3 for all connections
- **Certificate Management**: Auto-renewing certificates via Let's Encrypt
- **HSTS**: HTTP Strict Transport Security enabled
- **Secure Cookies**: HttpOnly, Secure, SameSite=Strict attributes

### 6.2 Network Security
- **WAF**: Web Application Firewall for protection
- **Private Networking**: Database in private subnet, backend in private subnet
- **VPC Peering**: Secure network communication between services

---

## 7. Audit & Monitoring

### 7.1 Audit Logging
- **All Actions**: Log user logins, queries, connection changes, exports
- **Immutable Logs**: Write-ahead logging, append-only
- **Log Retention**: 12 months retention period
- **Log Integrity**: Digital signatures on log entries

### 7.2 Security Monitoring
- **Anomaly Detection**: Unusual query patterns, access times
- **Alerting**: Real-time alerts for suspicious activity
- **Incident Response**: Documented incident response plan

---

## 8. Additional Security Measures

### 8.1 Dependency Security
- **SCA**: Software Composition Analysis (Snyk, Dependabot)
- **Regular Updates**: Keep dependencies updated
- **Vulnerability Scanning**: Automated vulnerability scanning

### 8.2 Penetration Testing
- **Annual Testing**: Annual third-party penetration testing
- **Internal Testing**: Regular internal security reviews
- **Bug Bounty**: Optional bug bounty program

### 8.3 Compliance
- **GDPR**: Data minimization, user consent, right to erasure
- **SOC 2**: Optional SOC 2 compliance
- **Data Encryption**: Encryption at rest and in transit

---

## 9. Secure Development Practices

### 9.1 Code Reviews
- **Security Reviews**: Security-focused code reviews
- **Peer Reviews**: All code changes reviewed by peers
- **Automated Checks**: Pre-commit hooks for security checks

### 9.2 Testing
- **Security Tests**: Automated security tests in CI/CD
- **Fuzz Testing**: Fuzz testing for API endpoints
- **Static Analysis**: SAST tools (SonarQube, CodeQL)
