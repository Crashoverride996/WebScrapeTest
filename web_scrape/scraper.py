import json
import asyncio
import aiohttp
import requests
import datetime as dt
from datetime import datetime

from bs4 import BeautifulSoup

from web_scrape.helpers import get_header, create_csv, parse_currency

json_template = """
	{
		"erectDate": "",
		"nothing": "",
		"pjname": "",
		"page": ""
	}
"""


class Scraper:
	"""
		A class to represent a scraper.


		Attributes
		----------
		config : dict
			configuration loaded from environment variables

		Methods
		-------
		run():
			Extracts all information for each currency and saves it in csv file.
	"""

	def __init__(self, config=None):
		self.start_url = config.get('start_url')
		self.time_interval = config.get('time_interval')
		self.page_count = config.get('page_count')
		self.output_directory = config.get('output_directory')
		self.output_format = config.get('output_format')

	def __del__(self):
		print(f'End of program - {datetime.now().time()}')

	def run(self):
		"""
			Performs extraction of data for all of currencies available

			Returns:
				Integer: Number of extracted currencies

		"""
		print(f'Start of program - {datetime.now().time()}')

		currency_json = json.loads(json_template)
		time_interval = self.time_interval

		page = 1
		last_page = self.page_count

		today = dt.date.today()
		n_days_ago = (today - dt.timedelta(days=time_interval)).isoformat()
		today = today.isoformat()

		currency_page = requests.get(self.start_url, headers=get_header()).content

		soup = BeautifulSoup(currency_page, 'html.parser')

		currencies = [currency['value'] for currency in soup.find_all('option') if len(currency['value']) > 1]

		header = None
		rows = []

		currency_json['erectDate'] = n_days_ago
		currency_json['nothing'] = today

		for idx, currency in enumerate(currencies):

			print(f'Progress: {idx}/{len(currencies)} - Currency: {currency}')

			currency_json['pjname'] = currency

			while page < last_page:

				try:

					today = dt.date.today()

					currency_json['page'] = page

					currency_subpage = requests.post(self.start_url, headers=get_header(), data=currency_json).content

					soup = BeautifulSoup(currency_subpage, 'html.parser')

					if not header:
						header = [header.get_text() for header in soup.find_all("td", {"class": "lan12_hover"})]

					rows_tags = soup.find_all('tr')[2:]
					rows_value = [[column.get_text() for column in row.find_all('td')] for row in rows_tags]
					rows.extend(rows_value[1:-4])
				except Exception as e:
					print(f'\tError occurred while extracting data for currency: {currency}, on page {page}')
					print('\tError: ' + str(e))
					print('\tContinuing...')
				finally:
					page += 1

			filename = self.output_directory + '/' + currency + '_' + str(n_days_ago) + '_' + str(
				today) + self.output_format  # noqa

			create_csv(filename, header, rows)
			print(f'\tExtracted {len(rows)} rows')

			page = 1
			rows = []

		return len(currencies)

	async def async_run(self):
		"""
			Asynchronously performs extraction of data for all of currencies available

			Returns:
				Integer: Number of extracted currencies

		"""
		print(f'Start of program - {datetime.now().time()}')

		loop = asyncio.get_event_loop()

		currency_json = json.loads(json_template)
		time_interval = self.time_interval

		last_page = self.page_count

		today = dt.date.today()
		n_days_ago = (today - dt.timedelta(days=time_interval)).isoformat()
		today = today.isoformat()

		currency_page = requests.get(self.start_url, headers=get_header()).content

		soup = BeautifulSoup(currency_page, 'html.parser')

		currencies = [currency['value'] for currency in soup.find_all('option') if len(currency['value']) > 1]

		currency_json['erectDate'] = n_days_ago
		currency_json['nothing'] = today

		for idx, currency in enumerate(currencies):
			async with aiohttp.ClientSession() as session:
				filename, header, rows = await parse_currency(loop, session, currency, self.start_url, currency_json,
															  last_page, self.output_directory, self.output_format)
				create_csv(filename, header, rows)
				print(f'\tExtracted {len(rows)} rows')

		return len(currencies)
