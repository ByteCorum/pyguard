# Contributing

Thank you for considering a contribution. This document describes how to propose changes, and what is expected of them.

By participating in this project, you agree to abide by the [Code of Conduct](./CODE_OF_CONDUCT.md).

## Getting Help First

Before opening an issue or PR, check the right channel
In particular:

- Usage questions go to [Discussions](https://github.com/ByteCorum/pyguard/discussions/new?category=q-a), not the issue tracker
- Security vulnerabilities go to , never to a public issue. [Report a vulnerability](https://github.com/ByteCorum/pyguard/security/advisories/new)
- Bugs and features go through the [issue templates](https://github.com/ByteCorum/pyguard/issues/new/choose)
- More extensive guide how to get help and support described in [SUPPORT.md](./SUPPORT.md)

## Environment Setup

TODO

<!-- Describe here how to build and run the project locally.
     Required content:

     1. Prerequisites: language version, package manager, tools
     2. Clone and dependency installation commands
     3. Build command
     4. Test command
     5. Lint / format command
-->

## Making Changes

1. Fork the repository and create a branch from `stable`. Branch naming: `feat/<short-name>`, `fix/<short-name>`, `docs/<short-name>`, `chore/<short-name>`.
2. Make your change. One logical change per pull request, split unrelated changes into separate PRs.
3. Make separate commits for logically separate changes; do not mix formatting-only changes with logic changes in one commit.
4. Ensure the linter and formatter pass, and all tests pass locally.
5. Squash or rebase your branch so each commit is meaningful; PRs with a clean history are merged as-is.
6. Open a pull request following the [pull request template](../.github/PULL_REQUEST_TEMPLATE.md).

## Commit Style

This project follows the [Conventional Commits](https://www.conventionalcommits.org/)

specification:

```
<type>(<optional scope>): <description>

<optional body>

<optional footer>
```

Rules:

- Subject line: imperative, present tense ("add", not "added"), no trailing period, no more than 72 characters
- Body (if any): wrapped at 100 characters, explains what and why
- Footer: reference issues (`Closes #123`) and breaking changes (`BREAKING CHANGE: <description>`)

Types:

| Type     | Purpose                                           | SemVer effect |
| -------- | ------------------------------------------------- | ------------- |
| feat     | New feature for the user                          | MINOR         |
| fix      | Bug fix for the user                              | PATCH         |
| docs     | Documentation only                                | none          |
| style    | Formatting, whitespace; no logic change           | none          |
| refactor | Code change that neither fixes nor adds a feature | none          |
| perf     | Performance improvement                           | PATCH         |
| test     | Adding or correcting tests                        | none          |
| build    | Build system or dependencies                      | none          |
| ci       | CI configuration and workflows                    | none          |
| chore    | Maintenance; anything not covered above           | none          |
| revert   | Revert a previous commit                          | as target     |

`feat` and `fix` with a `!` (or a `BREAKING CHANGE:` footer) produce a MAJOR release.

Examples:

```
feat(auth): add token refresh on session resume
fix(api): prevent duplicate submissions on double click
docs: correct branch name in CONTRIBUTING
refactor(core)!: change public signature of parseInput

BREAKING CHANGE: parseInput no longer accepts raw strings
```

## Labels

Labels are defined in [labels.yml](../.github/labels.yml) and applied automatically by issue forms. A label policy workflow enforces the structure.

The axes:

- **Type:** what kind of work: `type: bug`, `type: enhancement`, `type: documentation`, `type: maintenance` (one per item)
- **Status:** pipeline state: `status: needs-triage`, `status: in-progress`, `status: blocked`, `status: needs-info`, `status: suspended`, `status: done` (one per item; applied by maintainers, not contributors)
- **Priority:** `priority: 0` (highest, work immediately) through `priority: 3` (low; when time permits). One per item.
- **Size** `size: S` / `size: M` / `size: L` / `size: XL`. One per item. These match the TODO.md tags (`S:<s|m|l|xl>`, lowercase there, uppercase in labels).

Additional markers: `security`, `breaking-change`, `invalid`, `duplicate`, `wontfix`.

## AI-Generated Changes

**Any change generated with the assistance of AI tools: code, tests,
documentation, or commit messages must be explicitly flagged.**

- State it in the pull request description ("This change was AI-assisted") and describe which parts
- Apply the `ai-marked` label to the pull request
- You remain fully responsible for AI-assisted contributions: review every line, verify correctness, and ensure you can explain the change without the tool
- Unflagged AI-generated contributions discovered later may be reverted without notice
- This policy exists for accountability: the human who submits a change owns it, regardless of how it was produced

## Style and Formatting

Formatting and style are enforced by [.editorconfig](../.editorconfig) and [.yamllint](../.yamllint) (for workflow files). Configure your editor to respect `editorconfig`.

## Review Process

- Pull requests are reviewed by the code owners defined in [.github/CODEOWNERS](../.github/CODEOWNERS)
- Reviews happen as availability permits, please be patient
- If a review requests changes, push fixes as separate commits; do not force-push over reviewed commits unless asked
- Pull requests introducing breaking changes should carry the `breaking-change` label
- Squash merges use the PR title as the commit message, so the PR title must follow the commit style above (`feat: ...`, `fix: ...`)

## Licensing

By contributing, you agree your contributions are licensed under the project's [LICENSE](../LICENSE).
