#################################
##### Name: Katherine Garrison ##
##### Uniqname: garrisok  #######
#################################

from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import shutil
import datetime
import plotly.graph_objs as go

# import dailyCovid19Data as covidOTD


def downloadEuroDataFile():
    ''' Sends request to url and saves data to json file in local dir.

    Parameters
    ----------
    None

    Returns
    -------
    none
    '''
    url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json'
    fileName = 'dailyCovid19Data.json'
    with urllib.request.urlopen(url) as response, open(fileName, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def convertEuroDataToDict():
    ''' Converts json data to dict format.

    Parameters
    ----------
    None

    Returns
    -------
    none
    '''
    with open('dailyCovid19Data.json', 'r') as file:
        return json.load(file)


def findRecordsForCountry(countryCode: str, records: list):
    '''Matches the countryCode ('geoID' key) with the countryCode of items in records param.

    Parameters
    ----------
    countryCode: string
    records: list of dicts

    Returns
    -------
    list
        a list of tuples that match the countryCode param
    '''
    #return [x for x in records if x['geoId'] == countryCode]
    output = []
    for x in records:
        if x['geoId'] == countryCode:
            output.append(x)
    return output


def findRecordWithMaxCases(records: list):
    ''' Converts 'cases' of each record and gives the max value

    Parameters
    ----------
    list

    Returns
    -------
    tuple of max count for 'cases'
    '''
    getCasesForRecord = lambda record: int(record['cases'])
    #print(getCasesForRecord(records[0]))
    return max(records, key=getCasesForRecord)


def findRecordWithMaxDeaths(records: list):
    ''' Converts 'deaths' of each record and gives the max value

    Parameters
    ----------
    list

    Returns
    -------
    tuple of max count for 'deaths'
    '''
    getDeathsForRecord = lambda record: int(record['deaths'])
    #print(getCasesForRecord(records[0]))
    return max(records, key=getDeathsForRecord)


def findMostRecentRecords(numDays: int, records: list):
    ''' Retrieves date information for the amount of most recent dates user chooses.

    Parameters
    ----------
    int
    list

    Returns
    -------
    list of dates
    '''
    convertRecordToDate = lambda record: datetime.date(int(record['year']), int(record['month']), int(record['day']))
    sortedRecords = sorted(records, key=convertRecordToDate)
    return sortedRecords[-numDays:]


def addDateObjectToRecords(records: list):
    ''' Returns formatted dates.

    Parameters
    ----------
    list

    Returns
    -------
    list - list of dates with proper format
    '''
    for record in records:
        record['date'] = datetime.date(int(record['year']), int(record['month']), int(record['day']))
    return records


def createCasesPlot(records):
    ''' Creates line plot for confirmed cases to be opened in internet browser.

    Parameters
    ----------
    List

    Returns
    -------
    none
    '''
    countryName = records[0]['countriesAndTerritories'].replace('_', ' ')
    xAxis = [record['date'].strftime("%B %d") for record in records]
        #print('xAxis=', xAxis)
        # xAxis = []
        # for record in recentRecordsWithDate:
        #     xAxis.append(record['date'].strftime("%B %d"))

        #xAxis = map(lambda record: record['date'].strftime("%B %d"), recentRecordsWithDate)

    yAxis = [int(record['cases']) for record in records]
    fig = go.Figure(data=go.Scatter(x=xAxis, y=yAxis, mode='lines+markers', marker={'symbol':'triangle-down', 'size':17, 'color':'navy'}, line={'color': 'lightskyblue', 'width':3, 'dash':'solid'}))
    fig.update_layout(title=f'Recent Cases in {countryName}', xaxis_title='Date', yaxis_title='Cases')
    fig.write_html("scatter-cases.html", auto_open=True)


def createDeathsPlot(records):
    ''' Creates line plot for confirmed deaths to be opened in internet browser.

    Parameters
    ----------
    list

    Returns
    -------
    none
    '''
    countryName = records[0]['countriesAndTerritories'].replace('_', ' ')
    xAxis = [record['date'].strftime("%B %d") for record in records]
    yAxis = [int(record['deaths']) for record in records]
    fig = go.Figure(data=go.Scatter(x=xAxis, y=yAxis, mode='lines+markers', marker={'symbol':'circle', 'size':21, 'color':'darkred'}, line={'color': 'black', 'width':3, 'dash':'solid'}))
    fig.update_layout(title=f'Recent Deaths in {countryName}', xaxis_title='Date', yaxis_title='Deaths')
    fig.write_html("scatter-deaths.html", auto_open=True)


def startInteractivePrompt():
    ''' Interacts with user, runs the program

    Parameters
    ----------
    None

    Returns
    -------
    none
    '''
    covidOTD = convertEuroDataToDict()
    records = covidOTD['records']
    while True:
        response = input("Enter Country Code (2 Letters) or 'exit': ")
        countryRecords = findRecordsForCountry(response, records)
        if response == 'exit':
            break
        if not countryRecords:
            print("Hey that's not a valid country code >:(")
            continue
        daysResponse = input("Enter Number of Days to retroactively report : ")
        while not daysResponse.isdigit():
            print('Hey that\'s not a positive integer >:(')
            daysResponse = input("Enter Number of Days: ")
        recentRecords = findMostRecentRecords(int(daysResponse), countryRecords)
        recentRecordsWithDate = addDateObjectToRecords(recentRecords)
        #print(recentCountryRecords)
        print("-------------")
        print("Requested days reported for " + recentRecords[0]['countriesAndTerritories'].replace("_", " "))
        print("-------------")
        print(f'{"Date":30}{"New Cases":15}{"New Deaths":15}')
        for record in recentRecordsWithDate:
            print(f"{record['date'].strftime('%A, %B %d, %Y'):30}{int(record['cases']):<15,d}{int(record['deaths']):<15,d}")
        # Show user plotly visualizations
        createCasesPlot(recentRecordsWithDate)
        createDeathsPlot(recentRecordsWithDate)

    #print(findRecordWithMaxDeaths(findRecordsForCountry('MX', records)))


if __name__ == '__main__':
    downloadEuroDataFile()
    startInteractivePrompt()

    # print(findDataForCountry('BR', records))


