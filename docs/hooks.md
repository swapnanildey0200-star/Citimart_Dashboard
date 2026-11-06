# Hooks

> **Document class:** Controlled process guideline  
> **Framework:** Vibe Coding  
> **Guideline baseline:** 1.0.0  
> **Status:** Template; project-specific content requires review  

## Purpose

Event-driven agent and Git automation controls.

## Agent read trigger

**MUST** read or consult this file: Before registering or changing execution hooks.

## Normative sections and rules

### 1. Registry

- **MUST** — List event, trigger, owner, executable action and affected tools.

### 2. Safety

- **MUST** — Define privileges, allowlisted commands, input sanitization, timeouts and side effects.

### 3. Failure

- **MUST** — Define fail-open/closed behavior, retriability, idempotence and audit trail.

### 4. Validation

- **MUST** — Test hook behavior and safe rollback prior to activation.

### 5. Gates

- **MUST** — Enforce spec checks before edits where supported, security/lint pre-commit and CI verification pre-merge.

### 6. Fallback

- **MUST** — Use server-side CI or review when agent platforms cannot enforce a required hook.

## Evidence and change control

- **MUST** record owner, revision/date, relevant approval reference, and traceable evidence in the applicable project instantiation.
- **MUST** route changes to process rules through `docs/guideline-CHANGELOG.md` and formal baseline revision; route feature behavior through approved versioned specs and `docs/CHANGELOG.md`.
- **SHOULD** keep links to canonical artifacts instead of duplicating definitions.

## Vibe Coding interpretation

- **MAY** use provisional decisions in an isolated prototype, clearly marked `DRAFT`; **MUST** formalize and approve production-bound behavior before shipping.
