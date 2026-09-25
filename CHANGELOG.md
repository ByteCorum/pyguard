# Changelog

This file contains all changes that were ever made to project

## v3.0.0.0 | 2025-07-30

### Rewrote all tool from scratch

### Added

- Spread support across all 3 major platforms(`Linux`, `Windows`, `Mac`), `BSD` should be also supported, but not tested
- Added new encryption algorithms: `Salsa20`, `ChaCha20-Poly1305`, `AES-GCM`
- Added more commands and abilities
- Added new tests

### Changed

- Rewrote obfuscation and protection mechanisms and algorithms
- Fixed plenty of bugs
- Fixed critical vulnerabilities
- Cleaned code

## v2.0.1.5 | 2024-08-05

### Added

- Added improved exceptions handling: Now all exceptions looks clearly and understandable.
- Added obfuscation checks: Now every commit should pass build checks + functional checks.
- Added obfuscation examples - see examples of obfuscation in `examples` dir.

### Changed

- Optimized ImportManager: Now it only includes needed libs.
- Fixed fatal error with hashing: Program was hashing important parts of code, breaking it

## v2.0.0.0 | 2024-08-04

**Initial GitHub Release**

## v1.0.0.0 | unknown

**Initial Release**
