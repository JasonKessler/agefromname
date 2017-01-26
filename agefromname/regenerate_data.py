import datetime
import io
import math
from urllib.request import urlopen
from zipfile import ZipFile

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def regenerate_birth_counts(
		census_zip_file=None,
		output_path='data/year_of_birth_counts.csv.gz'):
	'''Regenerate table containing counts of first names by sex and year of birth.

	:param census_zip_file: str, file-like object similar to http://www.ssa.gov/oact/babynames/names.zip, defaults to SSA.gov url
	:param output_path: str, path of .gz file to write dataframe csv
	:return: pd.DataFrame, pandas data frame with the columns first_name,sex,count,year_of_birth
	'''
	if census_zip_file is None:
		census_zip_file = io.BytesIO(urlopen('http://www.ssa.gov/oact/babynames/names.zip').read())
	year_of_birth_dfs = []
	with ZipFile(census_zip_file) as names_zip:
		for filename in names_zip.namelist():
			if filename.startswith('yob') and filename.endswith('txt'):
				cur_year_of_birth_df = pd.read_csv(names_zip.open(filename),
				                                   index_col=None,
				                                   names=['first_name', 'sex', 'count'])
				cur_year_of_birth_df['year_of_birth'] = filename[3:7]
				year_of_birth_dfs.append(cur_year_of_birth_df)
	year_of_birth_df = pd.concat(year_of_birth_dfs, ignore_index=True)
	year_of_birth_df['first_name'] = year_of_birth_df['first_name'].apply(str.lower)
	year_of_birth_df['sex'] = year_of_birth_df['sex'].apply(str.lower)
	year_of_birth_df.to_csv(output_path, index=False, compression='gzip')
	return year_of_birth_df


def _decade_mortality_table(year,
                            url_template='https://www.ssa.gov/oact/NOTES/as120/LifeTables_Tbl_7_{}.html'):
	assert int(year) % 10 == 0
	url = url_template.format(year)
	soup = BeautifulSoup(urlopen(url).read(), 'lxml')
	table = soup.find('table', border=1)
	rows = []
	for row in table.find_all('tr'):
		row_datum = [cell.text.strip() for cell in row.find_all('td')]
		if len(row_datum) == 15 and row_datum[0] != '':
			rows.append({
				'year_of_birth': int(year),
				'age': int(row_datum[0]),
				'm_prob_survive_that_year': 1 - float(row_datum[1]),
				'f_prob_survive_that_year': 1 - float(row_datum[9]),
			})
	df = pd.DataFrame(rows).sort_values(by='age')
	for sex in 'mf':
		df[sex + '_prob_alive'] = np.cumprod(df[sex + '_prob_survive_that_year']).astype(np.float64)
	df['as_of_year'] = df['year_of_birth'] + df['age']
	return df[['year_of_birth', 'as_of_year', 'm_prob_alive', 'f_prob_alive']]


def regenerate_decade_mortality_table(
		url_template='https://www.ssa.gov/oact/NOTES/as120/LifeTables_Tbl_7_{}.html',
		output_path='data/mortality_table.csv.gz',
		min_decade=1900,
		max_decade=math.ceil(datetime.datetime.now().year * 0.1) * 10):
	'''
	:param url_template: str, url tempate (with year as {}) to scrape
	:param output_path: str, path of .gz file to write dataframe csv
	:param min_decade: int, minimum decade to search
	:param max_decade: int, maximum decade to search
	:return: pd.DataFrame, pandas data frame with the columns year_of_birth,as_of_year,m_death_prob,f_death_prob
	'''
	mortality_df = pd.concat([_decade_mortality_table(year, url_template)
	                          for year
	                          in range(min_decade, max_decade, 10)], axis=0)
	mortality_df.to_csv(output_path, index=False, compression='gzip')
	return mortality_df


def regenerate_all():
	regenerate_birth_counts()
	regenerate_decade_mortality_table()
