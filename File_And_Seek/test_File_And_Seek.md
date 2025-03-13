# Manual Test Cases for File And Seek Challenge

## 1. Environment Setup Tests

### TC-001: Verify Docker Setup
**Objective**: Ensure the Docker environment is set up correctly.

**Steps**:
1. Start challenge on the webapp

**Expected Result**: The Flask service should start and be accessible on `http://localhost:80`.

## 2. Basic Functionality Tests

### TC-002: Verify Main Page Accessibility
**Objective**: Ensure the main page of the Flask application is accessible.

**Steps**:
1. Open a web browser.
2. Navigate to `http://localhost:80`.

**Expected Result**: The main page should load without errors.

### TC-003: Verify Hidden File Accessibility
**Objective**: Ensure the hidden file `security.txt` is accessible.

**Steps**:
1. Open a web browser.
2. Navigate to `http://localhost:80/security.txt`.

**Expected Result**: The `security.txt` file should be downloaded or displayed in the browser.

## 3. File Generation and Content Tests

### TC-004: Verify JSON File Creation
**Objective**: Ensure the JSON file with product information is created correctly.

**Steps**:
1. Check the `flask_app/hidden` directory.
2. Verify the presence of the `security.txt` file.
3. Open the `security.txt` file and verify its contents.

**Expected Result**: The `security.txt` file should contain a JSON object with product information and hashed flag parts.

### TC-005: Verify Product ID Assignment
**Objective**: Ensure each product in the JSON file has a unique ID part of the hashed flag.

**Steps**:
1. Open the `security.txt` file in the `flask_app/hidden` directory.
2. Verify that each product has an `id` field with a part of the hashed flag.

**Expected Result**: Each product should have a unique `id` field corresponding to a part of the hashed flag.

## 4. Application Management Tests

### TC-006: Verify Flask Application Logging
**Objective**: Ensure the Flask application logs important events.

**Steps**:
1. Check the application logs.

**Expected Result**: The logs should contain information about the creation of the JSON file, assignment of IDs to products, and any errors encountered.

## 5. End-to-End Flow Tests

### TC-007: Verify Full Challenge Flow
**Objective**: Ensure the full challenge flow works as expected.

**Steps**:
1. Access the main page at `http://localhost:80`.
2. Access the hidden file at `http://localhost:80/security.txt`.
3. Verify the contents of the `security.txt` file.

**Expected Result**: The main page should load, the hidden file should be accessible, and the `security.txt` file should contain the correct product information and hashed flag parts.

### TC-008: Submit Challenge Flag on Webapp
**Objective**: Ensure the challenge flag can be submitted successfully on the webapp.

**Steps**:
1. Access the main page at `http://localhost:80`.
2. Locate the flag submission form on the webapp.
3. Enter the challenge flag into the submission form.
4. Submit the flag.

**Expected Result**: The flag should be submitted successfully, and a confirmation message should be displayed on the webapp.

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