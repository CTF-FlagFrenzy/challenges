# Manual Test Cases for The Neverending Zip

## Overview
This document contains manual test cases to verify the proper functioning of The Neverending Zip application, which creates and processes deeply nested ZIP files.

## 1. Deployment Tests

### TC-001: Container Deployment
**Description**: Test deploying the application in a Docker container.

**Prerequisites**:
- Docker and Docker Compose installed

**Steps**:
1. Navigate to the project root directory
2. Verify container logs for successful startup

**Expected Results**:
- Container should build and start without errors
- Logs should indicate successful Flask application startup
- No Python exceptions or errors should be visible in logs

## 2. Web Interface Tests

### TC-002: Container Web Interface Access
**Description**: Test accessing the web interface through the container.

**Prerequisites**:
- Container running from TC-001

**Steps**:
1. Open a web browser and navigate to `http://localhost:80`
2. Wait for the web interface to load

**Expected Results**:
- The web interface should be accessible
- The challenge page with "Funny Challenge" title should display
- Progress bar should appear and update in real-time

## 3. Functionality Tests

### TC-003: ZIP Generation in Container
**Description**: Test the ZIP generation process in the container environment.

**Prerequisites**:
- Container running with Docker Compose

**Steps**:
1. Access the web interface at `http://localhost:80`
2. Monitor the progress bar for ZIP creation
3. Check container logs for creation progress

**Expected Results**:
- Progress updates should appear in logs showing layers/second
- Web interface progress bar should update accordingly
- HaveFun.zip should be created inside the container

### TC-004: Container Resource Usage During ZIP Creation
**Description**: Monitor container resource usage during ZIP creation.

**Prerequisites**:
- Container running with Docker Compose
- Tools for monitoring container resources (docker stats)

**Steps**:
1. Start ZIP creation process via web interface
2. Run `docker stats` in a terminal to monitor container resource usage
3. Observe memory, CPU and I/O usage during the process

**Expected Results**:
- Container should use resources within reasonable limits
- Process should not crash due to lack of resources
- Memory usage should remain stable without continuous growth

### TC-005: Custom Team Key in Container Environment
**Description**: Test flag generation with a custom team key in container.

**Prerequisites**:
- Docker and Docker Compose installed

**Steps**:
1. Edit docker-compose.yml to set a custom TEAMKEY value
2. Deploy container with `docker-compose up --build`
3. Access web interface and download the generated ZIP
4. Extract the ZIP and find the flag

**Expected Results**:
- Container should use the custom TEAMKEY from environment variable
- Flag in the generated ZIP should be based on the custom key
- Flag format should be `FF{SHA256 hash}`

## 4. Performance Tests

### TC-006: Multi-Browser Access to Containerized App
**Description**: Test multiple concurrent users accessing the containerized application.

**Prerequisites**:
- Container running with Docker Compose

**Steps**:
1. Access the web interface from multiple browsers simultaneously
2. Monitor container performance during concurrent access
3. Check for any race conditions or resource conflicts

**Expected Results**:
- Application should handle concurrent users without errors
- Resources should be properly managed
- Each user should get proper progress updates

### TC-007: Flag Submission
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