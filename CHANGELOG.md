# Changelog

## [0.2.7] - 2026-03-01

### Fixed
- Fixed a bug where concurrent `logging` module outputs and default `sys.stderr` printing would cause terminal visual artifacts or jam the loading animation spinner. 
- Implemented temporary StreamHandler hook and shared cursor tracking across system out streams for graceful handling of long, asynchronous log outputs seamlessly against the spinning animation.

## [0.2.6] - 2026-02-28

### Fixed
- Fixed an issue where the loading animation spinner could get stuck or corrupted when standard output (e.g. `print()`) contained newline characters.
- Improved terminal output safety and concurrent printing handling using threading locks and intelligent cursor position tracking. Multi-line logs printed inside decorated functions will now correctly interleave with the running animation spinner.

## [0.2.5]
- Previous releases.
