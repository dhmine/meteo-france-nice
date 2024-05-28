import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import sys
import getopt
import os

urlbase = "https://www.historique-meteo.net/france/provence-alpes-cote-d-azur/nice"

def getWeatherData(url):
    """
    Fetch weather data from the given URL.

    Parameters:
    url (str): URL of the weather website.

    Returns:
    dict: A dictionary containing weather data.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = {
        'Température maximale': None,
        'Température minimale': None,
        'Vitesse du vent': None,
        'Humidité': None,
        'Visibilité': None,
        'Couverture nuageuse': None,
        'Durée du jour': None
    }

    table = soup.find('table', class_='table')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                label = cols[0].text.strip()
                value = cols[3].text.strip()
                
                if "Température maximale" in label:
                    data['Température maximale'] = value
                elif "Température minimale" in label:
                    data['Température minimale'] = value
                elif "Vitesse du vent" in label:
                    data['Vitesse du vent'] = value
                elif "Précipitations" in label:
                    data['Précipitations'] = value
                elif "Humidité" in label:
                    data['Humidité'] = value
                elif "Visibilité" in label:
                    data['Visibilité'] = value
                elif "Couverture nuageuse" in label:
                    data['Couverture nuageuse'] = value
                elif "Durée du jour" in label:
                    data['Durée du jour'] = value

    return data

def getMeteoByDay(region, day):
    """
    Get weather data for a specific day.

    Parameters:
    region (str): Region name.
    day (str): Date in YYYY/MM/DD format.

    Returns:
    DataFrame: A Pandas DataFrame containing the weather data.
    """
    try:
        url = f"{urlbase}/{day}/"
        print(f"Fetching URL: {url}")
        data = getWeatherData(url)
        data['region'] = region
        data['day'] = day
        return pd.DataFrame([data])
    except Exception as e:
        print(f"Error in getMeteoByDay for region {region} on day {day}: {e}")
        return pd.DataFrame(columns=list(data.keys()) + ['region', 'day'])

def getMeteoData(start_date, end_date, folder, region):
    """
    Fetch weather data for a date range.

    Parameters:
    start_date (str): Start date in YYYY/MM/DD format.
    end_date (str): End date in YYYY/MM/DD format.
    folder (str): Folder to save the CSV file.
    region (str): Region name.

    Returns:
    str: The filename of the saved CSV file.
    """
    ds = pd.DataFrame()
    start = datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.strptime(end_date, "%Y/%m/%d")
    filename = f"Meteo_{region}_{start_date.replace('/', '-')}_{end_date.replace('/', '-')}.csv"

    while start <= end:
        ds_one_day = getMeteoByDay(region, start.strftime("%Y/%m/%d"))
        ds = pd.concat([ds, ds_one_day], ignore_index=True)
        start += timedelta(days=1)

    if not os.path.exists(folder):
        os.makedirs(folder)
    ds.to_csv(f"{folder}/{filename}", index=False)
    return filename

def usage():
    """
    Print usage information.
    """
    print('Meteo Gathering Usage: python script.py -s <Start Date> -e <End Date> -f <Target Folder>')

def main():
    """
    Main function to parse arguments and fetch weather data.
    """
    start_date, end_date, target_folder = '', '', ''

    try:
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "s:e:f:h")
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            return
        elif opt in ["-s"]:
            start_date = arg.strip()
        elif opt in ["-e"]:
            end_date = arg.strip()
        elif opt in ["-f"]:
            target_folder = arg.strip()

    if not start_date or not end_date or not target_folder:
        usage()
        sys.exit(2)

    print(f"Fetching data from {start_date} to {end_date} for region Nice")

    try:
        filename = getMeteoData(start_date, end_date, target_folder, 'nice')
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error while gathering meteo data: {e}")

if __name__ == "__main__":
    main()
