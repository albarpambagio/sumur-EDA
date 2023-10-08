import sqlite3
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so


cnx = sqlite3.connect('olist.db')

query_cstmr = "SELECT * FROM olist_order_customer_dataset;"
query_payment = "SELECT * FROM olist_order_payments_dataset;"
query_status = "SELECT * FROM olist_order_dataset;"
query_seller = "SELECT * FROM olist_sellers_dataset;"

df = pd.read_sql_query(query_cstmr, cnx)
df_payment = pd.read_sql_query(query_payment, cnx)
df_status = pd.read_sql_query(query_status, cnx)
df_seller = pd.read_sql_query(query_seller, cnx)


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


#sns.boxplot(y=df_payment['payment_value']) #outliers detection
df_p_median = df_payment['payment_value'].median()


df_join = df.merge(df_status, on=['customer_id'], how='outer')
df_join_drop = df_join.drop(['customer_zip_code_prefix', 'order_purchase_timestamp',
       'order_approved_at', 'order_delivered_carrier_date',
       'order_delivered_customer_date', 'order_estimated_delivery_date', 
       'order_purchase_timestamp',
       'order_approved_at', 'order_delivered_carrier_date',
       'order_delivered_customer_date', 'order_estimated_delivery_date'], axis=1)


df_join_count = df_join_drop.groupby(['order_status', 'customer_city']).count()
#max_counts = df_join_count.groupby('order_status')['customer_id'].max()
max_counts_1 = df_join_count.reset_index(level="customer_city")
max_counts_count = max_counts_1.value_counts(subset='customer_city')
max_counts_max = max_counts_1.groupby('order_status').max()
#needs viz

seller_count = df_seller.groupby('seller_city').count()
seller_count_sort = seller_count.sort_values(by=["seller_id"], ascending= False)
seller_count_filter = seller_count_sort[seller_count_sort['seller_id'] >= 52]
seller_count_reset = seller_count_filter.reset_index()
seller_count_plot = seller_count_reset.plot.bar(x='seller_city', y='seller_id', rot=0)

print(max_counts_max)


'''
Data cleansing

dc_duplicate_1 = df.duplicated().sum()
dc_null = df.isnull().sum()
dc_format = df.value_counts() #for unstandardized format
'''

