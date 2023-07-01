# sqlean-driver

[![PyPI - Version](https://img.shields.io/pypi/v/sqlean-driver.svg)](https://pypi.org/project/sqlean-driver)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sqlean-driver.svg)](https://pypi.org/project/sqlean-driver)

A SQLAlchemy driver for [`sqlean.py`](https://github.com/nalgeon/sqlean.py).

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
  - [Extensions](#extensions)
  - [Alternatives](#alternatives)
- [License](#license)

## Installation

```console
pip install sqlean-driver
```

## Usage

```python
from sqlalchemy import create_engine, func, select

engine = create_engine("sqlite+sqlean:///:memory:?extensions=all")

with engine.connect() as conn:
    result = conn.execute(select(func.ipfamily("192.168.1.1")))
    print(result.scalar())  # 4
```

### Extensions

By default, `sqlean.py` disables all [SQLite extensions](https://github.com/nalgeon/sqlean.py#extensions). To enable all of them, pass `extensions=all` as a query parameter to the connection string. Or use a comma-separated list of extensions to enable only some of them, e.g. `extensions=ipaddr,crypto`.

### Alternatives

Note that you don't strictly need this driver to use `sqlean.py` with SQLAlchemy. You can supply `sqlean` as the [`module`](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.module) parameter to `create_engine`:

```python
import sqlean
from sqlalchemy import create_engine, func, select

sqlean.extensions.enable_all()
engine = create_engine("sqlite:///:memory:", module=sqlean)

with engine.connect() as conn:
    result = conn.execute(select(func.ipfamily("192.168.1.1")))
    print(result.scalar())  # 4
```

## Development

This project uses [Hatch](https://hatch.pypa.io/) to manage the development environment, so make sure you have it installed.

### Run tests and coverage

```console
hatch run cov
```

### Run linter

```console
hatch run lint:style
```

### Run type checker

```console
hatch run typing:check
```

## License

`sqlean-driver` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
