# Manual Test Cases for Shadow File Challenge

## 1. Environment Setup Tests

### TC-001: Docker Environment Setup
1. **Steps**:
   - Check that TEAMKEY is set in docker-compose.yml
2. **Expected Results**:
   - Application launches with proper environment variables

## 2. Basic Functionality Tests

### TC-002: Homepage Access
1. **Steps**:
   - Navigate to http://localhost:80/
2. **Expected Results**:
   - Financial Dashboard page displays with charts and proper styling

### TC-003: Hidden File Generation
1. **Steps**:
   - Access the homepage to trigger create_json.py
   - Check logs for successful file creation
2. **Expected Results**:
   - Log message "JSON file successfully created" appears

## 3. Security and Vulnerability Tests

### TC-004: Hidden Endpoint Discovery
1. **Steps**:
   - Use directory fuzzing tool (like ffuf) against the application
   - Run: `ffuf -w common.txt -u http://localhost:80/FUZZ`
2. **Expected Results**:
   - Tool discovers "/security.txt" endpoint

### TC-005: Security.txt File Access
1. **Steps**:
   - Navigate to http://localhost:80/security.txt
2. **Expected Results**:
   - JSON content with product information is displayed

### TC-006: Path Traversal Test
1. **Steps**:
   - Try accessing: http://localhost:80/../hidden/security.txt
   - Try accessing: http://localhost:80/hidden/security.txt
2. **Expected Results**:
   - Access denied or 404 error (application properly protects hidden directory)

## 4. Flag Recovery Tests

### TC-007: Flag Encoding Verification
1. **Steps**:
   - Access security.txt
   - Extract product IDs 
   - Decode first ID from hex using a tool like CyberChef
2. **Expected Results**:
   - Decoded content appears to be part of a flag

### TC-008: Flag Assembly Process
1. **Steps**:
   - Access security.txt
   - Extract all product IDs
   - Decode each ID from hex
   - Sort decoded parts according to the "units" field value of each product
   - Concatenate parts in the correct order
2. **Expected Results**:
   - Assembled flag matches format FF{...} with SHA256 hash

### TC-009: End-to-End Challenge Solution
1. **Steps**:
   - Launch the application
   - Discover the security.txt endpoint
   - Access the security.txt file
   - Extract and decode all product IDs
   - Arrange parts according to units field values
   - Assemble the complete flag
2. **Expected Results**:
   - Valid flag obtained in format FF{...}

## 5. Error Handling Tests

### TC-010: Missing Environment Variables
1. **Steps**:
   - Modify docker-compose.yml to remove TEAMKEY
   - Restart container
   - Access the homepage
2. **Expected Results**:
   - Application logs error about missing environment variables but continues to function

### TC-011: Invalid Access Attempts
1. **Steps**:
   - Access non-existent endpoints: http://localhost:80/admin
   - Access invalid file paths: http://localhost:80/file.txt
2. **Expected Results**:
   - Proper 404 error responses without revealing sensitive information

### TC-012: Flag Submission
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