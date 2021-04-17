# Web Scrape Test

Web Scrape Test is a Python Scraper for extracting currency data.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Scraper.

Available in an async and non-async version.

```bash
pip setup.py install
```

## Usage non-async

```python
from web_scrape.configuration import create_app


if __name__ == '__main__':
    app = create_app()
    app.run()
```

## Usage async

```python
import asyncio
from web_scrape.configuration import create_app


if __name__ == '__main__':
    app = create_app()
    asyncio.run(app.async_run())
```

## License
[MIT](https://choosealicense.com/licenses/mit/)