## Why
Validation should be automatic in CI to prevent merging proposals or archives that fail strict checks. This reduces errors and enforces spec hygiene.

## What Changes
- Add a CI workflow to run `openspec validate --strict` for proposals and specs.
- Document usage in the project and reference the workflow.

## Impact
- Affected specs: workflow/tooling (new capability)
- Affected code: CI configuration files (e.g., `.github/workflows/openspec-validate.yml` or equivalent)