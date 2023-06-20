# imports for SQL data part
import pyodbc
import modin.pandas as pd
from tqdm import tqdm
import dask.dataframe as dd
import pymysql
import ray

ray.init()

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=191.168.0.81;DATABASE=Ariel;UID=interntools;PWD=NtpSqw$9!')
print("Connected")
query = "SELECT OrderID, ContactEmail FROM OrderCustomerPO"
mssql = pd.read_sql(query, conn)

# Close the database connection
conn.close()
#print(mssql)

conn2 = pymysql.connect(
    host='191.168.0.101',
    user='interntools',
    password='NtpSqw$9!',
    database='ariel',
    charset='utf8mb4'  
)
print("Connected")
query2 = "SELECT first_name, email FROM users"
mysql = pd.read_sql(query2, conn2)

# Close the database connection
conn2.close()

# Find the common emails between the two dataframes
common_emails = set(mssql['ContactEmail']).intersection(mysql['email'])

# Filter the original dataframes to get the rows where the emails are common
df1_common = mssql[mssql['ContactEmail'].isin(common_emails)]
df2_common = mysql[mysql['email'].isin(common_emails)]

# Get the index values of the common emails in each dataframe
common_emails_df1_indices = df1_common.index.values
common_emails_df2_indices = df2_common.index.values

# Print the common emails and their indices in each dataframe
print("Common emails in df1:")
for email in common_emails:
    indices = df1_common[df1_common['ContactEmail'] == email].index.values
    print(f"Email: {email}, Indices in df1: {indices}")

print("\nCommon emails in df2:")
for email in common_emails:
    indices = df2_common[df2_common['email'] == email].index.values
    print(f"Email: {email}, Indices in df2: {indices}")

 