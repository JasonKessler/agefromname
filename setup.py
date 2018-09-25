from setuptools import setup, find_packages

setup(name='agefromname',
      version='0.0.8',
      description='Predict how old someone is from their name and gender, using the baby name data from the US Social Security Administration. Predicts gender from name as well.',
      url='https://github.com/JasonKessler/agefromname',
      author='Jason Kessler',
      author_email='jason.kessler@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
	      'nose',
	      'numpy',
	      'pandas',
	      'statsmodels',
	      'beautifulsoup4'
      ],
      package_data={
	      'agefromname': ['data/*']
      },
      test_suite="nose.collector",
      tests_require=['nose'],
      setup_requires=['nose>=1.0'],
      zip_safe=False)
