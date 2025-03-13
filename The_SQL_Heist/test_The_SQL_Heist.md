# Manual Test Cases for The SQL Heist Challenge

## 1. Container Setup and Access Tests

### TC-001: Container Startup and Accessibility
1. **Steps**:
   - Run `docker-compose up -d` in the project root directory
   - Wait for container to fully initialize (approximately 30 seconds)
   - Open a web browser and navigate to http://localhost:80
2. **Expected Result**:
   - Docker container starts without errors
   - Web page titled "Dark News Paper" loads successfully
   - Article listings are visible

### TC-002: Container Environment Variables
1. **Steps**:
   - Run `docker exec -it the_sql_heist_web_1 env | grep TEAMKEY`
2. **Expected Result**:
   - The TEAMKEY environment variable is set with the expected value

## 2. Basic Functionality Tests

### TC-003: Article Display
1. **Steps**:
   - Access the home page
   - Verify multiple articles are displayed in the main section
   - Verify breaking news section contains 5 random articles
2. **Expected Result**:
   - Articles should be rendered with titles and content
   - Breaking news should display 5 article titles

### TC-004: Normal Search Functionality
1. **Steps**:
   - Enter a legitimate search term (e.g., "Weather")
   - Submit the search form
2. **Expected Result**:
   - Search results should display only articles containing "Weather" in title or content
   - Search results should maintain proper formatting

## 3. Security and Vulnerability Tests

### TC-005: Direct Flag Search Prevention
1. **Steps**:
   - Enter "flag" in the search box
   - Submit the search form
2. **Expected Result**:
   - Alert popup stating "Its not that easy buddy 💀" should appear
   - User should be redirected to the homepage

### TC-006: Basic SQL Injection Test
1. **Steps**:
   - Enter the following in the search box: `' OR '1'='1`
   - Submit the search form
2. **Expected Result**:
   - All articles should be displayed in the results
   - Flag should NOT be visible yet

### TC-007: Advanced SQL Injection for Flag Retrieval
1. **Steps**:
   - Enter the following in the search box: `' OR flag IS NOT NULL --`
   - Submit the search form
2. **Expected Result**:
   - The "Special Article" containing the flag should be displayed
   - Flag should appear in red box in bottom right of screen
   - Flag should follow format `FF{...}`

### TC-008: SQL UNION Injection Test
1. **Steps**:
   - Enter the following in the search box: `' UNION SELECT NULL, 'Injected Title', 'Injected Content', NULL FROM The_SQL_Heist_App_article --`
   - Submit the search form
2. **Expected Result**:
   - Results should include an article with title "Injected Title" and content "Injected Content"

## 4. Persistence Tests

### TC-009: Flag Regeneration
1. **Steps**:
   - Retrieve the flag using SQL injection
   - Restart the container with `docker-compose restart`
   - Retrieve the flag again using the same injection method
2. **Expected Result**:
   - The flag should be the same before and after restart (if TEAMKEY remains unchanged)

### TC-010: Multiple Users Access
1. **Steps**:
   - Open two different browsers or browser sessions
   - Access the application simultaneously
   - Perform searches in both sessions
2. **Expected Result**:
   - Both sessions should function independently
   - No cross-session contamination

## 5. Edge Case Tests

### TC-011: Long Search Query
1. **Steps**:
   - Enter a very long search string (500+ characters)
   - Submit the search form
2. **Expected Result**:
   - Application should handle the long input without crashing
   - Results should process normally or return an appropriate error

### TC-012: Special Character Handling
1. **Steps**:
   - Enter search terms with various special characters: `!@#$%^&*()`
   - Submit the search form
2. **Expected Result**:
   - Application should handle special characters gracefully
   - No unexpected errors or crashes

## 6. Alternative SQL Injection Techniques

### TC-013: Boolean-based Blind SQL Injection
1. **Steps**:
   - Enter: `' OR (SELECT SUBSTR(flag,1,1) FROM The_SQL_Heist_App_article WHERE flag IS NOT NULL)='F' --`
2. **Expected Result**:
   - If the first character of the flag is 'F', all articles should be displayed
   - Otherwise, no articles should be displayed

### TC-014: Time-based Blind SQL Injection
1. **Steps**:
   - Enter: `' OR (SELECT CASE WHEN (SELECT SUBSTR(flag,1,1) FROM The_SQL_Heist_App_article WHERE flag IS NOT NULL)='F' THEN RANDOMBLOB(1000000) ELSE 'a' END) --`
2. **Expected Result**:
   - If the first character is 'F', query should take longer to execute
   - Response time difference should be noticeable

### TC-015: Flag Submission
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
| TC-015  |      |        |                     |        |              |