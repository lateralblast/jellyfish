# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] - 2026-10-03
### Changed
- PEP 8 formatting: 4-space indentation, docstrings, module constants, `os.path.join`, `is not` / `not in` idioms
- Third-party modules are imported lazily where used; `--version`, `--options` and help no longer trigger module installation
- Shebang is now `python3`

### Removed
- Unused `bs4` / `beautifulsoup4` dependency
- Redundant stdlib entries from the README requirements list

## [0.1.9] - 2026-10-03
### Changed
- Option descriptions are now argparse `help=` strings, so `-h` shows them and `--options` reads them from the parser instead of parsing the script source

### Fixed
- Incorrect option descriptions for `--did`, `--hclurl` and `--release`

## [0.1.8] - 2026-10-03
### Changed
- Script flow moved into `main()` behind an `if __name__ == "__main__"` guard, with a `build_parser()` function and a proper exit status (1 when the JSON file is missing)
- `search_json` split into `search_string` and `search_keys`
- Help with no arguments uses `parser.print_help()` instead of re-running the script

## [0.1.7] - 2026-10-03
### Changed
- Missing modules are now installed in a single step at startup, using the running interpreter's pip and the correct package names (`bs4` installs `beautifulsoup4`)
- Installs into the active virtualenv when there is one, otherwise `--user`, falling back to `--break-system-packages` for externally managed Pythons
- Exits with a manual install command if installation fails

## [0.1.6] - 2026-10-03
### Removed
- Dead code: unused `execute_command`, stray `options` statement, no-op pip bootstrap and unused `subprocess` import

### Fixed
- Close file opened by `file_to_array`

## [0.1.5] - 2026-10-03
### Fixed
- `--fetch` no longer deletes the existing JSON file before the download succeeds

## [0.1.4] - 2026-10-03
### Fixed
- Selenium 4.10+ headless mode (`-headless` argument)
- Firefox process is now closed after fetching driver details

## [0.1.3] - 2026-10-03
### Fixed
- Driver detail parsing no longer raises on pages without `var details =`; invalid cached HTML is discarded with a warning

## [0.1.2] - 2026-10-03
### Fixed
- `--get` with a key missing from a record no longer raises `KeyError`

## [0.1.1] - 2026-10-03
### Fixed
- Default JSON file and work directory resolve correctly when run as `python jellyfish.py`

## [0.1.0] - 2026-10-03
### Fixed
- `--release` search crash: list-valued `releases` field is now matched per entry

## [0.0.9] - 2026-10-03
### Fixed
- Search crash on records with null fields (e.g. `--vendor` hitting `vendor: null`)

## [0.0.8] - 2021-11-30
### Changed
- Cleaned up output

## [0.0.7] - 2021-11-29
### Added
- Code to get value for key for driver

## [0.0.6] - 2021-11-29
### Added
- Initial code to fetch and process individual component information

### Changed
- Improved output

## [0.0.5] - 2021-11-25
### Added
- Code to fetch VMware HCL JSON file

## [0.0.4] - 2021-11-25
### Changed
- Improved search code

## [0.0.3] - 2021-11-25
### Added
- Code to deal with duplicates

## [0.0.2] - 2021-11-25
### Added
- `--get` switch

## [0.0.1] - 2021-11-24
### Added
- Initial load and print

## [0.0.0] - 2021-11-24
### Added
- Initial git repository commit
