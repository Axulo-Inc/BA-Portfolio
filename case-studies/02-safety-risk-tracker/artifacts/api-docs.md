# API Documentation
## Safety & Risk Management System

## Base Information
- **Base URL:** `https://api.safety-system.company.com/v1`
- **Authentication:** Bearer Token required
- **Rate Limit:** 100 requests/minute per user

## 1. Authentication Endpoints

### 1.1 Login
**POST** `/auth/login`

**Request:**
```json
{
  "username": "user@company.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "USER001",
    "name": "John Smith",
    "roles": ["SAFETY_OFFICER"]
  }
}
```

### 1.2 Token Refresh
**POST** `/auth/refresh`

**Response:**
```json
{
  "access_token": "new_token_here",
  "expires_in": 3600
}
```

## 2. Hazard Management Endpoints

### 2.1 Create Hazard Report
**POST** `/hazards`

**Request:**
```json
{
  "title": "Exposed electrical wiring",
  "description": "Electrical panel left open",
  "location": {
    "site": "PIT-A",
    "area": "Processing Plant"
  },
  "hazard_type": "ELECTRICAL",
  "severity": "HIGH",
  "likelihood": "MEDIUM"
}
```

**Response (201 Created):**
```json
{
  "id": "HAZ-20240120-001",
  "status": "SUBMITTED",
  "priority": "HIGH",
  "risk_score": 12,
  "estimated_resolution": "2024-01-20T12:30:00Z"
}
```

### 2.2 Get Hazard Details
**GET** `/hazards/{hazard_id}`

**Response (200 OK):**
```json
{
  "id": "HAZ-20240120-001",
  "title": "Exposed electrical wiring",
  "status": "ASSIGNED",
  "priority": "HIGH",
  "reporter": "John Smith",
  "assignee": "Sarah Johnson",
  "created_at": "2024-01-20T08:30:00Z"
}
```

## 3. Dashboard Endpoints

### 3.1 Get Dashboard Summary
**GET** `/dashboard/summary`

**Response:**
```json
{
  "hazards": {
    "total": 45,
    "by_status": {
      "SUBMITTED": 3,
      "ASSIGNED": 10,
      "IN_PROGRESS": 25,
      "RESOLVED": 5,
      "CLOSED": 2
    }
  },
  "compliance": {
    "rate": 92.5,
    "target": 95.0
  }
}
```

## 4. Error Responses

### 4.1 Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {"field": "title", "message": "Cannot be empty"}
    ]
  }
}
```

## 5. Support
- **Documentation:** Internal Confluence page
- **Support Email:** safety-support@company.com
- **Emergency Contact:** Safety Team Lead (ext. 5555)
