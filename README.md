# sqlean-driver

[![PyPI - Version](https://img.shields.io/pypi/v/sqlean-driver.svg)](https://pypi.org/project/sqlean-driver)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sqlean-driver.svg)](https://pypi.org/project/sqlean-driver)

A SQLAlchemy driver for [`sqlean.py`](https://github.com/nalgeon/sqlean.py).

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
  - [Extensions](#extensions)
- [License](#license)

## Installation

```console
pip install sqlean-driver
```

## Usage

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite+sqlean:///:memory:?extensions=all")

with engine.connect() as conn:
    result = conn.execute(text("SELECT ipfamily('192.168.1.1')"))
    print(result.scalar())  # 4
```

### Extensions

By default, `sqlean.py` disables all [SQLite extensions](https://github.com/nalgeon/sqlean.py#extensions). To enable all of them, pass `extensions=all` as a query parameter to the connection string. Or use a comma-separated list of extensions to enable only some of them, e.g. `extensions=ipaddr,crypto`.

## License

`sqlean-driver` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
