# imports for SQL data part
import pandas as pd
from tqdm import tqdm
import pymysql

conn = pymysql.connect(
    host='191.168.0.101',
    user='interntools',
    password='NtpSqw$9!',
    database='ariel',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

print("Connected")
query = "SELECT email FROM users"
print("Loading Data...")
df = pd.read_sql_query(query, conn)

loop = tqdm(total = len(df.index), position = 0, leave = False)
for k in range(int(len(df.index)/2)):
    loop.set_description("Loading...".format(k))
    loop.update(2)


loop.close()
conn.close()
print("Data Loaded")

# Check if the values match in the same row
specific_string = "bill@bells.com"

# Check if the specific string is present in the column
is_present = df['email'].str.contains(specific_string, case=False)
matching_rows = df[is_present]

if not matching_rows.empty:
    print("Valid Email")
    print(matching_rows)
else:
    print("Invalid Email")

