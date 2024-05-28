# Meteo Nice Scraper

This project scrapes historical weather data for Nice, France from the website [historique-meteo.net](https://www.historique-meteo.net/france/provence-alpes-cote-d-azur/nice) and saves the data to a CSV file.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Example](#example)


## Introduction

The Meteo Nice Scraper is a Python-based project designed to fetch historical weather data for Nice, France. The data includes temperature, wind speed, humidity, visibility, cloud cover, and day length, and is saved to a CSV file for easy analysis.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine
- pip (Python package installer)
- An internet connection to fetch data from the web

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/dhmine/meteo-france-nice.git
   cd meteo-france-nice
   
2. **Create a Virtual Environment:**
    ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

4. **Install the Required Libraries:**
   ```bash
   pip install -r requirements.txt

## Usage
To fetch weather data for a specific date range and save it to a CSV file, use the following command:
  ```bash
   python scraper.py -s <Start Date> -e <End Date> -f <Target Folder>










