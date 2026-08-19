<!-- markdownlint-disable -->

# Hardening Report: yoshi389111--github-profile-3d-contrib/v0.9.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **yoshi389111--github-profile-3d-contrib/v0.9.1** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Workflow files reference GitHub Actions using mutable version tags (@v5) instead of immutable full 40-character SHA commit hashes. This exposes the workflow to supply-chain attacks if the tag is moved to a malicious commit. Affected references: actions/checkout@v5 and actions/setup-node@v5 in build.yml; actions/checkout@v5 in latest-branch.yml.

Locations:

- `.github/workflows/build.yml:10`
- `.github/workflows/build.yml:11`
- `.github/workflows/latest-branch.yml:8`

### script-injection (severity: high)

Sub-rule (a): A GitHub Actions expression is interpolated directly inside a run: shell command. In latest-branch.yml, the run: block contains: `git branch -f latest ${{ github.event.release.tag_name }}`. The value of github.event.release.tag_name flows through YAML template substitution before the shell parses it, so a tag name containing shell metacharacters (e.g. semicolons, backticks, $(...)) could result in arbitrary command execution.

Locations:

- `.github/workflows/latest-branch.yml:12`

### missing-permissions (severity: medium)

Neither workflow file defines a top-level permissions: key, and no job in either file defines a job-level permissions: key. Without explicit permissions, workflows inherit the default repository permissions (which may be write-all), granting broader access than necessary. Both build.yml and latest-branch.yml are affected.

Locations:

- `.github/workflows/build.yml:1`
- `.github/workflows/latest-branch.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, missing-permissions

**Notes:**

Fixed all three findings across build.yml and latest-branch.yml:
1. unpinned-uses: Pinned actions/checkout@v5 → @fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09 and actions/setup-node@v5 → @a0853c24544627f65ddf259abe73b1d18a591444, preserving the tag in a comment.
2. script-injection: In latest-branch.yml, moved `${{ github.event.release.tag_name }}` out of the run: shell string into an env: block as TAG_NAME, then referenced it as "$TAG_NAME" in the shell script.
3. missing-permissions: Added `permissions: contents: write` at the top level of both workflow files. contents: write is the minimum required since both workflows push commits/branches to the repository.

