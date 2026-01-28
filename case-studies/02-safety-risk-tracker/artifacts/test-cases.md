# Test Cases
## Safety & Risk Management System

---

## 1. Testing Strategy

### 1.1 Testing Levels

#### 1.1.1 Unit Testing
- Scope: Individual components and services  
- Tools: pytest, Jest  

#### 1.1.2 Integration Testing
- Scope: Service-to-service communication  
- Scope: Database interactions  

#### 1.1.3 API Testing
- Scope: REST endpoint validation  
- Tools: Postman, pytest  

#### 1.1.4 UI Testing
- Scope: Mobile application  
- Scope: Web dashboard  
- Tools: Appium, Cypress  

#### 1.1.5 Performance Testing
- Scope: Load testing  
- Scope: Stress testing  
- Scope: Scalability testing  
- Tools: Locust, k6  

#### 1.1.6 Security Testing
- Scope: Authentication  
- Scope: Authorization  
- Scope: Data protection  
- Tools: OWASP ZAP, SonarQube  

#### 1.1.7 User Acceptance Testing (UAT)
- Scope: End-to-end business scenarios  
- Participants: Business stakeholders  

#### 1.1.8 Accessibility Testing
- Standard: WCAG 2.1 AA  
- Tools: axe-core  

---

### 1.2 Testing Environment Strategy

#### 1.2.1 Environment Matrix

| Environment | Purpose                    | Data Type                  | Refresh Cycle |
|------------|----------------------------|----------------------------|---------------|
| Dev        | Development / Unit Testing | Synthetic Data             | Daily         |
| QA         | Integration Testing        | Synthetic Data             | Weekly        |
| Staging    | Pre-production Testing     | Anonymized Production Data | Monthly       |


## 2. Functional Test Cases

### 2.1 Authentication & Authorization

**TC-AUTH-001: Successful User Login**
- **Test ID:** AUTH-001
- **Priority:** Critical
- **Precondition:** Valid user account exists in system
- **Test Steps:**
  1. Navigate to login page (web/mobile)
  2. Enter valid username and password
  3. Click "Login" button
  4. Verify redirection to dashboard
- **Expected Result:** User is successfully logged in, session established, dashboard loads within 3 seconds
- **Automation Status:** Automated

**TC-AUTH-002: Invalid Login Attempt**
- **Test ID:** AUTH-002
- **Priority:** High
- **Precondition:** None
- **Test Steps:**
  1. Navigate to login page
  2. Enter invalid username
  3. Enter invalid password
  4. Click "Login" button
- **Expected Result:** Error message displayed "Invalid username or password", session not established
- **Automation Status:** Automated

**TC-AUTH-003: Role-Based Access Control**
- **Test ID:** AUTH-003
- **Priority:** High
- **Precondition:** Test users exist for each role (Field Worker, Safety Officer, Manager, Admin)
- **Test Steps:**
  1. Login as Field Worker
  2. Attempt to access admin functions
  3. Login as Safety Officer
  4. Attempt to access manager functions
  5. Login as Manager
  6. Attempt to access admin functions
  7. Login as Admin
  8. Verify access to all functions
- **Expected Result:** Access denied (403) for unauthorized functions
- **Automation Status:** Automated

### 2.2 Hazard Reporting

**TC-HAZARD-001: Create Complete Hazard Report**
- **Test ID:** HAZ-001
- **Priority:** Critical
- **Precondition:** User logged in as Field Worker
- **Test Steps:**
  1. Click "Report New Hazard" button
  2. Enter title: "Exposed electrical wiring"
  3. Select hazard type: "Electrical"
  4. Set severity: 4 (High)
  5. Set likelihood: 3 (Medium)
  6. Enter description
  7. Attach photo
  8. Verify location capture
  9. Click "Submit Report"
- **Expected Result:** Report created successfully, confirmation message, report ID generated, risk score calculated (12 = HIGH)
- **Automation Status:** Automated

**TC-HAZARD-002: Offline Hazard Reporting**
- **Test ID:** HAZ-002
- **Priority:** High
- **Precondition:** Mobile device in airplane mode
- **Test Steps:**
  1. Create hazard report offline
  2. Save draft locally
  3. Re-enable internet connectivity
  4. Verify automatic sync occurs
- **Expected Result:** Report saved locally, sync triggered when online, data integrity maintained
- **Automation Status:** Manual

**TC-HAZARD-003: Hazard Validation**
- **Test ID:** HAZ-003
- **Priority:** High
- **Precondition:** None
- **Test Steps:**
  1. Attempt to submit empty report
  2. Attempt to submit with title exceeding 255 characters
  3. Attempt to submit with invalid location data
  4. Attempt to attach file > 10MB
- **Expected Result:** Appropriate validation errors displayed, user-friendly error messages
- **Automation Status:** Automated

### 2.3 Risk Assessment

**TC-RISK-001: Automatic Risk Score Calculation**
- **Test ID:** RISK-001
- **Priority:** Critical
- **Precondition:** Hazard report created
- **Test Steps:**
  1. Create hazard with severity=5, likelihood=5
  2. Verify risk score = 25
  3. Create hazard with severity=2, likelihood=2
  4. Verify risk score = 4
  5. Create hazard with severity=4, likelihood=3
  6. Verify risk score = 12
- **Expected Result:** Risk scores calculated correctly per 5x5 matrix, risk level categorized correctly
- **Automation Status:** Automated

**TC-RISK-002: Manual Risk Assessment Override**
- **Test ID:** RISK-002
- **Priority:** High
- **Precondition:** Safety Officer role, hazard report exists
- **Test Steps:**
  1. View hazard details
  2. Override automatic risk score from 12 to 20
  3. Provide justification
  4. Save override
  5. View audit trail
- **Expected Result:** Manual score applied, justification saved, audit trail records change
- **Automation Status:** Automated

### 2.4 Workflow Management

**TC-WF-001: Automatic Hazard Assignment**
- **Test ID:** WF-001
- **Priority:** Critical
- **Precondition:** Multiple Safety Officers available
- **Test Steps:**
  1. Submit critical hazard (risk score 20+)
  2. Monitor assignment queue
  3. Verify assignment within 5 minutes
  4. Check workload distribution
- **Expected Result:** Hazard automatically assigned based on rules, notification sent to assignee
- **Automation Status:** Automated

**TC-WF-002: Workflow Status Transitions**
- **Test ID:** WF-002
- **Priority:** High
- **Precondition:** Hazard assigned to test user
- **Test Steps:**
  1. Change status from Assigned to In Progress
  2. Add progress notes
  3. Change status to Resolved
  4. Add resolution details
  5. Change status to Closed
- **Expected Result:** Valid status changes saved, notes required for transitions, audit trail maintained
- **Automation Status:** Automated

### 2.5 Dashboard & Reporting

**TC-DASH-001: Real-time Dashboard Updates**
- **Test ID:** DASH-001
- **Priority:** Critical
- **Precondition:** Dashboard open in browser
- **Test Steps:**
  1. Submit new hazard report from mobile app
  2. Monitor dashboard metrics update
  3. Verify update within 10 seconds
- **Expected Result:** Dashboard updates in real-time without refresh
- **Automation Status:** Manual

**TC-DASH-002: Report Generation**
- **Test ID:** DASH-002
- **Priority:** High
- **Precondition:** Test data exists for date range
- **Test Steps:**
  1. Navigate to reports section
  2. Select date range (last 30 days)
  3. Select site filter
  4. Generate compliance report
  5. Export to PDF
  6. Export to Excel
- **Expected Result:** Reports generated within 2 minutes, all data included, formats correct
- **Automation Status:** Automated

### 2.6 Notifications

**TC-NOTIF-001: Multi-channel Notification Delivery**
- **Test ID:** NOTIF-001
- **Priority:** Critical
- **Precondition:** User has email and SMS configured
- **Test Steps:**
  1. Submit critical hazard report
  2. Check email inbox for notification
  3. Check SMS received
  4. Check mobile app push notification
- **Expected Result:** Notifications delivered on all configured channels within 1 minute
- **Automation Status:** Semi-automated

**TC-NOTIF-002: User Notification Preferences**
- **Test ID:** NOTIF-002
- **Priority:** Medium
- **Precondition:** User logged in
- **Test Steps:**
  1. Navigate to notification settings
  2. Disable email notifications
  3. Enable SMS for critical only
  4. Set quiet hours
  5. Save preferences
  6. Trigger test notifications
- **Expected Result:** Preferences saved and respected, quiet hours honored
- **Automation Status:** Automated

## 3. Performance Test Cases

**TC-PERF-001: Peak Load - 500 Concurrent Users**
- **Test ID:** PERF-001
- **Priority:** High
- **Scenario:** Simulate 500 concurrent users during morning peak
- **Acceptance Criteria:**
  - 95% of API requests < 2 seconds response time
  - Error rate < 1%
  - CPU utilization < 80%
  - Memory utilization < 85%
- **Tools:** Locust/k6

**TC-PERF-002: Hazard Report Submission Load**
- **Test ID:** PERF-002
- **Priority:** High
- **Scenario:** 100 reports/minute during incident response
- **Acceptance Criteria:**
  - All reports processed within 5 minutes
  - No data loss
  - Database response times stable
  - File storage handles uploads

## 4. Security Test Cases

**TC-SEC-001: Password Policy Enforcement**
- **Test ID:** SEC-001
- **Priority:** High
- **Test Steps:**
  1. Attempt to set password less than 12 characters
  2. Attempt password without complexity
  3. Test password history
  4. Test account lockout after failed attempts
- **Expected Result:** Password policy enforced, meaningful error messages

**TC-SEC-002: SQL Injection Prevention**
- **Test ID:** SEC-002
- **Priority:** Critical
- **Test Steps:**
  1. Attempt SQL injection via API parameters
  2. Attempt SQL injection via form fields
- **Expected Result:** Injection attempts blocked, no data exposure

**TC-SEC-003: Cross-Site Scripting (XSS) Prevention**
- **Test ID:** SEC-003
- **Priority:** High
- **Test Steps:**
  1. Enter script tags in text fields
  2. Test stored XSS
  3. Test reflected XSS
  4. Verify CSP headers
- **Expected Result:** XSS payloads neutralized, CSP headers present

## 5. Usability Test Cases

**TC-USA-001: Mobile App Usability with Work Gloves**
- **Test ID:** USA-001
- **Priority:** High
- **Test Steps:**
  1. Wear standard work gloves
  2. Complete hazard report workflow
  3. Test button sizes and spacing
  4. Test in bright sunlight conditions
- **Expected Result:** App remains usable in field conditions

**TC-USA-002: Learning Curve**
- **Test ID:** USA-002
- **Priority:** Medium
- **Test Steps:**
  1. New user completes onboarding
  2. Time first complete hazard report
  3. Survey user satisfaction
  4. Measure error rate for first 10 reports
- **Acceptance Criteria:** First report completed in < 5 minutes, error rate < 10%

## 6. Exit Criteria

### 6.1 Release Readiness Criteria
- ✅ All critical/high severity defects resolved
- ✅ Test automation passing rate > 95%
- ✅ Performance test targets met
- ✅ Security assessment passed
- ✅ User acceptance testing signed off
- ✅ Documentation updated
- ✅ Disaster recovery test completed

### 6.2 Go/No-Go Checklist
- [ ] Functional testing complete
- [ ] Regression testing complete
- [ ] Performance testing within SLA targets
- [ ] Security testing passed
- [ ] UAT signed off by business stakeholders
- [ ] Production deployment plan reviewed
- [ ] Rollback plan documented and tested
- [ ] Support team trained and ready
