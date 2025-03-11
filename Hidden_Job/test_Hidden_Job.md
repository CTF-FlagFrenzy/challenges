# Manual Test Cases for Hidden Job Challenge

## 1. Environment Setup Tests

### TC-001: Docker Compose Setup
**Description**: Verify that the Docker Compose setup starts the Flask service correctly.

**Steps**:
1. Navigate to the root directory of the challenge.
2. Open the challenge on the webapp.
3. Check the output to ensure the Flask service starts without errors.
4. Open a web browser and navigate to `http://localhost:8003`.
5. Verify that the main page is displayed.

## 2. Basic Functionality Tests

### TC-002: Flask Application - Main Page
**Description**: Ensure the Flask application serves the main page correctly.

**Steps**:
1. Open a web browser and navigate to `http://localhost:8003`.
2. Verify that the main page is displayed.
3. Check the browser console for any errors.

### TC-003: Flask Application - Hidden File
**Description**: Ensure the Flask application serves the hidden file correctly.

**Steps**:
1. Open a web browser and navigate to `http://localhost:8003/robots.txt`.
2. Verify that the hidden file is displayed.
3. Check the content of the hidden file to ensure it matches the expected text.

### TC-004: Flask Application - Template Rendering
**Description**: Ensure the Flask application renders the HTML template correctly.

**Steps**:
1. Open a web browser and navigate to `http://localhost:8003`.
2. Verify that the main page is displayed with the correct HTML structure.
3. Check the browser console for any errors related to template rendering.

## 3. File Generation Tests

### TC-005: TXT File Creation
**Description**: Verify that the TXT file is created correctly by the `create_txt.py` script.

**Steps**:
1. Navigate to the `flask_app` directory.
2. Run the command `python create_txt.py`.
3. Check the `flask_app/hidden` directory for the `robots.txt` file.
4. Open the `robots.txt` file and verify that it contains the expected text.

### TC-006: Flask Application - TXT File Generation
**Description**: Ensure the Flask application generates the TXT file on the main page request.

**Steps**:
1. Delete the `robots.txt` file from the `flask_app/hidden` directory if it exists.
2. Open a web browser and navigate to `http://localhost:8003`.
3. Verify that the main page is displayed.
4. Check the `flask_app/hidden` directory for the `robots.txt` file.
5. Open the `robots.txt` file and verify that it contains the expected text.

## 4. Content Validation Tests

### TC-007: TXT File Content Validation
**Description**: Verify that the TXT file contains valid conversation text.

**Steps**:
1. Open the `robots.txt` file in the `flask_app/hidden` directory.
2. Verify that the text structure is correct and contains the expected conversation lines.
3. Check that the hashed flag is correctly included in the conversation.

## 5. Flag Submission Tests

### TC-008: Submit Challenge Flag on Webapp
**Description**: Ensure the challenge flag can be submitted successfully on the webapp.

**Steps**:
1. Access the main page at `http://localhost:8003`.
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