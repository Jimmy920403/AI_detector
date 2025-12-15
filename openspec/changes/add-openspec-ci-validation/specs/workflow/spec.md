## ADDED Requirements
### Requirement: OpenSpec CI Validation
The project MUST validate OpenSpec proposals and specs in Continuous Integration using strict mode to prevent invalid changes from merging.

#### Scenario: Validate on pull requests
- **WHEN** a pull request is opened or updated
- **THEN** `openspec validate --strict` runs and MUST pass for merge eligibility

#### Scenario: Validate on default branch pushes
- **WHEN** commits are pushed to the default branch
- **THEN** `openspec validate --strict` runs to ensure specs and archived changes remain valid