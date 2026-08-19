<!-- markdownlint-disable -->

# Hardening Report: yoshi389111--github-profile-3d-contrib/v0.9.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **yoshi389111--github-profile-3d-contrib/v0.9.2** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Both workflow files reference GitHub Actions using mutable tag refs (@v5) instead of pinned 40-character commit SHAs. This exposes the workflow to supply-chain attacks if the tag is moved to a different (potentially malicious) commit. Failing references: `actions/checkout@v5` and `actions/setup-node@v5` in build.yml; `actions/checkout@v5` in latest-branch.yml.

Locations:

- `.github/workflows/build.yml:11`
- `.github/workflows/build.yml:12`
- `.github/workflows/latest-branch.yml:11`

### script-injection (severity: high)

Sub-rule (a): The `run:` block in latest-branch.yml directly interpolates `${{ github.event.release.tag_name }}` into a shell command without any quoting or sanitization. An attacker who can create a release with a crafted tag name (e.g. containing shell metacharacters or newlines) could inject arbitrary shell commands. Offending line: `git branch -f latest ${{ github.event.release.tag_name }}`

Locations:

- `.github/workflows/latest-branch.yml:15`

### missing-permissions (severity: medium)

Neither `.github/workflows/build.yml` nor `.github/workflows/latest-branch.yml` declares a top-level `permissions:` key, and no job within either file declares job-level `permissions:`. Without explicit permissions, GitHub Actions defaults to the repository's default token permissions, which may be overly broad (e.g. `write` on all scopes for older repositories). Explicit minimal permissions should be declared for each workflow.

Locations:

- `.github/workflows/build.yml:1`
- `.github/workflows/latest-branch.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, missing-permissions

**Notes:**

Fixed all three findings across both workflow files:

1. **unpinned-uses** (build.yml lines 11-12, latest-branch.yml line 11): Pinned `actions/checkout@v5` → `@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09 # v5` and `actions/setup-node@v5` → `@a0853c24544627f65ddf259abe73b1d18a591444 # v5` using resolved commit SHAs.

2. **script-injection** (latest-branch.yml line 15): Moved `${{ github.event.release.tag_name }}` out of the `run:` shell string into a step-level `env:` block as `TAG_NAME`, then referenced it as `"$TAG_NAME"` in the shell script to prevent shell metacharacter injection.

3. **missing-permissions** (both files): Added `permissions: contents: write` at the top level of both workflows. `contents: write` is the minimum needed for `git push` in build.yml and force-pushing the `latest` branch in latest-branch.yml.

