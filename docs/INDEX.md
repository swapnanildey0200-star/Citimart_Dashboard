# Citimart Retail Analytics & Management Dashboard — Documentation Index

**System:** Citimart Retail Analytics & Management Dashboard  
**Version:** 1.1.0  
**Status:** Active Production Baseline  
**Last Updated:** November 2026  

---

## 1. Documentation Authority & Hierarchy

All development, features, and operational practices for the Citimart Dashboard must adhere to this documentation structure:

1. **Constitutional & Process Baseline**: [`constitution.md`](constitution.md), [`rules.md`](rules.md)
2. **Product Requirements & Behavior**: [`prd.md`](prd.md), [`acceptance-criteria.md`](acceptance-criteria.md), [`features/`](features/)
3. **Architecture, Persistence & API Contracts**: [`system-architecture.md`](system-architecture.md), [`database.md`](database.md), [`apis.md`](apis.md), [`adrs/`](adrs/)
4. **Implementation & Operational Controls**: [`security.md`](security.md), [`code-testing.md`](code-testing.md), [`deployment.md`](deployment.md), [`runbook.md`](runbook.md)
5. **Execution & State Memory**: [`task.md`](task.md), [`plan.md`](plan.md), [`memory.md`](memory.md), [`CHANGELOG.md`](CHANGELOG.md)

---

## 2. Master Document Registry

### Core Product & Architecture Specifications
| Document | Purpose | Primary Audience |
| :--- | :--- | :--- |
| [`prd.md`](prd.md) | Product Requirements Document: The 4-Question Framework, 10 Views, user personas, functional specifications (REQ-001 to REQ-010). | Product Managers, Engineers |
| [`system-architecture.md`](system-architecture.md) | System Architecture: C4 diagrams, ingestion engine, analytical processing, fallback store, React UI. | Architects, Lead Engineers |
| [`tech-stacks.md`](tech-stacks.md) | Technology Stack: FastAPI, React 19, Vite, Tailwind CSS v4, MongoDB Atlas, Motor, Pandas. | All Developers |
| [`database.md`](database.md) | Persistence Architecture: Schema models (Sales, Inventory, Purchases, Products, Stores), compound indexes, resilient in-memory fallback. | Backend Engineers, DBAs |
| [`apis.md`](apis.md) | REST API Specification: Endpoints, query parameters, payloads, responses for all 7 routers. | Frontend & Backend Engineers |
| [`design.md`](design.md) | UI & Design System: Desktop-first layout, color tokens, typography, Indian numbering (`₹` Lakhs/Crores), KPI components. | UI/UX Developers |

### Security, Quality & Operations
| Document | Purpose | Primary Audience |
| :--- | :--- | :--- |
| [`security.md`](security.md) | Security Architecture: Formula-injection protection, backend-only credentials, upload sanitization, CORS policy. | Security Engineers, Developers |
| [`code-testing.md`](code-testing.md) | Test Strategy & Pyramid: Unit tests, edge-case coverage (zero-division, empty sets), upload tests, running pytest. | QA, Developers |
| [`code-review.md`](code-review.md) | Code Review Standards: PR checklist, quality bars, linting, error handling standards. | Reviewers, Authors |
| [`performance.md`](performance.md) | Performance SLAs: <300ms API latency, batch ingestion speed, compound index efficiency. | Performance Engineers |
| [`observability.md`](observability.md) | Observability & Telemetry: Logging conventions, health check APIs, audit trail (`import_jobs`). | DevOps, Site Reliability |
| [`deployment.md`](deployment.md) | Production Deployment Guide: Vercel frontend rewrites, Render/Railway backend hosting, Atlas provisioning. | DevOps, Operations |
| [`environments.md`](environments.md) | Environments & Config: Development, Staging, Production configurations and environment variables. | Developers, DevOps |
| [`runbook.md`](runbook.md) | Operational Runbook: Starting services, re-seeding demo data, handling DB outages, bulk file fixes. | Support, Operators |
| [`error-tracker.md`](error-tracker.md) | Incident & Error Tracker: Past issues, root-cause analyses, prevention safeguards. | Engineers, Tech Leads |

### Project Execution & Tracking
| Document | Purpose | Primary Audience |
| :--- | :--- | :--- |
| [`task.md`](task.md) | Work Tracking & Tasks: Current sprint status, module readiness, pending backlog items. | Project Team |
| [`plan.md`](plan.md) | Development Roadmap: Phase milestones (MVP, Analytics Views, Ingestion Engine, Production Scale). | Stakeholders, Leads |
| [`memory.md`](memory.md) | State Memory & Context: Verified working endpoints, verified UI pages, current codebase snapshot. | AI Agents, Developers |
| [`acceptance-criteria.md`](acceptance-criteria.md) | Verification Criteria: Given/When/Then acceptance tests for each system module. | QA, Product Owners |
| [`requirements-traceability.md`](requirements-traceability.md) | Traceability Matrix: Mapping business requirements to schemas, endpoints, and test cases. | Compliance, QA |
| [`decision-log.md`](decision-log.md) | Decision Log: Business, architectural, and UI design decisions over project lifetime. | All Stakeholders |
| [`risk-register.md`](risk-register.md) | Risk Register: Technical and operational risks, severity, probability, and mitigations. | Project Managers |
| [`phases.md`](phases.md) | Delivery Milestones: Release phases and milestone sign-off criteria. | Leadership, PMs |
| [`release-checklist.md`](release-checklist.md) | Release Readiness Checklist: Pre-flight audit before shipping production code. | Release Managers |
| [`CHANGELOG.md`](CHANGELOG.md) | Product Changelog: Detailed version history of features, bug fixes, and improvements. | All Stakeholders |
| [`handoff.md`](handoff.md) | Project Handoff Guide: Repository onboarding, architectural summary, maintenance instructions. | Successor Engineers |

### Special Directories
- [`adrs/`](adrs/README.md) — Architectural Decision Records:
  - [`ADR-0001-resilient-in-memory-fallback.md`](adrs/ADR-0001-resilient-in-memory-fallback.md)
  - [`ADR-0002-four-question-management-framework.md`](adrs/ADR-0002-four-question-management-framework.md)
  - [`ADR-0003-formula-injection-protection.md`](adrs/ADR-0003-formula-injection-protection.md)
- [`features/`](features/FEATURE-TEMPLATE.md) — Detailed Feature Specifications:
  - [`FEAT-001-upload-validation-pipeline.md`](features/FEAT-001-upload-validation-pipeline.md)
  - [`FEAT-002-executive-dashboard-and-decision-card.md`](features/FEAT-002-executive-dashboard-and-decision-card.md)
  - [`FEAT-003-inventory-ageing-and-velocity.md`](features/FEAT-003-inventory-ageing-and-velocity.md)
- [`domains/`](domains/README.md) — Domain definitions for retail intelligence, POS registers, and inventory velocity.
