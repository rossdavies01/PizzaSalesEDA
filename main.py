'''
Created on Mar 5, 2024

@author: Ross
'''
#Imports
import pandas as pd
import pyodbc


#Import CSV
data = pd.read_csv (r'C:\Users\Ross\Desktop\pizza_sales.csv')   
df = pd.DataFrame(data)

#Check for missing values
print(df.isna().sum())

#Standardize date format to USA datetime
df['order_date'] = df['order_date'].str.replace('-','/')
print(df.order_date)
df['order_date'] = pd.to_datetime(df['order_date'] + ' ' + df['order_time'], dayfirst='True')
print(df.order_date)
# df['order_date'] = df['order_date'].dt.strftime('%m/%d/%Y %H:%M:%S')
# print(df.order_date)

#Connect to SQL Server and truncate table
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DA-ROSS-MACHINE\SQLEXPRESS;'
                      'Database=pizzasales;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
sql = "truncate table pizzasales_rpt"
cursor.execute(sql)
cursor.commit()

#Create Table
# cursor.execute('''
#      CREATE TABLE [dbo].[pizzasales_new](
#      [pizza_id] [bigint] NOT NULL,
#      [order_id] [smallint] NULL,
#      [pizza_name_id] [varchar](100) NULL,
#      [quantity] [smallint] NULL,
#      [order_date] [date] NULL,
#      [order_time] [time](7) NULL,
#      [unit_price] [numeric](18, 2) NULL,
#      [total_price] [numeric](18, 2) NULL,
#      [pizza_size] [varchar](3) NULL,
#      [pizza_category] [varchar](10) NULL,
#      [pizza_ingredients] [varchar](200) NULL,
#      [pizza_name] [varchar](200) NULL
#      ) ON [PRIMARY]
#         ''')

#Insert DataFrame into Table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO dbo.pizzasales_rpt (pizza_id, order_id, pizza_name_id, quantity, order_date, order_time, unit_price, total_price, pizza_size, pizza_category, pizza_ingredients, pizza_name)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                ''',
                row.pizza_id, 
                row.order_id,
                row.pizza_name_id,
                row.quantity,
                row.order_date,
                row.order_time,
                row.unit_price,
                row.total_price,
                row.pizza_size,
                row.pizza_category,
                row.pizza_ingredients,
                row.pizza_name
                )
    conn.commit()
