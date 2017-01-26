import os
from datetime import datetime

import numpy as np
import pandas as pd


class AgeFromName(object):
	def __init__(self, mortality_df=None, year_of_birth_df=None):
		'''
		:param mortality_df: pd.DataFrame, optional
		:param year_of_birth_df: pd.DataFrame, optional
		'''
		if mortality_df is None:
			self._mortality_df = pd.read_csv(self._get_data_path('mortality_table.csv.gz'))
		else:
			self._mortality_df = mortality_df
		if year_of_birth_df is None:
			self._year_of_birth_df = pd.read_csv(self._get_data_path('year_of_birth_counts.csv.gz'))
		else:
			self._year_of_birth_df = year_of_birth_df

	def _get_data_path(self, file_name):
		return os.path.join(os.path.dirname(__file__), 'data', file_name)

	def get_estimated_counts(self, first_name, sex, current_year=datetime.now().year):
		'''
		:param first_name: str, First name
		:param sex: str, m or f for sex
		:param current_year: int, optional, defaults to current year
		:return: pd.Series, with int indices indicating years of
			birth, and estimated counts of total population with that name and birth year
		'''
		first_name = first_name.lower()
		sex = sex.lower()
		cur_df = (self._year_of_birth_df[(self._year_of_birth_df.first_name == first_name)
		                                 & (self._year_of_birth_df.sex == sex)
		                                 & (self._year_of_birth_df.year_of_birth <= current_year)]
		          [['year_of_birth', 'count']])
		year_stats = (self._mortality_df[self._mortality_df.as_of_year == current_year]
		              [['year_of_birth', sex + '_prob_alive']])
		cur_df['prob_alive'] = np.interp(cur_df.year_of_birth,
		                                 year_stats.year_of_birth,
		                                 year_stats[sex + '_prob_alive'])
		cur_df['estimated_count'] = cur_df['prob_alive'] * cur_df['count']
		return cur_df.set_index('year_of_birth')['estimated_count']

	def get_mle(self, first_name, sex, current_year=datetime.now().year):
		'''
		:param first_name: str, First name
		:param sex: str, m or f for sex
		:param current_year: int, optional, defaults to current year
		:return: int, the most likely year of birth
		'''
		return self.get_estimated_counts(first_name, sex, current_year).argmax()

	def get_estimated_distribution(self, first_name, sex, current_year=datetime.now().year):
		'''
		:param first_name: str, First name
		:param sex: str, m or f for sex
		:param current_year: int, optional, defaults to current year
		:return: pd.Series, with int indices indicating years of
			birth, and the estimated percentage of the total population of people who share sex and
			first name who were born that year.
		'''
		age_counts = self.get_estimated_counts(first_name, sex, current_year)
		to_ret = age_counts / age_counts.sum()
		to_ret.name = 'estimate_percentage'
		return to_ret
