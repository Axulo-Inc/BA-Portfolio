# System Architecture
## Safety & Risk Management System

## 1. Architecture Overview

### 1.1 High-Level Architecture
┌─────────────────────────────────────────────────────────────┐
│ Presentation Layer │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ Mobile │ │ Web │ │ Admin │ │ API │ │
│ │ App │ │ Dashboard│ │ Portal │ │ Gateway │ │
│ │ (React │ │ (React │ │ (React │ │ (nginx/ │ │
│ │ Native) │ │ JS) │ │ JS) │ │ Kong) │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────┐
│ Business Logic Layer │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ User │ │ Hazard │ │ Risk │ │ Notification│ │
│ │ Service │ │ Service │ │ Service │ │ Service │ │
│ │ (FastAPI)│ │ (FastAPI)│ │ (FastAPI)│ │ (FastAPI) │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│ │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ Analytics│ │ Workflow │ │ Reporting│ │ Audit │ │
│ │ Service │ │ Service │ │ Service │ │ Service │ │
│ │ (FastAPI)│ │ (FastAPI)│ │ (FastAPI)│ │ (FastAPI) │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────┐
│ Data Layer │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ PostgreSQL│ │ Redis │ │ S3/Blob │ │ Elastic- │ │
│ │ Database │ │ Cache │ │ Storage │ │ search │ │
│ │ (Primary)│ │ (Session,│ │ (Photos, │ │ (Logs, │ │
│ │ │ │ Cache) │ │ Docs) │ │ Search) │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────┐
│ Integration Layer │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ SSO │ │ SMS │ │ Email │ │ HR │ │
│ │ (AD/LDAP)│ │ Gateway │ │ Service │ │ System │ │
│ │ │ │ (Twilio) │ │ (SMTP) │ │ (API) │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────┘

text

### 1.2 Technology Stack
- **Frontend Mobile:** React Native (iOS & Android) with TypeScript
- **Frontend Web:** React.js with TypeScript, Material-UI
- **Backend:** Python 3.9+ with FastAPI microservices
- **API Gateway:** nginx/Kong for routing, rate limiting, authentication
- **Database:** PostgreSQL 14 (primary), Redis 7 (cache)
- **Message Queue:** RabbitMQ 3.11 for async processing
- **Storage:** AWS S3/MinIO for media files, documents
- **Search:** Elasticsearch 8.x for reporting and analytics
- **Monitoring:** Prometheus + Grafana + ELK Stack
- **Containerization:** Docker, Kubernetes (EKS/on-prem)
- **CI/CD:** GitLab CI/CD, ArgoCD for GitOps

## 2. Microservices Architecture

### 2.1 Service Breakdown

#### **User Service**
- **Purpose:** Authentication, authorization, user profile management
- **Endpoints:** `/auth/*`, `/users/*`, `/roles/*`, `/permissions/*`
- **Database:** PostgreSQL (users, roles, permissions, sessions)
- **Dependencies:** Company Active Directory/LDAP for SSO integration
- **Key Features:** JWT token generation/validation, password reset, session management

#### **Hazard Service**
- **Purpose:** Core hazard reporting and lifecycle management
- **Endpoints:** `/hazards/*`, `/attachments/*`, `/locations/*`
- **Database:** PostgreSQL (hazards, attachments, comments, locations)
- **Key Features:** Offline sync, photo upload with compression, GPS location tracking, draft saving, bulk operations

#### **Risk Service**
- **Purpose:** Risk assessment, scoring, and matrix management
- **Endpoints:** `/risk/*`, `/matrix/*`, `/assessments/*`
- **Database:** PostgreSQL (risk assessments, matrices, overrides, history)
- **Key Features:** 5x5 risk matrix calculation, automatic scoring, manual override with audit trail, configurable matrices

#### **Notification Service**
- **Purpose:** Multi-channel notification delivery and management
- **Endpoints:** `/notifications/*`, `/templates/*`, `/channels/*`
- **Integrations:** Email (SMTP/Exchange), SMS (Twilio), Push (Firebase/APNS), In-app
- **Key Features:** Template management, delivery tracking, retry logic, user preferences, escalation handling

#### **Workflow Service**
- **Purpose:** Hazard assignment, escalation, and status management
- **Endpoints:** `/workflow/*`, `/assignments/*`, `/escalations/*`
- **Database:** PostgreSQL (workflow rules, assignments, escalations, history)
- **Key Features:** Rule-based auto-assignment, load balancing, escalation triggers, SLA tracking, approval workflows

#### **Analytics Service**
- **Purpose:** Reporting, dashboard data, and business intelligence
- **Endpoints:** `/analytics/*`, `/dashboard/*`, `/reports/*`
- **Database:** PostgreSQL + Elasticsearch (for search and aggregation)
- **Key Features:** Real-time aggregation, trend analysis, predictive analytics, scheduled reports, data export

#### **Audit Service**
- **Purpose:** Comprehensive audit trail and compliance logging
- **Endpoints:** `/audit/*`, `/logs/*`
- **Database:** PostgreSQL (audit logs) + Elasticsearch (for search)
- **Key Features:** Immutable logging, change tracking, compliance reporting, investigation tools

### 2.2 Communication Patterns
- **Synchronous:** REST APIs (JSON) between services via API Gateway
- **Asynchronous:** RabbitMQ for event-driven communication (publish/subscribe)
- **Event Types:** `hazard.created`, `risk.assessed`, `notification.sent`, `workflow.assigned`
- **Service Discovery:** Consul for dynamic service registration and discovery
- **Circuit Breaking:** Resilience4j for fault tolerance
- **Caching:** Redis for frequent queries, session storage, rate limiting

## 3. Data Architecture

### 3.1 Database Schema (Key Tables)

```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) NOT NULL,
    site_id UUID,
    department VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hazard Reports
CREATE TABLE hazards (
    id VARCHAR(50) PRIMARY KEY,  -- Format: HAZ-YYYYMMDD-001
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    reporter_id UUID NOT NULL REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'SUBMITTED',
    hazard_type VARCHAR(100) NOT NULL,
    severity INT CHECK (severity BETWEEN 1 AND 5),
    likelihood INT CHECK (likelihood BETWEEN 1 AND 5),
    risk_score INT GENERATED ALWAYS AS (severity * likelihood) STORED,
    risk_level VARCHAR(20) GENERATED ALWAYS AS (
        CASE 
            WHEN (severity * likelihood) <= 3 THEN 'LOW'
            WHEN (severity * likelihood) <= 6 THEN 'MEDIUM'
            WHEN (severity * likelihood) <= 12 THEN 'HIGH'
            ELSE 'CRITICAL'
        END
    ) STORED,
    location JSONB NOT NULL,  -- {site: "PIT-A", area: "Processing", gps: {lat: xx, lng: xx}}
    attachments TEXT[],  -- Array of S3/MinIO paths
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    resolved_by UUID REFERENCES users(id)
);

-- Risk Assessments
CREATE TABLE risk_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hazard_id VARCHAR(50) NOT NULL REFERENCES hazards(id),
    assessor_id UUID REFERENCES users(id),
    automatic_score INT,
    manual_score INT,
    final_score INT,
    justification TEXT,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflow Assignments
CREATE TABLE assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hazard_id VARCHAR(50) NOT NULL REFERENCES hazards(id),
    assignee_id UUID NOT NULL REFERENCES users(id),
    assigned_by UUID REFERENCES users(id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    completed_at TIMESTAMP
);

-- Audit Trail
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(100) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
3.2 Data Flow
Mobile App → API Gateway → Hazard Service (Create hazard report)

Hazard Service → RabbitMQ → Risk Service (Trigger risk assessment)

Risk Service → RabbitMQ → Workflow Service (Assign based on risk)

Workflow Service → RabbitMQ → Notification Service (Notify assignee)

All Services → PostgreSQL (Persist data)

Analytics Service → Elasticsearch (Index for fast search/aggregation)

Audit Service ← All Services (Log all actions via events)

3.3 Data Migration Strategy
Phase 1: New system operates alongside legacy for 1 month

Phase 2: Historical data migration (last 2 years of records)

Phase 3: Legacy system decommission after UAT sign-off

4. Deployment Architecture
4.1 Cloud Deployment (AWS - Recommended)
text
Region: us-east-1 (Primary), us-west-2 (DR)
├── VPC with Public/Private Subnets (3-tier architecture)
│   ├── Public Subnet: Internet-facing load balancers, API Gateway
│   ├── Private Subnet: Application microservices (EKS pods)
│   └── Data Subnet: Databases, caching, storage (no direct internet)
├── Amazon EKS Cluster (Kubernetes)
│   ├── Microservices Pods (auto-scaling: 2-10 replicas based on CPU/memory)
│   ├── Redis Cluster (ElastiCache - cache.t3.medium x 3)
│   └── RabbitMQ Cluster (Amazon MQ - mq.t3.micro)
├── Amazon RDS PostgreSQL (db.t3.large, Multi-AZ for HA)
├── Amazon S3 Buckets (media storage with lifecycle policies)
├── Amazon CloudFront (CDN for static web assets)
├── Amazon Elasticsearch Service (for analytics and logging)
└── AWS WAF + Shield (DDoS protection and web application firewall)
4.2 On-Premises Deployment (For sites with no cloud connectivity)
text
Data Center (Primary Site)
├── Kubernetes Cluster (Rancher RKE2/OpenShift)
│   ├── Microservices Containers (deployed via Helm charts)
│   ├── Redis Sentinel Cluster (3 nodes for high availability)
│   └── RabbitMQ Cluster (3 nodes with mirrored queues)
├── PostgreSQL Cluster (Patroni with 3 nodes + 1 witness)
├── MinIO Cluster (4 nodes for S3-compatible object storage)
├── HAProxy Load Balancer (with SSL termination)
├── Network File System (NFS for shared storage)
└── Backup System (Veeam/Zerto for disaster recovery)
4.3 Hybrid Approach (Recommended for Mining Operations)
Cloud Primary: Main deployment in AWS for headquarters and well-connected sites

Edge Deployment: Lightweight Kubernetes at remote sites with poor connectivity

Data Sync: Bidirectional synchronization between cloud and edge deployments

Conflict Resolution: Last-write-wins with manual override for critical conflicts

4.4 Deployment Topology per Site Size
Large Sites (100+ users): Full microservices deployment

Medium Sites (20-100 users): Combined services (2-3 pods instead of 8)

Small Sites (<20 users): Single container with all services (for very remote locations)

Mobile-Only: API-only deployment for field teams with satellite connectivity

5. Security Architecture
5.1 Authentication & Authorization
OAuth 2.0 / OpenID Connect with company Active Directory as identity provider

JWT tokens (RS256) for stateless API authentication (15-minute expiry)

Refresh tokens for session persistence (7-day expiry, single-use)

Role-Based Access Control (RBAC) with hierarchical permissions

Attribute-Based Access Control (ABAC) for complex rules (site-specific access)

API Keys for system-to-system communication (service accounts)

Multi-factor Authentication (MFA) for administrative access

5.2 Data Protection
TLS 1.3 for all external and internal communications

AES-256-GCM encryption for data at rest (database, file storage)

Field-level encryption for sensitive PII data (employee information)

Key management via AWS KMS (cloud) or HashiCorp Vault (on-prem)

Data masking in logs and non-production environments

Secure key rotation automated via CI/CD pipeline

5.3 Network Security
VPC/Network segmentation with security groups (least privilege principle)

Web Application Firewall (WAF) rules for OWASP Top 10 protection

DDoS protection via AWS Shield/CloudFront or on-prem equivalent

VPN access only for administrative functions

Network intrusion detection (Suricata/Snort) for on-prem deployments

Regular vulnerability scanning (Nessus/Qualys) of all components

5.4 Application Security
Input validation and sanitization at all layers

SQL injection prevention via parameterized queries (SQLAlchemy)

Cross-Site Scripting (XSS) protection via CSP headers and output encoding

Cross-Site Request Forgery (CSRF) protection for state-changing operations

Rate limiting per user/IP (Redis-based sliding window)

Security headers (HSTS, X-Frame-Options, X-Content-Type-Options)

5.5 Compliance & Auditing
GDPR/CCPA compliance: Right to be forgotten, data portability

Industry compliance: ISO 45001 (Occupational Health and Safety)

Regular security audits: Quarterly internal, annual external

Penetration testing: Biannual by certified third-party

Incident response plan: Documented and tested semi-annually

6. Scalability & Performance
6.1 Horizontal Scaling Strategy
Stateless services: Scale out easily based on CPU/memory metrics

Database scaling: Read replicas for reporting, connection pooling (PgBouncer)

Cache scaling: Redis cluster with sharding for large datasets

Message queue scaling: RabbitMQ cluster with mirrored queues

Storage scaling: S3/MinIO automatically scales with usage

6.2 Performance Targets
API Response Time: < 200ms for 95% of requests (p95)

Mobile App Load Time: < 3 seconds on 4G networks

Dashboard Refresh: < 5 seconds with 10,000 active records

Report Generation: < 2 minutes for 12-month dataset

Concurrent Users: 500+ supported with linear scaling

Data Sync: < 30 seconds for offline-to-online synchronization

6.3 Caching Strategy
L1 Cache: In-memory (service level, short-lived)

L2 Cache: Redis (distributed, 5-minute TTL for dynamic data)

L3 Cache: CDN (CloudFront, 24-hour TTL for static assets)

Cache Invalidation: Event-driven via RabbitMQ messages

Cache Warming: Pre-load frequently accessed data at service startup

6.4 Database Optimization
Indexing Strategy: B-tree for equality, BRIN for time-series, GIN for JSON

Partitioning: Monthly partitioning for large tables (hazards, audit_logs)

Connection Pooling: 100 connections per service, managed by PgBouncer

Read Replicas: 2 replicas for reporting and analytics queries

Query Optimization: Regular EXPLAIN ANALYZE, slow query logging

7. Monitoring & Observability
7.1 Metrics Collection (Prometheus)
Infrastructure: CPU, memory, disk I/O, network bandwidth

Application: Request rate, error rate, latency (p50, p95, p99)

Business: Hazards reported/hour, resolution time, compliance rate

Database: Query performance, connection count, replication lag

Custom Metrics: Risk score distribution, notification delivery rate

7.2 Logging (ELK Stack)
Structured logging in JSON format (log level, timestamp, correlation ID)

Centralized log aggregation via Filebeat → Logstash → Elasticsearch

Log retention: 30 days (standard logs), 1 year (audit logs), 7 years (compliance)

Log analysis: Kibana dashboards for troubleshooting and analysis

Alerting: Anomaly detection in log patterns

7.3 Distributed Tracing (Jaeger)
End-to-end tracing across microservices for request flow

Performance analysis: Identify bottlenecks in service calls

Dependency mapping: Auto-discover service dependencies

Root cause analysis: Trace errors across service boundaries

7.4 Alerting & Notification
Alert Levels: Critical, Warning, Info (different response times)

Notification Channels: PagerDuty (Critical), Email (Warning), Slack (Info)

Escalation Policies: Auto-escalate if alert not acknowledged

Runbooks: Documented procedures for common alerts

Alert Fatigue Prevention: Deduplication, grouping, quiet periods

8. Disaster Recovery & Business Continuity
8.1 Backup Strategy
Database: Hourly incremental backups, daily full backups (retained for 30 days)

Object Storage: Versioning enabled on S3/MinIO, cross-region replication

Configuration: Infrastructure as Code (Terraform), versioned in Git

Application Code: Git repositories with CI/CD pipeline

Backup Testing: Monthly restoration tests to verify integrity

8.2 Recovery Objectives
RTO (Recovery Time Objective): 4 hours for critical systems

RPO (Recovery Point Objective): 1 hour (maximum data loss)

Data Integrity: Zero data loss for committed transactions

Service Restoration: Priority order: Database → Core Services → UI

8.3 Disaster Recovery Plan
Detection: Automated monitoring detects outage

Declaration: DR team declares disaster based on criteria

Failover: Traffic routed to DR region, databases promoted

Recovery: Services started in DR environment

Validation: Functional testing confirms system operation

Communication: Stakeholders notified of status

Failback: Return to primary after issue resolution

9. Integration Points
9.1 External Systems
HR System (Workday/SAP): Daily user synchronization (batch job at 2 AM)

Active Directory/LDAP: Real-time authentication, group membership

Email System (Exchange/Office 365): SMTP for notifications

SMS Gateway (Twilio): REST API for critical alerts

Push Notification (Firebase/APNS): Mobile app notifications

BI Tools (Power BI/Tableau): ODBC connection for advanced analytics

Document Management (SharePoint): API for report archival

9.2 Internal Systems
Legacy Safety System: One-time data migration, then read-only API

Maintenance Management System: Integration for corrective actions

Training Management System: Competency records for hazard assignment

Incident Management System: Bidirectional sync for serious incidents

Asset Management System: Equipment data for hazard context

9.3 API Specifications
RESTful API Design: Resource-oriented, versioned (v1, v2)

OpenAPI/Swagger: Interactive documentation for all endpoints

API Versioning: URL-based (/api/v1/...), backward compatibility for 1 year

Rate Limiting: 100 requests/minute per user, 1000/minute per API key

Throttling: Gradual response slowdown instead of hard cutoff

10. Development & Deployment
10.1 Development Workflow
Git Flow: feature branches → develop → release → main

Code Review: Mandatory pull requests with 2 approvals

Testing: Unit → Integration → E2E in CI pipeline

Environment Promotion: Dev → QA → Staging → Production

10.2 CI/CD Pipeline
text
Code Commit → GitLab CI
  ├── Lint/Format (black, eslint) 
  ├── Unit Tests (pytest, jest) → SonarQube Analysis
  ├── Build Docker Images → Push to Registry
  ├── Integration Tests (Testcontainers)
  └── Deploy to Environment (ArgoCD)
10.3 Environment Strategy
Development: 1 namespace per developer, ephemeral databases

QA: Stable environment for manual testing, test data refreshed weekly

Staging: Identical to production, used for final validation

Production: Multi-region deployment with blue/green deployments

11. Future Considerations & Roadmap
11.1 Phase 2 (Next 6-12 Months)
AI/ML Integration: Predictive hazard detection from historical patterns

IoT Sensor Integration: Real-time equipment monitoring data

Computer Vision: Automatic hazard detection from camera feeds

Blockchain: Immutable audit trail for compliance-critical actions

AR/VR: Hazard visualization for training and investigation

11.2 Phase 3 (12-24 Months)
Natural Language Processing: Voice-based hazard reporting

Wearable Integration: Safety sensors on personnel

Digital Twin: Virtual replica of physical sites for simulation

Advanced Analytics: Prescriptive recommendations for safety improvements

Global Deployment: Support for additional languages, regions, regulations

11.3 Technology Evolution
Serverless Components: AWS Lambda for sporadic workloads

Edge Computing: More processing at remote sites for latency reduction

Quantum-Safe Cryptography: Prepare for post-quantum security

5G Integration: Leverage high-speed mobile networks for real-time video

12. Support & Maintenance
12.1 Support Levels
Level 1: Help desk (password reset, basic usage)

Level 2: Application support (bug reports, feature requests)

Level 3: Development team (critical bugs, enhancements)

12.2 Maintenance Windows
Weekly: Security patches, minor updates (Saturday 2-4 AM)

Monthly: Feature releases, database maintenance (Sunday 12-4 AM)

Quarterly: Major upgrades, infrastructure changes (Scheduled with stakeholders)

12.3 Documentation
User Documentation: Online help, video tutorials, quick reference guides

Administrator Documentation: Installation, configuration, troubleshooting

API Documentation: OpenAPI specs, code examples, SDKs

Operational Documentation: Runbooks, disaster recovery procedures
