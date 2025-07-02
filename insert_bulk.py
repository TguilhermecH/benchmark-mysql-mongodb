import pandas as pd
import mysql.connector
from time import time
import csv

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abc@123",
    database="imdb"
)
cursor = conn.cursor()

df = pd.read_csv("title.basics.tsv", sep='\t', dtype=str, nrows=10000)
df = df.replace('\\N', None)

start = time()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO title_basics (
            tconst, titleType, primaryTitle, originalTitle,
            isAdult, startYear, endYear, runtimeMinutes, genres
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['tconst'], row['titleType'], row['primaryTitle'], row['originalTitle'],
        row['isAdult'], row['startYear'], row['endYear'], row['runtimeMinutes'], row['genres']
    ))

conn.commit()
end = time()

with open('results.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['MySQL', 'INSERT_TSV_10000', end - start])

cursor.close()
conn.close()
