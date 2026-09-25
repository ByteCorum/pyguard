# Security Policy

## Security

We take the security of this project seriously. If you believe you have found a security vulnerability, please report it to us as described below. We appreciate your efforts to disclose it responsibly.

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.**

The preferred channel is private vulnerability reporting:

[Report a vulnerability](https://github.com/{VAR_USERNAME}/{VAR_REPO}/security/advisories/new)

This creates a private communication channel between you and the maintainers. Alternatively, contact owners with the details via {VAR_CONTACT_LINK}.

You should receive an acknowledgment within 72 hours. If you do not, please follow up to confirm we received the original report.

Please include as much of the following as possible:

- Type of issue (e.g., injection, authentication flaw, memory corruption)
- Full paths of source file(s) related to the manifestation
- The location of the affected code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it
- Any special configuration required to reproduce the issue

## Supported Versions

| Version    | Supported |
| ---------- | --------- |
| v3.0.0.0   | Yes       |
| < v3.0.0.0 | No        |

Only the latest major release receives security fixes.

## Disclosure Policy

<!-- >This project follows [coordinated disclosure](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/about-coordinated-disclosure-of-security-vulnerabilities):
reports are handled privately, and details are published only after a
fix is available, via a GitHub Security Advisory. -->

Reports are handled privately, and details are published only after a fix is available.
Please give us a reasonable amount of time to remediate before disclosing the issue publicly.

## Scope

The following are explicitly out of scope:

- Issues in dependencies, report those to the respective projects
- Automated scanner output without a demonstrated, reproducible impact
- Social engineering, denial of service, or physical attacks

## What Not to Do

- Do not open a public issue, including on other repositories, describing the vulnerability
- Do not disclose details publicly before a fix is released
- Do not test against deployments you do not own
