# Manual Test Cases for Solana Assets Application

## Authentication Tests

### TC-001: User Login with Valid Credentials (Andreas)
**Objective**: Verify a user can successfully log in with valid credentials
**Precondition**: User is not logged in
**Steps**:
1. Navigate to the index page (http://localhost:80/)
2. Enter username: "Andreas"
3. Enter password: "GoodPassw0rd123"
4. Click "Sign In" button
**Expected Result**: 
- User is redirected to dashboard page
- Dashboard displays wallet information and charts
- Flag cookie is set in the browser
**Actual Result**: 
**Status**: 
**Notes**:

### TC-002: User Login with Valid Credentials (Leon)
**Objective**: Verify a user can successfully log in with secondary valid credentials
**Precondition**: User is not logged in
**Steps**:
1. Navigate to the index page (http://localhost:80/)
2. Enter username: "Leon"
3. Enter password: "Admin123"
4. Click "Sign In" button
**Expected Result**: 
- User is redirected to wrong.html page
- Page displays troll message
- A cookie named "Flag" with value "FF{try /files}" is set
**Actual Result**: 
**Status**: 
**Notes**:

### TC-003: User Login with Invalid Credentials
**Objective**: Verify system handles invalid login attempts properly
**Precondition**: User is not logged in
**Steps**:
1. Navigate to the index page (http://localhost:80/)
2. Enter invalid username and password combination
3. Click "Sign In" button
**Expected Result**: 
- Error message "Invalid username or password" is displayed
- User remains on the login page
**Actual Result**: 
**Status**: 
**Notes**:

## Navigation Tests

### TC-004: Access Dashboard Directly
**Objective**: Verify dashboard page accessibility
**Precondition**: None
**Steps**:
1. Navigate directly to the dashboard URL (http://localhost:80/dashboard/)
**Expected Result**: 
- Dashboard page loads successfully
- Solana and Polkadot charts are displayed
- Transaction lists are visible
- Flag cookie is set with the hashed flag value
**Actual Result**: 
**Status**: 
**Notes**:

### TC-005: News Page Access
**Objective**: Verify news page loads correctly
**Precondition**: None
**Steps**:
1. Navigate to the news page (http://localhost:80/news/)
**Expected Result**: 
- News page loads with three news articles
- Each article has a "Read more" link that shows additional content when clicked
**Actual Result**: 
**Status**: 
**Notes**:

### TC-006: Access Files Page
**Objective**: Verify files page accessibility and content display
**Precondition**: None
**Steps**:
1. Navigate to files page (http://localhost:80/files/)
**Expected Result**: 
- Files page loads and displays wallet credentials (Username: Andreas, Password: GoodPassw0rd123)
- Solana logo is displayed
**Actual Result**: 
**Status**: 
**Notes**:

### TC-007: Access Wrong Page
**Objective**: Verify the wrong page redirection
**Precondition**: None
**Steps**:
1. Navigate to right URL (http://localhost:80/right/)
**Expected Result**: 
- Wrong page loads with troll message
- Flag cookie is set with value "FF{try /files}"
**Actual Result**: 
**Status**: 
**Notes**:

## Cookie Management Tests

### TC-008: Flag Cookie Generation
**Objective**: Verify flag cookie is correctly generated and set
**Precondition**: None
**Steps**:
1. Navigate to dashboard (http://localhost:80/dashboard/)
2. Use browser developer tools to inspect cookies
**Expected Result**: 
- Flag cookie is present
- Cookie format follows the pattern "FF{[hashed_value]}"
- Cookie has appropriate expiration (7 days)
**Actual Result**: 
**Status**: 
**Notes**:

### TC-009: Index Page Cookie Management
**Objective**: Verify index page sets expected cookies
**Precondition**: None
**Steps**:
1. Navigate to index page (http://localhost:80/)
2. Use browser developer tools to inspect cookies
**Expected Result**: 
- Previous cookies are deleted
- A cookie named "Gemma-Lehre" with value "Its not that easy buddy" is set
**Actual Result**: 
**Status**: 
**Notes**:

## User Interface Tests

### TC-010: Dashboard UI Elements
**Objective**: Verify all UI elements on dashboard are correctly displayed
**Precondition**: User has navigated to dashboard
**Steps**:
1. Check Solana chart element
2. Check Polkadot chart element
3. Verify transaction lists
4. Check wallet worth displays
**Expected Result**: 
- All charts display properly
- Transaction lists show correct transactions
- Wallet worth displays correct amounts (15.3 SOL and 10.7 DOT)
- Navigation bar shows correct links
**Actual Result**: 
**Status**: 
**Notes**:

### TC-011: News UI Elements and Functionality
**Objective**: Verify news page UI elements and read more/less functionality
**Precondition**: User has navigated to news page
**Steps**:
1. Click "Read more" on first news item
2. Verify additional content is displayed
3. Click "Read less" on first news item
4. Verify content is hidden again
5. Repeat for other news items
**Expected Result**: 
- News items expand and collapse correctly
- Text changes between "Read more" and "Read less"
- All news items function independently
**Actual Result**: 
**Status**: 
**Notes**:

## Container Deployment Tests

### TC-012: Docker Container Deployment
**Objective**: Verify application deploys correctly in Docker container
**Precondition**: Docker and docker-compose installed
**Steps**:
1. Navigate to project root directory
2. Run `docker-compose up`
3. Check if container starts successfully
**Expected Result**: 
- Container builds without errors
- Web server starts and is accessible at http://localhost:80/
- TEAMKEY environment variable is properly set
**Actual Result**: 
**Status**: 
**Notes**:

### TC-013: Environmental Variable Access
**Objective**: Verify application correctly uses environmental variables
**Precondition**: Docker container running with TEAMKEY set
**Steps**:
1. Log in with valid credentials (Andreas/GoodPassw0rd123)
2. Navigate to dashboard
3. Check server logs for hashed flag value
**Expected Result**: 
- Log entry shows "Hashed Flag: [hash value]"
- Hash value matches the one in the Flag cookie
**Actual Result**: 
**Status**: 
**Notes**:

### TC-014: Flag Submission
**Objective**: Verify that the extracted flag can be successfully submitted to the scoring system.

**Steps**:
1. Navigate to the CTF scoring platform
2. Submit the extracted flag (with proper curly braces) in the submission form
3. Verify the submission is accepted

**Expected Result**: The flag is accepted by the scoring system and points are awarded for the challenge.

## Test Execution Log

| Test ID | Date | Tester | Browser/Environment | Result | Issues Found |
|---------|------|--------|---------------------|--------|--------------|
| TC-001  |      |        |                     |        |              |
| TC-002  |      |        |                     |        |              |
| TC-003  |      |        |                     |        |              |
| TC-004  |      |        |                     |        |              |
| TC-005  |      |        |                     |        |              |
| TC-006  |      |        |                     |        |              |
| TC-007  |      |        |                     |        |              |
| TC-008  |      |        |                     |        |              |
| TC-009  |      |        |                     |        |              |
| TC-010  |      |        |                     |        |              |
| TC-011  |      |        |                     |        |              |
| TC-012  |      |        |                     |        |              |
| TC-013  |      |        |                     |        |              |
| TC-014  |      |        |                     |        |              |