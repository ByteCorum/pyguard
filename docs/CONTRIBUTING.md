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

1. Fork the repository and create a branch from `stable`.
2. Branch naming and commit style must match the requirements described below in **Commit Style** and **Branch Naming** sections.
3. Make your change. One logical change per pull request, split unrelated changes into separate PRs.
4. Within a PR, make separate commits for logically distinct steps; each commit should leave the code in a working state.
5. Ensure the linter and formatter pass, and all tests pass locally.
6. Keep your history clean: if every commit is meaningful, the PR is merged as a merge commit; otherwise it will be squashed. Rebase is used only for small changes.
7. Open a pull request following the [pull request template](../.github/PULL_REQUEST_TEMPLATE.md).

## Commit Style

This project follows the [Conventional Commits](https://www.conventionalcommits.org/)

Specification:

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

| Type     | Purpose                                           | SemVer effect               |
| -------- | ------------------------------------------------- | --------------------------- |
| feat     | New feature for the user                          | MINOR                       |
| fix      | Bug fix for the user                              | PATCH                       |
| docs     | Documentation only                                | none                        |
| style    | Formatting, whitespace; no logic change           | none                        |
| refactor | Code change that neither fixes nor adds a feature | none                        |
| perf     | Performance improvement                           | PATCH                       |
| test     | Adding or correcting tests                        | none                        |
| build    | Build system or dependencies                      | none                        |
| ci       | CI configuration and workflows                    | none                        |
| chore    | Maintenance; anything not covered above           | none                        |
| revert   | Revert a previous commit                          | same as the reverted commit |

`feat` and `fix` with a `!` (or a `BREAKING CHANGE:` footer) indicate a MAJOR release.

Examples:

```
feat(auth): add token refresh on session resume
fix(api): prevent duplicate submissions on double click
docs: correct branch name in CONTRIBUTING
refactor(core)!: change public signature of parseInput

BREAKING CHANGE: parseInput no longer accepts raw strings
```

## Branch Naming

Branch naming rules follow the commit styling rules.

- Branch names should follow this pattern: `<type>(<optional scope>)/<short-description>`
- Imperative, present tense ("add", not "added"), no trailing period, no more than 45 characters
- If this branch relates to an issue, reference it (`#123`)
- If this branch introduces breaking changes, mark them in the commit messages and PR description (`!` or `BREAKING CHANGE` right after **Description** header); the branch name itself does not carry the marker.

Permitted types are listed in the **Types** table in the **Commit Style** section.

Examples:

```
feat(auth)/token-refresh
fix(api)/doubleclick-duplicate-submissions
docs(readme)/fix-typo
refactor(core)/public-signature-parseInput
```

## Labels

Labels are defined in [labels.yml](../.github/labels.yml) and applied automatically by issue forms. A label policy workflow enforces the structure.

The axes:

- **Type:** what kind of work: `type: bug`, `type: enhancement`, `type: documentation`, `type: maintenance` (one per item), `type: other` can be assigned additionally if change is not covered by any existing type
- **Status:** pipeline state: `status: needs-triage`, `status: in-progress`, `status: blocked`, `status: needs-info`, `status: suspended`, `status: done` (one per item; applied by maintainers, not contributors)
- **Priority:** `priority: 0` (highest, work immediately) through `priority: 3` (low; when time permits). One per item.
- **Size** `size: S` / `size: M` / `size: L` / `size: XL`. One per item. These match the TODO.md tags (`S:<s|m|l|xl>`, lowercase there, uppercase in labels).

Additional markers: `security`, `breaking-change`, `invalid`, `duplicate`, `wontfix`, `revert`.

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
