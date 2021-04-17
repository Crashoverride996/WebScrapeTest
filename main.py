# import asyncio
from web_scrape.configuration import create_app


if __name__ == '__main__':
    app = create_app()
    app.run()
    # asyncio.run(app.async_run())
