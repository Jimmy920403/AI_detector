# Project Context

## Purpose
Provide a clear, spec-driven workflow for planning, validating, and implementing changes using OpenSpec. The project aims to keep requirements explicit, scenarios testable, and proposals reviewable before implementation.

## Tech Stack
- TypeScript for application logic
- Node.js (LTS) for backend tooling and scripts
- Optionally React for any UI components (if/when applicable)
- Jest for unit/integration testing
- ESLint + Prettier for code style and formatting
- Git + GitHub (or similar) for version control and PRs
- OpenSpec CLI for spec management, validation, and archiving

## Project Conventions

### Code Style
- Use ESLint (typescript-eslint) with Prettier integration
- 2-space indentation, semicolons, single quotes in TS
- Kebab-case for folders and change IDs; PascalCase for types/classes; camelCase for variables/functions
- Avoid one-letter variable names; prefer descriptive identifiers
- Keep functions small, pure where possible, and favor composition

### Architecture Patterns
- Prefer simple, single-responsibility modules
- Keep capabilities isolated; one capability per folder under `openspec/specs/`
- Introduce abstractions only when proven by repeated use
- Avoid framework lock-in unless justified by scale/performance

### Testing Strategy
- Write tests for acceptance scenarios from specs where applicable
- Unit tests for pure logic; integration tests for IO boundaries
- Keep test names descriptive and mirror spec scenarios
- Aim for fast, deterministic tests; avoid global state

### Git Workflow
- Use feature branches named `feature/<short-kebab-description>`
- Use Conventional Commits (e.g., `feat:`, `fix:`, `docs:`)
- Open PRs referencing relevant `openspec/changes/<id>`
- Require proposal approval before merge of implementation PRs

## Domain Context
This repository centers on OpenSpec-driven development. Capabilities are documented under `openspec/specs/`, while proposed changes live under `openspec/changes/` until approved and archived. Assistants should prioritize spec compliance and strict validation before coding.

## Important Constraints
- Keep changes small and reviewable (<100 lines preferred for initial implementations)
- Avoid breaking changes without an approved proposal
- Use `openspec validate --strict` to gate proposals and archives
- Prefer modifying existing specs over creating duplicates

## External Dependencies
- OpenSpec CLI (local environment)
- Git hosting provider (e.g., GitHub)
- CI system (e.g., GitHub Actions) for validation automation (planned)
