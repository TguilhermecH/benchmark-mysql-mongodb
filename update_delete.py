from db import get_connection
import time
import csv

conn = get_connection()
cursor = conn.cursor()

start = time.time()
cursor.execute("""
    UPDATE title_basics
    SET runtimeMinutes = 10
    WHERE titleType = 'short' AND runtimeMinutes IS NULL
""")
conn.commit()
end = time.time()
csv.writer(open('results.csv', 'a')).writerow(['MySQL', 'UPDATE', end - start])

start = time.time()
cursor.execute("""
    DELETE FROM title_basics
    WHERE isAdult = 1 AND startYear < 1950
""")
conn.commit()
end = time.time()
csv.writer(open('results.csv', 'a')).writerow(['MySQL', 'DELETE', end - start])

cursor.close()
conn.close()
