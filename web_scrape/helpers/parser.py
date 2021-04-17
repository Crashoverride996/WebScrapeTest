import asyncio

from bs4 import BeautifulSoup

from web_scrape.helpers.origin import get_header


async def parse_currency(loop, session, currency, url, currency_json, page_count, output_directory, output_format):
	header = None
	rows = []
	page = 1

	currency_json['pjname'] = currency
	currency_json['page'] = page

	try:

		async with session.post(url, headers=get_header(), data=currency_json, timeout=300) as resp:
			content = await resp.read()
			text = content.decode('utf-8', errors='replace')

			soup = BeautifulSoup(text, 'html.parser')

			if not header:
				header = [header.get_text() for header in soup.find_all("td", {"class": "lan12_hover"})]

			rows_tags = soup.find_all('tr')[2:]
			rows_value = [[column.get_text() for column in row.find_all('td')] for row in rows_tags]
			rows.extend(rows_value[1:-4])

			tasks = []

			page += 1

			while page < page_count:
				currency_json['page'] = page
				task = loop.create_task(parse_currency_subpage(session, url, currency_json))
				tasks.append(task)
				page += 1
			results = await asyncio.gather(*tasks)

			rows.extend([x[0] for x in results])

			filename = output_directory + '/' + currency + '_' + str(currency_json['erectDate']) + '_' + str(currency_json['nothing']) + output_format # noqa

			return filename, header, rows

	except Exception as e:
		print(f'\tError occurred while extracting data for currency: {currency}, on page {page}')
		print('\tError: ' + str(e))
		print('\tContinuing...')


async def parse_currency_subpage(session, url, currency_json):
	rows = []

	async with session.post(url, headers=get_header(), data=currency_json, timeout=300) as resp:
		content = await resp.read()
		text = content.decode('utf-8', errors='replace')

		soup = BeautifulSoup(text, 'html.parser')

		rows_tags = soup.find_all('tr')[2:]
		rows_value = [[column.get_text() for column in row.find_all('td')] for row in rows_tags]
		rows.extend(rows_value[1:-4])

	return rows
