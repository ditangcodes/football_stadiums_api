import pandas as pd
from sqlalchemy import create_engine


# Load the CSV data
df = pd.read_csv('../csv_result/stadiums.csv')


# Create an SQLite database
engine = create_engine('sqlite:///stadiums.db')
df.to_sql('stadiums', engine, if_exists='replace', index=False)

print("Data loaded successfully")
