import sqlite3
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so

#TODO
#cek null masing masing objektif

cnx = sqlite3.connect('olist.db')


query_cstmr = "SELECT * FROM olist_order_customer_dataset;"
query_payment = "SELECT * FROM olist_order_payments_dataset;"
query_status = "SELECT * FROM olist_order_dataset;"


df = pd.read_sql_query(query_cstmr, cnx)
df_payment = pd.read_sql_query(query_payment, cnx)
df_status = pd.read_sql_query(query_status, cnx)

cstmr_count = df.groupby('customer_city').count()
cstmr_sort = cstmr_count.sort_values(by=["customer_unique_id"], ascending= False)
cstmr_sort_1 = cstmr_sort[cstmr_sort['customer_id'] >= 1521]
cstmr_sort_1 = cstmr_sort_1.reset_index()
#cstmr_sort_1_plot = cstmr_sort_1.plot.bar(x='customer_city', y='customer_id', rot=0)

payment_count = df_payment.groupby('payment_type').count()
payment_drop = payment_count.drop(index="not_defined")
payment_sort = payment_drop.sort_values(by=["order_id"], ascending= False)
payment_sort = payment_sort.reset_index()


#payment_plot = payment_sort.plot.bar(x='payment_type', y='order_id', rot=0)
#sns.boxplot(y=df_payment['payment_value'])
df_p_median = df_payment['payment_value'].median()


df_join = df.merge(df_status, on=['customer_id'], how='outer')
df_join_drop = df_join.drop(['customer_zip_code_prefix', 'order_purchase_timestamp',
       'order_approved_at', 'order_delivered_carrier_date',
       'order_delivered_customer_date', 'order_estimated_delivery_date', 
       'order_purchase_timestamp',
       'order_approved_at', 'order_delivered_carrier_date',
       'order_delivered_customer_date', 'order_estimated_delivery_date'], axis=1)
df_join_count = df_join_drop.groupby(['order_status', 'customer_city']).count()
max_counts = df_join_count.groupby('order_status')['customer_id'].max()
max_counts_one = df_join_count.groupby(level=['order_status', 'customer_city'])['customer_id'].max()
selecting = max_counts_one.where(max_counts_one.iloc() == max_counts['customer_id'])

print("Maximum Counts of Orders for Each Order Status:")
print(selecting)


'''
dc_duplicate_1 = df.duplicated().sum()
dc_null = df.isnull().sum()
dc_format = df.value_counts()
'''

'''
for x in df_join_count['customer_id']:
    for y in max_counts['customer_id']:
        if x in y:
            max_counts_list.append(x)    
'''