from collections import Counter
from unittest import TestCase
import pandas as pd
from agefromname import AgeFromName
from agefromname.generation_from_name import GenerationFromName, InvalidGenerationBirthYearDefinition


class TestGenerationFromName(TestCase):
	def test_validation(self):
		g = GenerationFromName()
		a = AgeFromName()
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName(3, a)
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName({'AAA': {3, 1}}, a)
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName({'AAA': [3, 1, 1]}, a)
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName({'AAA': [1]}, a)
		g = GenerationFromName({'AAA': [1999, 1999]}, a)
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName({'AAA': [1999, 1888]}, a)
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName({'AAA': [1999, 1888]}, a)
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName({'AAA': [1999, 1999], 'BBB': [1888, 2000]}, a)
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName({'AAA': [1990, 2000], 'BBB': [1985, 1990]}, a)
		with self.assertRaises(InvalidGenerationBirthYearDefinition):
			g = GenerationFromName({'AAA': [1990, 2000], 'BBB': [1985, 1990]}, a)
		g = GenerationFromName({'AAA': [1990, 2000], 'BBB': [2001, 2010]}, a)

	def test_get_estimated_counts(self):
		g = GenerationFromName({'AAA': [1930, 1945], 'BBB': [1946, 1999]})
		year_count = AgeFromName().get_estimated_counts('nancy', 'f', 1950)
		actual = g.get_estimated_counts('nancy', 'f', 1950)
		self.assertEqual(type(actual), pd.Series)
		self.assertEqual(actual.name, 'estimated_count')
		self._manually_verify_counts_or_distribution(actual, year_count)

		self.assertAlmostEqual(sum(actual), sum(year_count), places=0)


	def test_get_estimated_distribution(self):
		g = GenerationFromName({'AAA': [1930, 1945], 'BBB': [1946, 1999]})
		year_distribution = AgeFromName().get_estimated_distribution('nancy', 'f', 1950)
		actual = g.get_estimated_distribution('nancy', 'f', 1950)
		self.assertEqual(type(actual), pd.Series)
		self.assertEqual(actual.name, 'estimate_percentage')
		self._manually_verify_counts_or_distribution(actual, year_distribution)

		self.assertAlmostEqual(sum(actual), 1, places=0)

	def _manually_verify_counts_or_distribution(self, actual, year_count):
		self.assertEqual(set(actual.keys()),
		                 {'AAA', 'BBB', '_other'})
		expected = Counter()
		for year, cnt in year_count.iteritems():
			if 1930 <= year <= 1945:
				expected['AAA'] += cnt
			elif 1946 <= year <= 1999:
				expected['BBB'] += cnt
			else:
				expected['_other'] += cnt
		self.assertAlmostEqual(expected['AAA'], actual['AAA'], places=0)
		self.assertAlmostEqual(expected['BBB'], actual['BBB'], places=0)
		self.assertAlmostEqual(expected['_other'], actual['_other'], places=0)
