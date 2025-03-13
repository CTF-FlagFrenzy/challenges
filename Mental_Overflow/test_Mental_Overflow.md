# Manual Test Cases for Mental Overflow Application

## 1. Deployment and Setup Tests

### TC-001: Pod Deployment and Startup
**Objective**: Verify that the Kubernetes pod deploys and starts correctly.

**Steps**:
1. Open challenge on webapp

**Expected Result**: Pod starts successfully with appropriate log messages.

## 2. File and Service Tests

### TC-002: File Generation
**Objective**: Verify that the Brainfuck file is generated correctly.

**Steps**:
1. Access the endpoint using curl or a browser:
   `http://localhost:8080/brainfuck.bf`

**Expected Result**: The file should exist and contain Brainfuck code.

### TC-003: Service Accessibility
**Objective**: Verify that the Kubernetes service correctly exposes the Brainfuck file.

**Steps**:
1. Access the endpoint using curl or a browser:
   `http://localhost:8080/brainfuck.bf`

**Expected Result**: The Brainfuck content should be returned without errors.

## 3. Environment and Flag Tests

### TC-004: Environment Variable Handling
**Objective**: Verify that the application correctly uses the TEAMKEY environment variable.

**Steps**:
1. Create or update a ConfigMap or Secret with the team key:
   ```bash
   kubectl create configmap mental-overflow-config --from-literal=TEAMKEY=testkey123 -n <namespace>
   # Or update existing:
   kubectl patch configmap mental-overflow-config -p '{"data":{"TEAMKEY":"testkey123"}}' -n <namespace>
   ```
2. Update the deployment to use the ConfigMap/Secret (if not already configured)
3. Restart the pod:
   ```bash
   kubectl rollout restart deployment <deployment-name> -n <namespace>
   ```
4. Check the logs for the generated flag

**Expected Result**: The generated flag should be based on the combination of "#8W@3fp5#Y" + "testkey123".

### TC-005: Flag Submission
**Objective**: Verify that the extracted flag can be successfully submitted.

**Steps**:
1. Extract the flag through the appropriate method
2. Submit to the scoring system

**Expected Result**: The flag is accepted by the scoring system and points are awarded for the challenge.

## 4. Web Application Tests

### TC-006: Web Application Access
**Objective**: Verify that the Mental Overflow web application is accessible.

**Steps**:
1. Open a web browser
2. Navigate to the web application URL
3. Verify the application loads correctly

**Expected Result**: The web application loads without errors.

### TC-007: Brainfuck File Access
**Objective**: Verify that the Brainfuck file is accessible through the web application.

**Steps**:
1. Navigate to the web application URL
2. Access the Brainfuck file endpoint:
   ```
   https://<webapp-url>/brainfuck.bf
   ```
3. Verify that the file downloads or displays correctly

**Expected Result**: The Brainfuck file content should be returned without errors.

## 5. Brainfuck Execution and Flag Extraction Tests

### TC-008: Brainfuck File Content Verification
**Objective**: Verify that the downloaded Brainfuck file contains valid code.

**Steps**:
1. Download the Brainfuck file from the web application
2. Examine the content of the file:
   ```bash
   cat brainfuck.bf
   ```
3. Verify that it contains valid Brainfuck syntax (characters like +, -, >, <, [, ], ., ,)

**Expected Result**: The file should contain valid Brainfuck code.

### TC-009: Brainfuck Execution
**Objective**: Verify that the Brainfuck code can be executed and produces the expected output.

**Steps**:
1. Download the Brainfuck file from the web application
2. Use a Brainfuck interpreter (online or local) to execute the code
   ```bash
   # Example with a local interpreter
   bf downloaded-brainfuck.bf
   ```
   - Online interpreters can be found at sites like https://copy.sh/brainfuck/

**Expected Result**: The interpreter should output the hashed flag in the format `FF{...}` but with the curly braces replaced by random characters.

### TC-010: Flag Extraction
**Objective**: Verify that the obfuscated flag can be properly extracted and formatted.

**Steps**:
1. Execute the Brainfuck code to get the output
2. Identify the flag pattern in the output (characters between the replaced curly braces)
3. Replace the special characters with actual curly braces to form `FF{...}`
4. Verify that the flag follows the expected pattern

**Expected Result**: A properly formatted flag in the form `FF{...}` is extracted.

### TC-011: Flag Submission
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