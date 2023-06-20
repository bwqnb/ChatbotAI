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
print(mysql)

email = "brandyloo@arielpremium.com"

# Check if the string is present in the specified column
is_present = mysql["email"].isin([email])

# Get the boolean answer
result = is_present.any()










