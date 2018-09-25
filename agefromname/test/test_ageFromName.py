from unittest import TestCase

import pandas as pd

from agefromname.age_from_name import AgeFromName, InvalidSexException


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

	def test_get_all_name_female_prob(self):
		gender_prob = self.birth_year_predictor.get_all_name_female_prob()
		self.assertAlmostEqual(self.birth_year_predictor.prob_female('aaban'),
							   gender_prob.loc['aaban']['prob'],
							   places=4)
		self.assertAlmostEqual(self.birth_year_predictor.prob_female('alex'),
							   gender_prob.loc['alex']['prob'],
							   places=4)

	def test_get_all_name_male_prob(self):
		female_prob = self.birth_year_predictor.get_all_name_female_prob()
		male_prob = self.birth_year_predictor.get_all_name_male_prob()
		assert all((female_prob['prob'] + male_prob['prob']) > 0.999999)

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

	def test_prob_male(self):
		self.assertAlmostEqual(self.birth_year_predictor.prob_male('alex'), 0.9656, places=4)
		self.assertAlmostEqual(self.birth_year_predictor.prob_male('bill', minimum_age=90), 0.9819446677986078, places=4)
		self.assertAlmostEqual(self.birth_year_predictor.prob_male('bill', maximum_age=20), 1, places=4)
		self.assertAlmostEqual(self.birth_year_predictor.prob_male('taylor', current_year=1930), 1.0, places=4)

	def test_prob_female(self):
		self.assertAlmostEqual(self.birth_year_predictor.prob_female('alex'), 0.034385169011657335)
		self.assertAlmostEqual(self.birth_year_predictor.prob_female('bill', minimum_age=90), 1 - 0.9819446677986078,
		                       places=4)
		self.assertAlmostEqual(self.birth_year_predictor.prob_female('ariel', maximum_age=20), .808361029618998, places=4)
		self.assertAlmostEqual(self.birth_year_predictor.prob_female('ariel', minimum_age=20, maximum_age=40),
		                       .8139418787290704, places=4)
		self.assertAlmostEqual(self.birth_year_predictor.prob_female('ariel', maximum_age=40),
		                       .8108087012259286, places=4)
		self.assertAlmostEqual(self.birth_year_predictor.prob_female('taylor', current_year=1930), 1 - 1.0, places=4)

	def test_get_estimated_counts_None(self):
		actual = self.birth_year_predictor.get_estimated_counts('alex', None, 1940)
		self.assertEqual(type(actual), pd.Series)
		self.assertEqual(actual.name, 'estimated_count')
		self.assertEqual(set(actual.keys()),
		                 {1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889,
		                  1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899,
		                  1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909,
		                  1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919,
		                  1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929,
		                  1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939,
		                  1940})
		self.assertAlmostEqual(sum(actual), 24330.212406742125, places=0)

	def test_get_estimated_counts_bad_gender(self):
		with self.assertRaises(InvalidSexException):
			self.birth_year_predictor.get_estimated_counts('nancy', 'E', 1901)
		with self.assertRaises(InvalidSexException):
			self.birth_year_predictor.get_estimated_counts('nancy', 3, 1901)
		self.birth_year_predictor.get_estimated_counts('nancy')

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
