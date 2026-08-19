<!-- markdownlint-disable -->

# Hardening Report: yoshi389111--github-profile-3d-contrib/0.9.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **yoshi389111--github-profile-3d-contrib/0.9.0** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Both workflow files reference GitHub Actions using mutable version tags (@v4) instead of pinned full 40-character commit SHAs. This exposes the workflow to supply-chain attacks if the tag is moved to a malicious commit. Failing references: `actions/checkout@v4` and `actions/setup-node@v4` in build.yml; `actions/checkout@v4` in latest-branch.yml.

Locations:

- `.github/workflows/build.yml:10`
- `.github/workflows/build.yml:11`
- `.github/workflows/latest-branch.yml:9`

### permissions (severity: medium)

Neither workflow file defines a `permissions:` block at the top level or at the job level. Without explicit permissions, the GITHUB_TOKEN is granted its default (potentially broad) permissions. Each workflow should declare minimal required permissions (e.g., `contents: write` only where needed).

Locations:

- `.github/workflows/build.yml:1`
- `.github/workflows/latest-branch.yml:1`

### script-injection (severity: high)

Sub-rule (a): The `run:` block in latest-branch.yml directly interpolates `${{ github.event.release.tag_name }}` into a shell command without any sanitization. An attacker who can create a release with a crafted tag name (e.g., containing shell metacharacters) could achieve arbitrary command execution on the runner. Offending line: `git branch -f latest ${{ github.event.release.tag_name }}`

Locations:

- `.github/workflows/latest-branch.yml:12`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, permissions, script-injection

**Notes:**

Fixed all three findings across both workflow files: (1) Pinned actions/checkout@v4 → @11d5960a326750d5838078e36cf38b85af677262 and actions/setup-node@v4 → @49933ea5288caeca8642d1e84afbd3f7d6820020 with # v4 comments for readability. (2) Added `permissions: contents: write` at the top level of both build.yml and latest-branch.yml — contents: write is the minimum needed since both workflows push commits/branches. (3) Fixed script injection in latest-branch.yml by moving `${{ github.event.release.tag_name }}` into a step env var (TAG_NAME) and referencing it as "$TAG_NAME" in the shell script, preventing shell metacharacter injection via crafted release tag names.

