import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

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

    return df_extract

df = fetch_stadium_data()
if not df.empty:
    df.to_csv('../csv_result/stadiums.csv', index=False)
    print("Data saved successfully")
else:
    print("No data to save")
