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
query = "SELECT OrderID, CustomerID, CustomerMainOffice, PONumber, ContactEmail FROM OrderCustomerPO"
mssql = pd.read_sql(query, conn)

query1 = "SELECT CustomerID, MainOffice, CustomerEmail FROM CustomerMaster"
cus_master = pd.read_sql(query1, conn)

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


# Define the email
email = "brentmbp@q.com"

# Check if the email is present in the specified column
is_present = mysql["email"].isin([email])

# Get the boolean result
result_email = is_present.any()

if result_email:
    po = "BN29d51"
    orderid = 302772

    # Filter the DataFrame to get the rows that satisfy the conditions
    result_row_check = mssql[(mssql['PONumber'] == po) & (mssql['OrderID'] == orderid) & (mssql['ContactEmail'] == email)]

    # Check if any rows satisfy the conditions
    if not result_row_check.empty:
        print("\nThe three conditions are satisfied in the same row.")
    else:
        print("\nNeed Customer ID")

        # Find the rows where the email exists
        row_mssql = mssql[mssql['ContactEmail'] == email]
        row_mysql = mysql[mysql['email'] == email]

        # Check if the email exists in both DataFrames
        if not row_mssql.empty and not row_mysql.empty:
            # Access the data in a different column in the same row
            other_data_mssql = row_mssql['CustomerID'].values[0]
            other_data_mysql = row_mysql['customer_id'].values[0]

            # Compare the values in the different columns
            result_customerid = other_data_mssql == other_data_mysql

            if result_customerid:
                access = row_mysql['access_all_orders'].values[0]
                if access:
                    print("Access Orders")
                else:
                    print("No Access Orders")
            else:
                access_main_office = row_mysql['access_all_orders_main_office'].values[0]
                if access_main_office:
                    # Find the row in cus_master where the email exists
                    row_cus_master = cus_master[cus_master['CustomerEmail'] == email]
                    customerid_cus_master = row_cus_master['CustomerID'].values[0]

                    # Compare the customer ID with the data in MySQL DataFrame
                    result_customerid_main_office = customerid_cus_master == other_data_mysql

                    if result_customerid_main_office:
                        # Access the data in a different column in the same row
                        main_office_value = row_cus_master['MainOffice'].values[0]
                        main_office_access = mssql['CustomerMainOffice'].isin([main_office_value])

                        if main_office_access.any():
                            print("Main Office Access")
                        else:
                            print("Main Office Access Denied")
        else:
            print("Email does not exist in one of the DataFrames")
else:
    print("Email does not exist")


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










