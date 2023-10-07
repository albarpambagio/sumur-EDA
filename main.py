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

#cek null masing masing objektif
df_join = df.merge(df_status, on=['customer_id'], how='outer')
dc_duplicate_1 = df_join.isnull().sum()
print(dc_duplicate_1)


'''
dc_duplicate_1 = df.duplicated().sum()
dc_null = df.isnull().sum()
dc_format = df.value_counts()
'''

