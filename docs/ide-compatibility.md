# IDE Compatibility & Agent Configuration Standard

**Document ID:** GL-IDE-001  
**Version:** 1.0.0  
**Status:** Proposed Guideline Baseline  
**Applies to:** Vibe Coding and Spec-Driven Development (SDD)  
**Category:** Guidelines — Process Layer  
**Owner:** Project Owner / Engineering Lead  
**Last Updated:** 2026-11-04

---

## 1. Purpose

Establish a standard procedure for configuring, switching, and operating AI-assisted development environments without damaging project structure, duplicating engineering policies, or causing inconsistent agent behavior.

This policy supports Claude Code, Cursor, Windsurf, VS Code/GitHub Copilot, Codex, OpenCode, Antigravity, Trae, and compatible future platforms.

### 1.1 Mandatory principles

- **MUST** preserve the canonical project guidelines and approved specifications.
- **MUST** maintain compatibility with multiple coding agents where technically feasible.
- **MUST** execute IDE detection and pruning: In Single-IDE mode, automatically prune irrelevant IDE configuration files before first execution to avoid conflicts; in Multi-IDE mode, synchronize and preserve all declared active IDE adapters.
- **MUST NOT** overwrite existing agent configurations without explicit authorization.
- **MUST** separate universal engineering instructions from tool-specific configuration.
- **MUST** verify that the selected tool actually recognizes and loads the intended instructions.
- **SHOULD** minimize duplicated instructions and unnecessary context consumption.
- **MAY** enable additional platform capabilities when supported and approved.

## 2. Policy authority and document precedence

The following documents govern agent behavior:

1. `docs/constitution.md` — Engineering principles.
2. `docs/rules.md` — Enforceable development baseline.
3. `docs/ide-compatibility.md` — IDE configuration and compatibility rules.
4. `docs/spec.md` (SDD) or the approved project requirements (Vibe Coding).
5. Applicable feature specifications and approved technical contracts.
6. `AGENTS.md` — Portable agent instruction entry point.
7. Tool-specific instruction files — Platform adapters.
8. `docs/memory.md` — Verified project working context.

**MUST:** Approved guidelines control development procedures, while the latest approved feature specification controls feature behavior.

**MUST:** IDE-specific instruction files must not introduce conflicting independent engineering policies.

**MUST:** When conflicts occur, stop the affected work, record the conflict, and request an authoritative resolution.

This precedence describes project governance. It does not override higher-priority instructions or security policies enforced by the IDE or agent platform.

## 3. Supported IDEs and instruction files

| IDE / Agent | Primary configuration | Additional configuration |
|---|---|---|
| Claude Code | `CLAUDE.md` | `.claude/rules/`, `.claude/skills/`, settings and hooks |
| Cursor | `.cursor/rules/`, `AGENTS.md` | Legacy `.cursorrules`, compatible `CLAUDE.md` |
| Windsurf | `.windsurf/rules/` | `AGENTS.md`, supported workflows, legacy `.windsurfrules` |
| VS Code / GitHub Copilot | `.github/copilot-instructions.md`, `AGENTS.md` | `.github/instructions/` |
| OpenAI Codex | `AGENTS.md` | Nested `AGENTS.md`, supported Codex configuration |
| OpenCode | `AGENTS.md` and supported native configuration | Skills, commands, permissions and integrations |
| Antigravity | Version-supported project rules | Supported workflows and tool configuration |
| Trae | Version-supported project or agent rules | Supported custom agents and tool configuration |
| Other tools | `AGENTS.md` where supported | Verified native adapters |

**MUST:** Verify paths, file formats, discovery behavior, and available features against the installed tool version.

**MUST NOT:** Assume an IDE loads an instruction file solely because the file exists in the repository.

**SHOULD:** Use modern, actively supported configuration formats instead of legacy formats.

**MAY:** Retain legacy instruction files for backward compatibility.

## 4. Canonical file structure

```text
Project-Codebase/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── .cursorrules
├── .windsurfrules
│
├── docs/
│   ├── constitution.md
│   ├── rules.md
│   ├── ide-compatibility.md
│   ├── agents.md
│   ├── skills.md
│   ├── hooks.md
│   ├── plugins.md
│   ├── connectors.md
│   ├── memory.md
│   └── ...
│
├── .claude/
│   ├── rules/
│   ├── skills/
│   └── ...
│
├── .cursor/
│   └── rules/
│
├── .windsurf/
│   └── rules/
│
├── .github/
│   ├── copilot-instructions.md
│   └── instructions/
│
├── .agents/
│   ├── skills/
│   ├── commands/
│   ├── hooks/
│   └── templates/
│
└── playbooks/
```

**MUST:** Preserve the existing repository structure.

**MUST:** Use `docs/` for canonical project documentation in both frameworks.

**MUST NOT:** Introduce a `specs/` directory in the SDD framework.

**SHOULD:** Keep portable agent definitions in `.agents/` and maintain native adapters only where required.

**MAY:** Omit platform-specific folders when the corresponding tools are not configured.

## 5. IDE detection, Automated Pruning & Multi-IDE Coexistence

### 5.1 Operating Modes: Single-IDE vs. Multi-IDE

To prevent rule shadowing, context bloat, and conflicting instructions, this standard defines two operating modes:

#### Mode A: Single-IDE Targeted Mode (Auto-Pruning Enabled — Default)
When a single active IDE or coding agent is identified or chosen by the developer:
1. **MUST** retain the active IDE's adapter file/directory and canonical `AGENTS.md`.
2. **MUST** automatically remove irrelevant configuration directories and files belonging to other IDEs prior to or during Prompt 1 execution.
3. **MUST NOT** leave stale or inactive IDE configuration files that pollute token context or confuse AI agents.

**Single-IDE Pruning Matrix:**
| Active IDE / Agent | Retained Configuration | Pruned Irrelevant Configurations |
|---|---|---|
| **Antigravity** | `AGENTS.md`, `.agents/` | `.cursor/`, `.cursorrules`, `.windsurf/`, `.windsurfrules`, `.claude/`, `CLAUDE.md` |
| **OpenCode** | `AGENTS.md`, `.agents/` | `.cursor/`, `.cursorrules`, `.windsurf/`, `.windsurfrules`, `.claude/`, `CLAUDE.md` |
| **Cursor** | `.cursor/`, `.cursorrules`, `AGENTS.md` | `.windsurf/`, `.windsurfrules`, `.claude/`, `CLAUDE.md` |
| **Windsurf** | `.windsurf/`, `.windsurfrules`, `AGENTS.md` | `.cursor/`, `.cursorrules`, `.claude/`, `CLAUDE.md` |
| **Claude Code** | `CLAUDE.md`, `.claude/`, `AGENTS.md` | `.cursor/`, `.cursorrules`, `.windsurf/`, `.windsurfrules` |
| **Codex / Freebuff / Trae** | Platform adapter, `AGENTS.md` | Other inactive IDE directories |
| **VS Code (Standard)** | `.github/copilot-instructions.md` | `.cursor/`, `.windsurf/`, `.claude/` proprietary agent folders |

#### Mode B: Multi-IDE / Multi-Agent Coexistence Mode
When a developer or team deliberately uses **more than one IDE simultaneously** (e.g., *Antigravity + Cursor*, *Cursor + Claude Code*, or *VS Code + Windsurf*):
1. **User Declaration:** The user specifies multiple active IDEs during Step 2 / Prompt 1 (e.g. `ACTIVE_IDES=["antigravity", "cursor", "claude-code"]`).
2. **Harmonized Coexistence:** The configuration files for ALL selected active IDEs are preserved.
3. **Single Source of Truth:** Each active adapter MUST point directly to canonical `AGENTS.md`, `docs/`, and `.agents/`, guaranteeing zero policy drift across IDEs.
4. **Selective Pruning:** Only configuration files for IDEs *outside* the declared active set are pruned.
5. **Cross-IDE Session Discipline:** Agents must not clobber other IDEs' internal working directories.

### 5.2 Automated IDE Pruning Script

Developers can execute this cleanup script (or instruct the agent to run it during Step 2 / Prompt 1):

```powershell
# PowerShell: Prune Irrelevant IDE Configurations
param(
    [string[]]$ActiveIDEs = @("antigravity") # e.g. @("antigravity") or @("cursor", "claude")
)

$AllTargets = @{
    "cursor"    = @(".cursor", ".cursorrules")
    "windsurf"  = @(".windsurf", ".windsurfrules")
    "claude"    = @(".claude", "CLAUDE.md")
}

foreach ($ide in $AllTargets.Keys) {
    if ($ActiveIDEs -notcontains $ide) {
        foreach ($path in $AllTargets[$ide]) {
            if (Test-Path $path) {
                Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
                Write-Host "Pruned inactive IDE config: $path"
            }
        }
    }
}
Write-Host "Active IDE configuration verified: $($ActiveIDEs -join ', ')"
```

### 5.3 Detection Procedure
At session initialization or when changing the active coding tool:
1. **MUST** identify the active agent runtime or IDE using environment variables or prompt declaration.
2. **MUST** verify whether single-IDE pruning or multi-IDE coexistence is selected.
3. **MUST** prune inactive configuration files in Single-IDE mode or synchronize adapters in Multi-IDE mode.
4. **MUST** verify that `.agents/` custom commands (`*-ca-agent.md`) and skills (including `andrej-karpathy-skill`) are active and accessible.
5. **MUST** verify that `specs/` (in SDD) is recognized and user's format preference is recorded.

## 6. Configuration activation

### 6.1 Universal instructions

Every supported agent **MUST** follow:

- Project governance and safety rules.
- Latest approved specifications.
- Coding standards and architecture constraints.
- Test-driven development requirements.
- Security and privacy requirements.
- Version control procedures.
- Quality gates and completion criteria.
- Agent permission and escalation rules.

### 6.2 IDE-specific instructions

The active IDE **SHOULD** receive a short adapter containing:

1. Reference to canonical project guidelines.
2. Reference to approved specifications.
3. Relevant tool-specific instruction syntax.
4. Approved build and test commands.
5. Supported skill and hook locations.
6. Permissions and approval requirements.
7. Verification procedure.

**MUST NOT:** Duplicate the complete guideline collection across several instruction files.

**MUST:** Avoid contradictory instructions when an IDE loads multiple files simultaneously.

**SHOULD:** Use links or native import mechanisms when supported.

## 7. Switching between IDEs

### 7.1 Safe switching procedure

When changing from IDE A to IDE B:

1. **MUST** preserve existing source files and documentation.
2. **MUST** preserve IDE A's configuration.
3. **MUST** identify IDE B and supported configuration formats.
4. **MUST** inspect IDE B's existing instruction files.
5. **MUST** load the current guideline and approved-spec references.
6. **MUST** reconcile conflicts between active instruction sources.
7. **MUST** check skill, hook, and connector compatibility.
8. **MUST** verify permissions before enabling tools.
9. **MUST** validate instruction loading.
10. **MUST** report configuration status and unresolved incompatibilities.

### 7.2 Non-destructive switching

Switching IDEs **MUST NOT** automatically:

- Delete `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, or `.windsurfrules`.
- Delete `.claude/`, `.cursor/`, `.windsurf/`, or other platform directories.
- Modify the approved technology stack.
- Rewrite specifications.
- Change coding standards.
- Modify the Git history.
- Install plugins or MCP servers.
- Grant additional permissions.
- Change secrets or credentials.
- Disable quality gates.
- Remove tests or CI workflows.

Any such action requires an explicit authorized change.

## 8. Skills compatibility

### 8.1 Skill registry

`docs/skills.md` **MUST** define:

- Skill name and identifier.
- Purpose and ownership.
- Required inputs.
- Trigger conditions.
- Required documentation.
- Expected outputs.
- Permitted tools.
- Security permissions.
- Verification method.
- Supported IDEs.
- Version and maintenance status.

### 8.2 Activation procedure

Before activating a skill, the agent:

1. **MUST** check relevance to the current task.
2. **MUST** verify that the IDE supports the required skill mechanism.
3. **MUST** confirm that the skill is trusted and approved.
4. **MUST** inspect dependencies and permissions.
5. **MUST** avoid conflicting duplicate skills.
6. **MUST** validate expected execution behavior.
7. **SHOULD** prefer reusable portable skill definitions.
8. **MAY** create a tool-native adapter after approval.

**MUST NOT:** Treat a portable skill template as installed or executable unless the active tool can invoke it successfully.

## 9. Hooks compatibility

### 9.1 Hook categories

Relevant hooks may include:

- Session initialization.
- Before tool execution.
- Before file modification.
- After file modification.
- Before commit.
- Before pull request.
- Before deployment.
- After deployment.

### 9.2 Rules

- **MUST** verify supported trigger events before enabling hooks.
- **MUST** document input, output, side effects, permissions, and failure behavior.
- **MUST** prevent unauthorized destructive operations.
- **MUST** define timeout, retry, and logging behavior.
- **MUST** test hooks before relying on them.
- **MUST** retain CI-level enforcement for mandatory quality gates.
- **SHOULD** use portable scripts when possible.
- **MAY** implement equivalent hooks differently in different IDEs.

**MUST NOT:** Assume that all IDEs provide equivalent hook mechanisms.

## 10. Plugins and MCP server compatibility

### 10.1 Plugin and connector activation

Before enabling a plugin, MCP server, or connector:

1. **MUST** establish the business purpose.
2. **MUST** verify source and publisher trust.
3. **MUST** inspect required permissions.
4. **MUST** classify accessible data.
5. **MUST** separate development and production credentials.
6. **MUST** obtain authorization before installation or configuration changes.
7. **MUST** test connection and failure behavior.
8. **MUST** record configuration in the appropriate registry.
9. **SHOULD** begin with read-only access where feasible.
10. **MUST** request separate approval for destructive or externally visible operations.

### 10.2 Platform isolation

- **MUST NOT** assume MCP configuration from one IDE is automatically portable to another.
- **MUST NOT** copy secrets between IDEs without approval and secure handling.
- **MUST NOT** enable all available connectors by default.
- **MUST** distinguish configured, available, authorized, connected, and operational states.
- **MAY** reuse approved server definitions when compatible.

## 11. Slash commands and custom workflows

Supported portable commands include:

- `/plan`
- `/task`
- `/implement`
- `/verify`
- `/run`
- `/testing`
- `/review`
- `/errorlogs`
- `/gitlogs`
- `/change-request`
- `/spec-check`
- `/tdd`
- `/security-audit`
- `/release-check`
- `/handoff`

**MUST:** Maintain canonical command contracts in `.agents/commands/`.

**MUST:** Verify that a command is supported and registered in the active IDE before invoking it.

**MUST NOT:** Assume a slash command is available merely because its Markdown definition exists.

**MUST:** Require approval before implementation, destructive operations, or deployment where defined by project policy.

**SHOULD:** Provide equivalent documented manual workflows when a command cannot be registered.

**MAY:** Adapt command names and syntax for platform compatibility.

## 12. SDD-specific requirements

When using the Spec-Driven Development framework:

- **MUST** read the latest approved feature specification before implementation.
- **MUST** verify its version and approval status.
- **MUST** follow the mandatory change-request workflow.
- **MUST** write or update tests before implementation.
- **MUST** restrict implementation to approved scope.
- **MUST** preserve requirement-to-test traceability.
- **MUST** pass all required quality gates.
- **MUST NOT** allow IDE switching to bypass specification approval.
- **MUST NOT** implement feature changes from chat context alone when the approved specification has not been updated.
- **MUST** escalate conflicts requiring guideline revision.

These controls apply identically regardless of which coding agent is used.

## 13. Vibe Coding-specific requirements

When using the Vibe Coding framework:

- **MUST** distinguish disposable prototypes from production-bound work.
- **MUST** maintain an explicit project plan and prototype scope.
- **MUST** record material design and functionality decisions.
- **SHOULD** support rapid experimentation within approved boundaries.
- **MUST** preserve security and data-handling requirements during experimentation.
- **MUST** formalize selected behavior into approved requirements before production promotion.
- **MUST** pass production quality gates before release.
- **MUST NOT** treat IDE-generated functionality as automatically approved.

## 14. Context and memory synchronization

When switching agents or starting a new session:

1. **MUST** read the applicable guideline baseline.
2. **MUST** inspect the current specification and task state.
3. **MUST** inspect repository status and relevant code.
4. **MUST** distinguish verified project facts from stale memory.
5. **MUST** identify completed, pending, and blocked work.
6. **MUST** preserve documented decisions and unresolved issues.
7. **SHOULD** refresh `docs/memory.md` after meaningful milestones.
8. **MUST NOT** overwrite verified project state with unsupported agent assumptions.

`docs/memory.md` is an operational summary, not an independent source of feature requirements.

## 15. Conflict detection and resolution

### 15.1 Conflict categories

Potential conflicts include:

- Different coding conventions.
- Different framework instructions.
- Different test commands.
- Contradictory agent permissions.
- Conflicting architectural guidance.
- Duplicate skills or hooks.
- Incompatible plugin or MCP configurations.
- Outdated references to approved specifications.
- Conflicting local and repository-level instructions.

### 15.2 Resolution process

1. **MUST** identify all relevant conflicting instructions.
2. **MUST** determine their source and effective scope.
3. **MUST** check the authoritative guideline baseline.
4. **MUST** check platform-enforced policies and permissions.
5. **MUST** stop conflicting actions until resolved.
6. **MUST** request approval for any policy or configuration revision.
7. **MUST** record approved changes.
8. **MUST** verify that the conflict no longer affects execution.

**MUST NOT:** Resolve conflicts by silently deleting files or disabling controls.

## 16. Security and permission controls

- **MUST** apply least privilege to agent tools.
- **MUST** protect environment variables, secrets, tokens, and credentials.
- **MUST NOT** store secrets in agent instruction files or project memory.
- **MUST** request authorization for production access.
- **MUST** require approval for destructive commands.
- **MUST** protect against prompt injection through retrieved content, repositories, logs, and tool responses.
- **MUST** enforce repository permissions and server-side CI protections.
- **MUST** document externally connected tools and data access.
- **SHOULD** use sandboxed environments for experiments.
- **MAY** enable unattended execution only within explicit, bounded permissions.

## 17. Configuration verification checklist

The following checks **MUST** be performed when initially configuring a supported IDE or changing relevant configuration.

- [ ] Active IDE/agent identified.
- [ ] Tool version and instruction support verified.
- [ ] Canonical guideline version confirmed.
- [ ] Approved feature-spec version confirmed where applicable.
- [ ] `AGENTS.md` located and checked.
- [ ] Native instruction files inspected.
- [ ] Actual instruction loading verified.
- [ ] Conflicting rules resolved.
- [ ] Applicable skills identified.
- [ ] Required hooks validated.
- [ ] Plugin and MCP permissions reviewed.
- [ ] Approved commands available or mapped to manual procedures.
- [ ] Secrets and credentials protected.
- [ ] Existing files preserved.
- [ ] Build and test commands identified.
- [ ] SDD quality gates remain enforced where applicable.
- [ ] Configuration changes documented.
- [ ] Unresolved issues reported.

Checklist status must be supported by observable evidence rather than assumptions.

## 18. Required compatibility report

After setup or IDE switching, the agent **MUST** produce a concise report containing:

```text
IDE COMPATIBILITY REPORT

Project:
Development Mode: Vibe / SDD
Active IDE:
Agent Runtime:
Detected Version:
Guideline Version:
Approved Spec Version:

Canonical Instructions:
Native Instructions:
Instruction Loading Verified: Yes / No / Unknown

Skills:
Hooks:
Commands:
MCP Servers:
Plugins:

Conflicts:
Missing Capabilities:
Security Concerns:
Files Created:
Files Modified:
Files Deleted:
Tests Performed:
Verification Results:

Approval Required:
Final Status: Ready / Limited / Blocked
```

**MUST:** Report unknown values as unknown.

**MUST NOT:** Claim compatibility or successful activation without evidence.

## 19. Configuration change policy

This document belongs to the controlled Guidelines layer.

Any change to its mandatory rules:

1. **MUST** have an explicit revision request.
2. **MUST** identify the reason and expected benefits.
3. **MUST** assess compatibility and security impact.
4. **MUST** receive authorized approval.
5. **MUST** update the document version and revision date.
6. **MUST** update `docs/guideline-CHANGELOG.md`.
7. **MUST** verify affected IDE configurations.

Feature changes must follow the separate approved specification-change procedure.

## 20. Definition of Done

An IDE configuration is considered ready only when:

- The active agent platform has been identified.
- Required project instructions are confirmed as loaded or explicitly attached.
- Canonical guidelines remain authoritative.
- Approved specifications remain authoritative for feature behavior.
- Necessary commands, skills, hooks, and connectors have been verified.
- Permissions have been reviewed.
- No unresolved blocking conflicts remain.
- Existing configuration files have been preserved.
- The compatibility report has been completed.

If any mandatory check fails, configuration status **MUST** be reported as `Limited` or `Blocked`, not `Ready`.

---

## Final governing rule

**Switching AI coding IDEs must change only the necessary tool-specific configuration and active capabilities. It must never silently change project requirements, engineering standards, approval policies, source code, tests, or repository structure.**

All agents must follow the same approved project intent regardless of the IDE used.

---

**End of Document — GL-IDE-001 v1.0.0**