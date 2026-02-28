# Changelog

## [0.2.6] - 2026-02-28

### Fixed
- Fixed an issue where the loading animation spinner could get stuck or corrupted when standard output (e.g. `print()`) contained newline characters.
- Improved terminal output safety and concurrent printing handling using threading locks and intelligent cursor position tracking. Multi-line logs printed inside decorated functions will now correctly interleave with the running animation spinner.

## [0.2.5]
- Previous releases.
