from db import get_connection
import time
import csv

conn = get_connection()
cursor = conn.cursor()

start = time.time()
cursor.execute("SELECT * FROM title_basics WHERE startYear = 2020 LIMIT 100")
cursor.fetchall()
end = time.time()

with open('results.csv', 'a', newline='') as f:
    csv.writer(f).writerow(['MySQL', 'SELECT_SIMPLE', end - start])

start = time.time()
cursor.execute("""
    SELECT titleType, AVG(runtimeMinutes)
    FROM title_basics
    WHERE runtimeMinutes IS NOT NULL
    GROUP BY titleType
""")
cursor.fetchall()
end = time.time()

with open('results.csv', 'a', newline='') as f:
    csv.writer(f).writerow(['MySQL', 'SELECT_COMPLEX', end - start])

cursor.close()
conn.close()
