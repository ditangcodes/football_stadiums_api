import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import geohash

# Web Scrapping the Football stadium data on Wikipedia
def fetch_stadium_data():
    url = "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"
    tables = pd.read_html(url)

    if not tables:
        print("No tables found")
        return pd.DataFrame()

    # Getting the 3rd table as this is the data we want to web scrape using pandas
    df = tables[2]
    
    # Extract columns 
    df_extract = df[['Stadium', 'Seating capacity', 'Region', 'Country', 'City', 'Images', 'Home team(s)']]

    #Rename columns for clarity
    df_extract.columns = ['Stadium', 'Seating Capacity', 'Region', 'Country', 'City', 'Image', 'Home Teams']
    df_extract['Stadium']= df_extract['Stadium'].str.strip('♦')
    
    # Function to clean the Seating Capacity column
    def clean_seating_capacity(value):
    # Remove square brackets and the numbers inside them
        value = re.sub(r'\[\d+\]', '', value)
        # Remove commas
        value = value.replace(',', '')
        return value
    df_extract['Seating Capacity'] = df_extract['Seating Capacity'].apply(clean_seating_capacity)
    print(df_extract)

    # Initialize geolocator
    geolocator = Nominatim(user_agent="stadium_locator")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    # Function to get latitude and longitude
    def get_coordinates(city, country):
        try:
            location = geocode(f"{city}, {country}")
            return location.latitude, location.longitude
        except:
            return None, None
    # Apply the function to get coordinates
    df_extract['Latitude'], df_extract['Longitude'] = zip(*df_extract.apply(lambda row: get_coordinates(row['City'], row['Country']), axis=1))
    # Drop rows with missing coordinates
    df_extract = df_extract.dropna(subset=['Latitude', 'Longitude'])

    # Function to get geohash
    def get_geohash(lat, lon):
        return geohash.encode(lat, lon)
    
    # Apply the function to get geohash
    df_extract['Geohash'] = df_extract.apply(lambda row: get_geohash(row['Latitude'], row['Longitude']), axis=1)

    print(df_extract)   
    return df_extract

df = fetch_stadium_data()
if not df.empty:
    df.to_csv('../csv_result/stadiums.csv', index=False)
    print("Data saved successfully")
else:
    print("No data to save")
