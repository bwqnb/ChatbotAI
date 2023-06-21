# imports for SQL data part
import pyodbc
import modin.pandas as pd
from tqdm import tqdm
import dask.dataframe as dd
import pymysql
import ray
import warnings
warnings.filterwarnings("ignore")

ray.init()

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=191.168.0.81;DATABASE=Ariel;UID=interntools;PWD=NtpSqw$9!')
print("Connected")
query = "SELECT OrderID, CustomerID, PONumber, ContactEmail FROM OrderCustomerPO"
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
query2 = "SELECT customer_id, email, access_all_orders FROM users"
mysql = pd.read_sql(query2, conn2)

# Close the database connection
conn2.close()

email = "brentmbp@q.com"

# Check if the string is present in the specified column
is_present = mysql["email"].isin([email])

# Get the boolean answer
result_email = is_present.any()
if result_email:
    po = "BN29d51"
    orderid = 302772
    result_row_check = mssql[(mssql['PONumber'] == po) & (mssql['OrderID'] == orderid) & (mssql['ContactEmail'] == email)]

    # Check if any rows satisfy the conditions
    if not result_row_check.empty:
        print("\nThe three conditions are satisfied in the same row.")
    else:
        print("\nNeed Customer ID")
        # Replace with your specific data point

        # Find the row where the specific data point exists
        row_mssql = mssql[mssql['ContactEmail'] == email]

        # Access the data in a different column in the same row
        other_data_mssql = row_mssql['CustomerID'].values[0]
        row_mysql = mysql[mysql['email'] == email]

        # Access the data in a different column in the same row
        other_data_mysql = row_mysql['customer_id'].values[0]
        result_customerid = other_data_mssql == other_data_mysql

        if result_customerid:
            other_data_mysql = row_mysql['access_all_orders'].values[0]
            if other_data_mysql:
                print("yay")
            else:
                print("need master office")
        else:
            print("Bruh")


else:
    print("Done.")
'''
Customer provides email -> check to see if email exists in users.

No -> Go to registration page and ask visitor to register

Yes -> Ask for PO# or OrderID
Look up PO# or OrderID in OrderCustomerPO
See if OrderCustomerPO.ContactEmail = Email
    Yes -> release information
    No -> If users.customer_id = OrderCustomerPO.CustomerID
                Yes
                    If users.AccessAllOrders = True -> Release information
                    If users.AccessAllOrders = False -> no access
                No
                    If users.AccessAllOrdersMainOffice = True AND users.customer_id <-> CustomerMaster.CustomerID -> CustomerMaster.CustomerMainOffice = OrderCustomerPO.MainOffice
                            Yes -> release information
                            No -> no access
                            '''










