# DataNarrate - Acceptance Criteria

## Phase 1: Project Setup & Foundation

### General Criteria
- [ ] Project repository initialized with proper folder structure
- [ ] README.md with clear setup instructions
- [ ] .gitignore configured for Python, Node.js, Docker
- [ ] All planning documents created in docs/ folder

### Backend
- [ ] FastAPI application skeleton created
- [ ] Basic health endpoint (/health) working and returning 200 OK
- [ ] Database connection configured (PostgreSQL)
- [ ] Alembic migrations setup

### Frontend
- [ ] React + Vite application created
- [ ] Basic routing working
- [ ] Home page displayed successfully

### Docker & Dev Environment
- [ ] Dockerfile for backend and frontend created
- [ ] docker-compose.yml working for local development
- [ ] Services (backend, frontend, PostgreSQL, Redis) start successfully
- [ ] Sample e-commerce database created and seeded with test data

### CI/CD
- [ ] GitHub Actions workflow configured for linting and testing
- [ ] Pipeline runs on pull requests

---

## Phase 2: User Authentication & Management

### Registration
- [ ] User can register with email, password, first name, last name
- [ ] Password must meet complexity requirements (min 8 chars, etc.)
- [ ] Email must be unique across users
- [ ] Password is hashed with bcrypt before storage
- [ ] User receives confirmation message on successful registration

### Login
- [ ] User can login with email and password
- [ ] JWT access token returned on successful login
- [ ] Invalid credentials return appropriate error
- [ ] Login attempts are rate-limited
- [ ] User is redirected to dashboard on successful login

### User Profile
- [ ] Authenticated user can view their profile
- [ ] User can update their first name, last name
- [ ] User can change their password
- [ ] Profile changes are saved to database

### RBAC
- [ ] Roles (admin, user, viewer) are enforced
- [ ] Unauthorized access is blocked with 403 Forbidden
- [ ] Admin users have access to all features

### Audit Logging
- [ ] Login/logout events are logged
- [ ] User registration events are logged
- [ ] Profile change events are logged
- [ ] Audit logs include timestamp, user, action, IP address

### Testing
- [ ] Unit tests for auth service pass
- [ ] Integration tests for auth endpoints pass

---

## Phase 3: Database Connection Management

### Connection Creation
- [ ] User can create a new database connection
- [ ] Form includes: connection name, db type, host, port, database, username, password
- [ ] Supported db types: PostgreSQL, MySQL, SQL Server
- [ ] Password is encrypted before storage using AES-256-GCM
- [ ] Connection is associated with the user

### Connection Testing
- [ ] User can test a connection before saving
- [ ] Test returns success/failure status
- [ ] Error message displayed if connection fails

### Connection Management
- [ ] User can view list of their connections
- [ ] User can edit existing connections
- [ ] User can delete connections
- [ ] Connection list shows connection name, type, last connected time

### Schema Retrieval
- [ ] System can retrieve schema (tables, columns, types) from connected database
- [ ] Schema is cached in Redis with TTL
- [ ] Subsequent requests use cached schema
- [ ] Schema display shows tables, columns, data types

### Security
- [ ] User can only access their own connections
- [ ] Database credentials are never exposed in API responses
- [ ] Connections are validated before use

### Testing
- [ ] Unit tests for connection service pass
- [ ] Integration tests for connection endpoints pass

---

## Phase 4: Natural Language to SQL

### SQL Generation
- [ ] User can enter natural language query
- [ ] System generates valid SQL from natural language
- [ ] SQL generation uses database schema context
- [ ] SQL generation completes within 5 seconds (P95)
- [ ] Generated SQL is displayed to user before execution

### SQL Validation
- [ ] Only SELECT statements are allowed
- [ ] INSERT/UPDATE/DELETE/DROP/ALTER are blocked
- [ ] SQL syntax is validated
- [ ] All referenced tables/columns are verified to exist
- [ ] Dangerous patterns (comments, UNION, stacked queries) are blocked
- [ ] Validation fails fast with clear error message

### Query Execution
- [ ] Validated SQL is executed against the database
- [ ] Query results are returned to user
- [ ] Query times out after configurable duration (e.g., 30s)
- [ ] Row count is limited (e.g., 10,000 rows)
- [ ] Query execution errors are displayed clearly
- [ ] Execution time and row count are shown

### Database Security
- [ ] Queries executed with read-only database user
- [ ] No write operations allowed
- [ ] Query history is saved

### Accuracy
- [ ] SQL generation accuracy > 85% on test queries
- [ ] Common business queries work correctly

### Testing
- [ ] Unit tests for SQL generator pass
- [ ] Unit tests for SQL validator pass
- [ ] Integration tests for query endpoint pass
- [ ] Manual testing with 50+ different queries

---

## Phase 5: Query Results, Visualizations & Insights

### Results Display
- [ ] Query results displayed in table format
- [ ] Table supports pagination for large result sets
- [ ] Columns have appropriate headers
- [ ] Numeric values are formatted correctly

### Visualizations
- [ ] System automatically recommends appropriate chart type
- [ ] Bar charts supported
- [ ] Line charts supported
- [ ] Pie charts supported
- [ ] Scatter charts supported
- [ ] Charts are interactive (hover tooltips)
- [ ] User can switch between chart types
- [ ] Charts render within 2 seconds

### Insights
- [ ] AI-generated business insights displayed with results
- [ ] Insights are relevant to the query
- [ ] Insights highlight key findings (trends, anomalies, top/bottom performers)
- [ ] 2-5 insights generated per query

### Query History
- [ ] User can view their query history
- [ ] History shows natural language query, timestamp, status, execution time
- [ ] History is paginated
- [ ] History can be filtered by date, status, connection
- [ ] User can re-run a previous query from history

### Query UI
- [ ] Query page has clean, intuitive interface
- [ ] SQL is displayed with syntax highlighting
- [ ] Loading states shown during generation/execution
- [ ] Error messages are user-friendly

### Testing
- [ ] Visualizations render correctly with different data types
- [ ] Insights are relevant and helpful
- [ ] History loads and filters correctly

---

## Phase 6: Saved Queries & Exports

### Save Queries
- [ ] User can save a query with name and description
- [ ] Saved queries include natural language query and generated SQL
- [ ] User can add tags to saved queries
- [ ] Saved queries are private by default
- [ ] User can mark queries as public (optional)

### Saved Queries Management
- [ ] User can view list of saved queries
- [ ] List shows query name, description, tags, last used
- [ ] User can search saved queries by name/description
- [ ] User can filter saved queries by tags
- [ ] User can edit saved queries
- [ ] User can delete saved queries
- [ ] User can run a saved query with one click

### Exports
- [ ] User can export query results to CSV
- [ ] User can export query results to Excel (.xlsx)
- [ ] User can export query results to JSON
- [ ] User can export visualizations as PNG
- [ ] User can export visualizations as PDF
- [ ] Exported files are downloaded automatically

### Testing
- [ ] Saved queries persist correctly in database
- [ ] Exports generate correct files with all data
- [ ] Exported files can be opened in external applications

---

## Phase 7: Polish, Testing & Deployment

### Testing
- [ ] Unit test coverage > 80% for backend
- [ ] Unit test coverage > 70% for frontend
- [ ] All integration tests pass
- [ ] E2E tests cover main user flows
- [ ] No critical or high-severity bugs
- [ ] Performance testing: API response < 500ms (P95), except query execution
- [ ] Load testing: system handles 50 concurrent users

### Security
- [ ] Security audit completed
- [ ] No critical vulnerabilities found
- [ ] All dependencies up to date
- [ ] Penetration testing passed (if applicable)
- [ ] Secrets properly managed (no hardcoded secrets)

### Performance
- [ ] Database queries optimized
- [ ] Caching working correctly
- [ ] Frontend bundle size optimized
- [ ] Page load time < 2 seconds

### Deployment
- [ ] Production environment deployed
- [ ] Monitoring (Prometheus + Grafana) set up
- [ ] Logging (ELK or similar) set up
- [ ] Alerting configured for critical errors
- [ ] SSL/TLS certificates configured and valid
- [ ] Backup and recovery procedures documented and tested

### Documentation
- [ ] API documentation complete and up to date
- [ ] User guide created
- [ ] Deployment documentation created
- [ ] Troubleshooting guide created

### User Acceptance
- [ ] Beta testing completed with real users
- [ ] User feedback incorporated
- [ ] User satisfaction score > 4.0/5.0

---

## Overall Project Acceptance

- [ ] All phases completed and accepted
- [ ] All acceptance criteria met
- [ ] No critical bugs in production
- [ ] System is stable and performant
- [ ] Documentation is complete
- [ ] Project is ready for launch
