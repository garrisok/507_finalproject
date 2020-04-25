# About COVID-19 Project

This is a simple program, aggregating specified data from COVID-19 confirmed cases and deaths by country. Country and dates are chosen by user through input.

## How to work it

User is prompted to specify the Alpha2 country code to attain data on.
    Refer to "geoId.txt” file for list of country names and alpha-2 codes. This file contains a list of 249 countries the user can choose from. See examples below for user input.

### Data Source

When the "507_Covid_Project.py" is ran data from the European Centre for Disease PRevention and Control (ECDC) site is created into a JSON file on the user's current directory. The user is promted for once data is pulled form the site. The file is created each time the program is ran, updating daily data. The file created is name "dailyCovid19Data.json".

**European Centre for Diease Prevention and Control (ECDC)** - *Main Site* - [ECDC](https://www.ecdc.europa.eu/en)
**ECDC Daily Data on COVID-19 Cases** - *Data Site* - [ECDC](https://opendata.ecdc.europa.eu/covid19/casedistribution/json)

### Prerequisites

Python are packages needed to run this program.

```
from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import shutil
import datetime
import plotly.graph_objs as go
```

### User Input

First promt user interacts with is to specify the country to request COVID-19 data on.

Example of user input: "US"
```
Enter Country Code (2 Letters) or 'exit': US
```
Next, user is prompted to specify the amount of days to retroactively report on. Requests include present day.
Below example reuqests information for US and the last 5-days.

Example of user input request: "5"

```
Enter Number of Days to retroactively report : 5
```
Upon selection of number of days, output will look similar to displayed table below. User will be able to continue requesting data with the input loop, or exit the program.
Two windows will open in an internet browser showing a graph for "Recent Deaths in United States of America" and "Recent Cases in United States of America":

```
-------------
Requested days reported for United States of America
-------------
Date                          New Cases      New Deaths
Tuesday, April 21, 2020       28,065         1,857
Wednesday, April 22, 2020     37,289         2,524
Thursday, April 23, 2020      17,588         1,721
Friday, April 24, 2020        26,543         3,179
Saturday, April 25, 2020      21,352         1,054
Enter Country Code (2 Letters) or 'exit':
```
![Confirmed Cases](https://github.com/garrisok/507_finalproject/blob/master/images/recent_cases.JPG)


<img src="https://github.com/garrisok/507_finalproject/blob/master/images/recent_deaths.JPG" width="250">

## Authors

* **Katherine Garrison** - *Current work* - [GitHub](https://github.com/garrisok)

