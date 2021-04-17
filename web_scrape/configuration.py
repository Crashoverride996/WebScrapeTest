from environs import Env

from web_scrape.scraper import Scraper


def create_configuration():

	env = Env()
	env.read_env()
	config = {}

	start_url = env.str('START_URL')
	time_interval = env.int('TIME_INTERVAL')
	page_count = env.int('PAGE_COUNT')
	output_directory = env.str('OUTPUT_DIRECTORY', default='output')
	output_format = env.str('OUTPUT_FORMAT', default='.csv')
	print(f'Using ./{output_directory} as location for output of {output_format} files')
	print(f'Time interval set to {time_interval}')

	config['start_url'] = start_url
	config['time_interval'] = time_interval
	config['page_count'] = page_count
	config['output_directory'] = output_directory
	config['output_format'] = output_format

	return config


def init_app(config):
	app = Scraper(config)

	return app


def create_app():
	app = init_app(create_configuration())

	return app
