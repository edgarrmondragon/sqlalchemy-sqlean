# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html),
and is generated by [git-cliff](https://github.com/orhun/git-cliff).

## [0.2.0] - 2024-10-27

### Added

- Official support for Python 3.13 ([#115](https://github.com/edgarrmondragon/sqlean-driver/issues/115))

### Testing

- Test with Python 3.13 ([#42](https://github.com/edgarrmondragon/sqlean-driver/issues/42))

## [0.1.1] - 2023-10-07

### Added

- Official support for Python 3.12 ([#39](https://github.com/edgarrmondragon/sqlean-driver/issues/39))

### Testing

- Report version `sqlean.py` in pytest output ([#25](https://github.com/edgarrmondragon/sqlean-driver/issues/25))
- Catch warnings ([#28](https://github.com/edgarrmondragon/sqlean-driver/issues/28))

## [0.1.0] - 2023-08-14

### Added

- Support Python 3.12 ([#5](https://github.com/edgarrmondragon/sqlean-driver/issues/5))

### Testing

- Test on Windows and MacOS ([#15](https://github.com/edgarrmondragon/sqlean-driver/issues/15))
- Add end-to-end SQL test ([#12](https://github.com/edgarrmondragon/sqlean-driver/issues/12))

### Change

- Remove `__about__.py` ([#18](https://github.com/edgarrmondragon/sqlean-driver/issues/18))

## [0.0.1] - 2023-07-06

### Fixed

- Address `Dialect.dbapi` deprecation warning by implementing `import_dbapi` ([#14](https://github.com/edgarrmondragon/sqlean-driver/issues/14))

## [0.0.1a3] - 2023-07-06

### Documentation

- Use the `select` API in examples ([#8](https://github.com/edgarrmondragon/sqlean-driver/issues/8))
- Clarify wording on how to use the `create_engine(..., module=sqlean)` alternative ([#10](https://github.com/edgarrmondragon/sqlean-driver/issues/10))
- Document typing check script

### Fixed

- Ensure compatibility with SQLAlchemy 1 ([#13](https://github.com/edgarrmondragon/sqlean-driver/issues/13))

### Testing

- Check error when no extensions are installed ([#7](https://github.com/edgarrmondragon/sqlean-driver/issues/7))

## [0.0.1a2] - 2023-06-28

### Documentation

- Add development instructions ([#2](https://github.com/edgarrmondragon/sqlean-driver/issues/2))

<!-- generated by git-cliff -->
