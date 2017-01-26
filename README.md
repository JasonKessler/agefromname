# AgeFromName 0.0.1
A tool for predicting someone's age or generation given their name and assigned sex at birth, 
assuming they were born in the US.

Feel free to use the Gitter community [gitter.im/agefromname](https://gitter.im/agefromname/Lobby) for help or to discuss the project.   

## Installation

`$ pip install agefromname`

## Overview

This more or less apes the approach of FiveThirtyEight's ["How to Tell if Someone's  Age
When All you Know Is Her Name"](https://fivethirtyeight.com/features/how-to-tell-someones-age-when-all-you-know-is-her-name/) article.
 
It includes data collected scraped from the Social Security 
Administration's [Life Tables for the United States Social Security Area 1900-2100](https://www.ssa.gov/oact/NOTES/as120/LifeTables_Body.html#wp1168591)
 and their [baby names data](http://www.ssa.gov/oact/babynames/names.zip). Code is included
 to re-scrape and refresh this data in `regenerate_data.py`.  It includes data as far back as
 1981.

To use, first initialize the finder

```pydocstring
>>> from agefromname import AgeFromName
>>> age_from_name = AgeFromName()
```

Now you can use this to get the maximum likelihood estimate of someone's age, give their first name and 
gender.  Note that their gender should be a single letter, 'm' or 'f' (case-insensitive), and that the
  first name is case-insensitive as well.
  
```pydocstring
>>> age_from_name.get_mle('jAsOn', 'm')
1977
>>> age_from_name.get_mle('Jason', 'M')
1977
```

You can also include find the MLE after as of a particular year.  Note that if omitted, the current
year is used.

```pydocstring
>>> age_from_name.get_mle('john', 'm', 1980)
1947
>>> age_from_name.get_mle('john', 'm', 2000)
1964
```

Getting estimated counts of living people with a giving name and gender at a particular date is easy, 
and given in a Pandas Series.
```pydocstring
>>> age_from_name.get_estimated_counts('john', 'm', 1960)
year_of_birth
1881     4613.792420
1882     5028.397099
1883     4679.560929
...
```

We can see corresponding probability distribution using

```pydocstring
>>> age_from_name.get_estimated_distribution('mary', 'f', 1910)
year_of_birth
1881    0.016531
1882    0.019468
1883    0.019143
...
```

Finally, we can see similar information for generations, as well, using the GenerationFromName class.
```pydocstring
>>> generation_from_name.get_mle('barack', 'm')
'Generation Z'
>>> generation_from_name.get_mle('ashley', 'f')
'Millenials'
>>> generation_from_name.get_mle('monica', 'f')
'Generation X'
>>> generation_from_name.get_mle('bill', 'm')
'Baby Boomers
>>> generation_from_name.get_mle('bill', 'f')
'Greatest Generation'
>>> generation_from_name.get_estimated_distribution('jaden', 'm')
Baby Boomers           0.000000
Generation X           0.001044
Generation Z           0.897662
Greatest Generation    0.000000
Millenials             0.101294
_other                 0.000000
Name: estimate_percentage, dtype: float64
>>> generation_from_name.get_estimated_distribution('gertrude', 'f')
Baby Boomers           0.259619
Generation X           0.031956
Generation Z           0.009742
Greatest Generation    0.425293
Millenials             0.011412
_other                 0.261979
>>> generation_from_name.get_estimated_counts('ashley', 'f')
Baby Boomers              702.481287
Generation X            29274.206090
Generation Z           141195.016621
Greatest Generation        34.998913
Millenials             652914.233604
_other                      0.102625
Name: estimated_count, dtype: float64
```

