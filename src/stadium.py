import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_stadium_data():
    url = "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"
    tables = pd.read_html(url, match='Football stadiums by capacity')

    if not tables:
        print("No tables found")
        return pd.DataFrame()

    # Assuming the first table is the one we need
    df = tables[0]

    # Rename columns for clarity
    df.columns = ['Rank', 'Stadium', 'Seating Capacity', 'Region', 'Country', 'City', 'Image', 'Home Teams']

    # Drop the 'Image' column as it's not needed
    df = df.drop(columns=['Image'])

    return df

df = fetch_stadium_data()
if not df.empty:
    df.to_csv('../csv_result/stadiums.csv', index=False)
    print("Data saved successfully")
else:
    print("No data to save")
