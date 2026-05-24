# Branch Protection Rules Justification

## Why We Protect the `main` Branch

These rules are industry standards that ensure code quality and team collaboration:

### 1. Require Pull Request Reviews (at least 1)
- **Prevents direct errors**: No code reaches `main` without a second set of eyes.
- **Shares knowledge**: Team members learn from each other's code.
- **Catches bugs early**: Reviewers spot logical or style issues automated tests might miss.

### 2. Require Status Checks to Pass (CI Workflow)
- **Blocks broken code**: PRs cannot merge if any unit or integration test fails.
- **Ensures consistency**: Every commit on `main` is verified to work in a clean environment.
- **Protects the release artifact**: The code that gets packaged/deployed is always in a known good state.

### 3. Disable Direct Pushes
- **Enforces the review process**: All changes must flow through a PR.
- **Maintains a clean history**: `main` always represents a complete, verified feature or fix.
- **Prevents "silent" changes**: Every modification is documented in a PR and associated issues.

## How to Set Up (GitHub UI)
1. Repository → **Settings** → **Branches** → **Add branch protection rule**
2. Branch name pattern: `main`
3. Require a pull request before merging
   - Require approvals (1)
4. Require status checks to pass before merging
   - Require branches to be up to date
   - Search and select your CI workflow name (e.g., "CI / build-and-test")
5. Do not allow bypassing the above settings
6. Click **Create**
