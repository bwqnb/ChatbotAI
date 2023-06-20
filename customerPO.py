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

# Get the unique values from the first column of df1
column1_values = mssql['ContactEmail'].unique()

# Get the unique values from the second column of df2
column2_values = mysql['email'].unique()

# Find the common values between the two columns
common_values = set(column1_values).intersection(column2_values)

# Add a new column 'IsCommon' to indicate if the value is common in df1
mssql['IsCommon'] = mssql['ContactEmail'].isin(common_values)

# Add a new column 'IsCommon' to indicate if the value is common in df2
mysql['IsCommon'] = mysql['email'].isin(common_values)

# Filter the original DataFrames to get the rows where the values are common
df1_common = mssql[mssql['IsCommon']]
df2_common = mysql[mysql['IsCommon']]

# Get the common strings along with their original locations
common_strings_df1 = df1_common[['ContactEmail']]
common_strings_df2 = df2_common[['email']]

# Print the common strings and their original locations
print(common_strings_df1.head())
print(common_strings_df2.head())
 