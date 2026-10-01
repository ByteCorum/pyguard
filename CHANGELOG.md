# Changelog

This file contains all changes that were ever made to project

## v3.1.0.0 | 2026-10-01

### Added

#### General

- Added strict parameters type control to avoid unexpected runtime errors
- Added _Pyrefly_ strict code checks to ensure height code quality
- Added _Yamllint_ strict workflows checks to ensure height workflows quality
- Added comprehensive project documentation

#### General Commands

- Added streamed real time pip output to **dependencies** command

#### Legacy Obfuscation

- Added _Base64_ separator encoding to `MediumObfuscation` and `PowerObfuscateion` to blend separator better into encrypted code
- Added `--seplen` separator length option, to allow custom separators

#### Main Obfuscation

- Added advanced environment checks to detect execution in hostile environment
- Added `--decoy` decoy code entry to execute if environment checks fail, to prevent attacker from knowing whether he was detected
- Added `--debug` and `--debug-error` to make it easier to find bugs in executor

#### Tests

- Added _complex_ test case to ensure stability with complex codebases
- Added _local tests_ to allow contributors to test their changes without pushing

### Changed

#### General

- Improved project structure for better orientation
- Rewrote readme to ensure clean and comprehensive project understanding
- Fixed argument type error when parsing incorrect argument
- Reworked project-wide exception handling to provide better errors
- Rewrote **logger** functionality to ensure correct handling of all possible cases
- Many small code quality and performance improvements
- Many bug fixes

#### General Commands

- Fixed inconsistency in **help** command handling
- Fixed **info** command output suppression if `--quiet` is on
- Fixed _pip_ ignoring global instructions in **dependencies**
- Rewrote help texts for better understanding

#### Legacy Obfuscation

- Reworked files and dirs path handling algorithm to ensure maximum robustness

#### Main Obfuscation

- Reworked files and dirs path handling algorithm to ensure maximum robustness
- Fixed save path calculation algorithm
- Replaced _AES-GCM_ with _AES-GCM-SIV_ and _ChaCha20_ with _XChaCha20-Poly1305_
- Rewrote executor to ensure maximum possible protection
- Reworked encryption and decryption logic for new algorithms to be as fast as possible
- Reworked file integrity checks to ensure maximum security and bypass protection
- Reworked string hashing because old one was poorly made
- Changed executor import logic
- Improved executor assembling to ensure maximum robustness

#### Tests

- Reworked github workflow test pipelines to cover more cases
- Reworked github workflow test pipelines to ensure robustness
- Reworked local test execution structure

### Removed

- Removed `--salsa` option from **main obfuscation**, because it's unauthenticated stream cipher
- Replaced _AES-GCM_ with _AES-GCM-SIV_ and _ChaCha20_ with _XChaCha20-Poly1305_

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
