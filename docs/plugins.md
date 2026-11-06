# Plugins

> **Document class:** Controlled process guideline  
> **Framework:** Vibe Coding  
> **Guideline baseline:** 1.0.0  
> **Status:** Template; project-specific content requires review  

## Purpose

Governance for code-agent plugins and extensions.

## Agent read trigger

**MUST** read or consult this file: Before install, enablement or upgrade.

## Normative sections and rules

### 1. Inventory

- **MUST** — Capture plugin, publisher, purpose, version, platform and owner.

### 2. Approval

- **MUST** — Assess permissions, security posture, privacy impact, licenses and cost.

### 3. Boundaries

- **MUST** — Limit project and data scope to need-to-know; disable unused plugins.

### 4. Updates

- **MUST** — Review version changes, compatibility and revocation procedure.

### 5. Monitoring

- **SHOULD** — Audit plugin behavior and failures when supported.

### 6. Optionality

- **MAY** — Use project-specific productivity extensions after approval.

## Evidence and change control

- **MUST** record owner, revision/date, relevant approval reference, and traceable evidence in the applicable project instantiation.
- **MUST** route changes to process rules through `docs/guideline-CHANGELOG.md` and formal baseline revision; route feature behavior through approved versioned specs and `docs/CHANGELOG.md`.
- **SHOULD** keep links to canonical artifacts instead of duplicating definitions.

## Vibe Coding interpretation

- **MAY** use provisional decisions in an isolated prototype, clearly marked `DRAFT`; **MUST** formalize and approve production-bound behavior before shipping.
