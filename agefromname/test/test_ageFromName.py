from unittest import TestCase
import pandas as pd
from agefromname.age_from_name import AgeFromName


class TestBirthYearPredictor(TestCase):
	def setUp(cls):
		cls.birth_year_predictor = AgeFromName()

	def test_get_mle(self):
		birth_year_predictor = self.birth_year_predictor
		self.assertEqual(birth_year_predictor.get_mle('jason', 'm', 2017), 1977)
		self.assertEqual(birth_year_predictor.get_mle('JAsOn', 'M', 2017), 1977)
		self.assertEqual(birth_year_predictor.get_mle('jennifer', 'f', 2017), 1972)
		self.assertEqual(birth_year_predictor.get_mle('jeNNifer', 'F', 2017), 1972)
		self.assertEqual(birth_year_predictor.get_mle('nancy', 'f', 2017), 1952)

	def test_get_mle_default(self):
		self.birth_year_predictor.get_mle('nancy', 'f')

	def test_mle_not_current_year(self):
		self.assertEqual(self.birth_year_predictor.get_mle('nancy', 'f', 1901), 1900)

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