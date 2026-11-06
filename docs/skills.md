# Skills

> **Document class:** Controlled process guideline  
> **Framework:** Vibe Coding  
> **Guideline baseline:** 1.0.0  
> **Status:** Template; project-specific content requires review  

## Purpose

Registry of portable reusable agent skills.

## Agent read trigger

**MUST** read or consult this file: Before skill creation, modification or invocation.

## Normative sections and rules

### 1. Catalog

- **MUST** — Maintain name, role, owner, version, goal, trigger and applicability.

### 2. Contract

- **MUST** — Specify mandatory context, inputs, outputs and allowed tools.

### 3. Execution

- **MUST** — Specify steps, quality checks, stop conditions and escalation.

### 4. Security

- **MUST** — Evaluate privileges and trust boundary for installed or imported skills.

### 5. Tests

- **SHOULD** — Evaluate skill output with example cases and regressions.

### 6. Lifecycle

- **MUST** — Record approval, deprecation and retirement.

### 7. Suggested skills

- **SHOULD** — Cover requirements, spec validation, architecture, planning, TDD, UI review, API/data checks, security, accessibility, debugging, release and ML evaluation.

## Evidence and change control

- **MUST** record owner, revision/date, relevant approval reference, and traceable evidence in the applicable project instantiation.
- **MUST** route changes to process rules through `docs/guideline-CHANGELOG.md` and formal baseline revision; route feature behavior through approved versioned specs and `docs/CHANGELOG.md`.
- **SHOULD** keep links to canonical artifacts instead of duplicating definitions.

## Vibe Coding interpretation

- **MAY** use provisional decisions in an isolated prototype, clearly marked `DRAFT`; **MUST** formalize and approve production-bound behavior before shipping.
