import sqlite3
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so

cnx = sqlite3.connect('olist.db')


query = "SELECT * FROM olist_order_customer_dataset;"
df = pd.read_sql_query(query, cnx)
dc_duplicate_1 = df.duplicated().sum()
dc_null = df.isnull().sum()
dc_format = df.value_counts()

aggr_count = df.groupby('customer_city').count()
aggr_sort = aggr_count.sort_values(by=["customer_unique_id"], ascending= False)
aggr_sort_1 = aggr_sort[aggr_sort['customer_id'] >= 1521]
aggr_sort_1 = aggr_sort_1.reset_index()
aggr_sort_1_plot = aggr_sort_1.plot.bar(x='customer_city', y='customer_id', rot=0)

