from unittest import TestCase

import pandas as pd

from agefromname.age_from_name import AgeFromName


class TestBirthYearPredictor(TestCase):
	def setUp(cls):
		cls.birth_year_predictor = AgeFromName()

	def test_get_argmax(self):
		birth_year_predictor = self.birth_year_predictor
		self.assertEqual(birth_year_predictor.argmax('jason', 'm', 2017), 1977)
		self.assertEqual(birth_year_predictor.argmax('JAsOn', 'M', 2017), 1977)
		self.assertEqual(birth_year_predictor.argmax('jennifer', 'f', 2017), 1972)
		self.assertEqual(birth_year_predictor.argmax('jeNNifer', 'F', 2017), 1972)
		self.assertEqual(birth_year_predictor.argmax('nancy', 'f', 2017), 1952)

	def test_get_argmax_default(self):
		self.birth_year_predictor.argmax('nancy', 'f')

	def test_argmax_not_current_year(self):
		self.assertEqual(self.birth_year_predictor.argmax('nancy', 'f', 1901), 1900)

	def test_get_estimated_distribution(self):
		actual = self.birth_year_predictor.get_estimated_distribution('nancy', 'f', 1901)
		self.assertEqual(type(actual), pd.Series)
		self.assertEqual(actual.name, 'estimate_percentage')
		self.assertEqual(set(actual.keys()),
		                 {1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889,
		                  1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899,
		                  1900, 1901})
		self.assertAlmostEqual(sum(actual), 1)

	def test_get_estimated_counts(self):
		actual = self.birth_year_predictor.get_estimated_counts('nancy', 'f', 1901)
		self.assertEqual(type(actual), pd.Series)
		self.assertEqual(actual.name, 'estimated_count')
		self.assertEqual(set(actual.keys()),
		                 {1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889,
		                  1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899,
		                  1900, 1901})
		self.assertAlmostEqual(sum(actual), 9669, places=0)

	def test_get_estimated_counts_minimum_age(self):
		min_age_30 = self.birth_year_predictor.get_estimated_counts('nancy', 'f',
		                                                            current_year=1960,
		                                                            minimum_age=30)
		min_age_0 = self.birth_year_predictor.get_estimated_counts('nancy', 'f',
		                                                           current_year=1960)
		explicit_min_age_0 = self.birth_year_predictor.get_estimated_counts('nancy', 'f',
		                                                                    current_year=1960,
		                                                                    minimum_age=0)
		born_in_1930 = self.birth_year_predictor.get_estimated_counts('nancy', 'f',
		                                                              current_year=1930,
		                                                              minimum_age=0)
		self.assertEqual(set(explicit_min_age_0),
		                 set(min_age_0))
		self.assertNotEqual(set(born_in_1930), set(min_age_30))
		self.assertEqual(min_age_0.index.max() - min_age_30.index.max(), 30)
		self.assertGreater(min_age_0.sum(), min_age_30.sum())
		self.assertEqual(set(min_age_0.ix[min_age_30.index]), set(min_age_30))

	def test_get_estimated_distribution_minimum_age(self):
		min_age_30 = self.birth_year_predictor.get_estimated_distribution('nancy', 'f',
		                                                                  current_year=1960,
		                                                                  minimum_age=30)
		self.assertAlmostEqual(min_age_30.sum(), 1.)

	def test_argmax_minimum_age(self):
		argmax_age_30 = self.birth_year_predictor.argmax('nancy', 'f',
		                                                 current_year=1960,
		                                                 minimum_age=30)
		argmax_age_0 = self.birth_year_predictor.argmax('nancy', 'f',
		                                                current_year=1960)

		self.assertLess(argmax_age_30, argmax_age_0)
