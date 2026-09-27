# TODO

Planned work and known issues for this project.
Completed items are removed from this file; completed work belongs in the Changelog, not here.

Entry format: `[ ] <NAME> | P:<0-3> | S:<s|m|l|xl> | <COMMENT>`. Priority 0 is highest; size is effort estimate (s < 1h, m = half a day, l = multi-day, xl = week+).
Link the matching issue when one exists: `[ ] #42 ...`

## Planned

- [ ] Publish as python lib | P:1 | S:m
- [ ] Global vars should be defined globally, not in every command | P:3 | S:l | Not affect functionality, only code quality
- [x] Add exception handling in places of loud fail instead of default python error | P:0 | S:m
- [ ] Resolve issue with pointless check and param in `LegacyObfuscation.GenSeperator()` | P:3 | S:s
- [ ] Add separator encoding with b64encode for `LegacyObfuscation.MediumObfuscation()` and `LegacyObfuscation.PowerObfuscateion()` | P:2 | S:m

## Feature Ideas

- [ ] Add precompilation of cmds dir | P:3 | S:l | suspended

## Known Issues

- [x] Obfuscation of files from different projects is not supported; use 1 command per project | P:- | S:- | wontfix: by design, the common-root guard rejects unrelated trees to prevent misplaced output and broken dependencies
