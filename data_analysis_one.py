import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    """
    A class for performing data analysis on Olist dataset.
    
    Args:
        database_path (str): The path to the SQLite database file containing the dataset.

    Methods:
        fetch_data(query):
            Fetch data from the database using a SQL query.

        load_data():
            Load customer, payment, order, and seller data from the database.

        customer_city_analysis():
            Analyze and return popular customer cities based on customer counts.

        payment_type_analysis():
            Analyze and return payment type distribution.

        payment_value_median():
            Calculate and return the median of payment values.

        order_status_customer_city_analysis():
            Analyze and return the maximum order counts per status for each customer city.

        seller_city_analysis():
            Analyze and return popular seller cities based on seller counts.
    """
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def fetch_data(self, query):
        """
        Fetch data from the database using a SQL query.

        Args:
            query (str): SQL query to fetch data.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing the fetched data.
        """
        return pd.read_sql_query(query, self.connection)

    def load_data(self):
        """
        Load customer, payment, order, and seller data from the database.
        """
        query_customer = "SELECT * FROM olist_order_customer_dataset;"
        query_payment = "SELECT * FROM olist_order_payments_dataset;"
        query_order = "SELECT * FROM olist_order_dataset;"
        query_seller = "SELECT * FROM olist_sellers_dataset;"

        self.customer_data = self.fetch_data(query_customer)
        self.payment_data = self.fetch_data(query_payment)
        self.order_data = self.fetch_data(query_order)
        self.seller_data = self.fetch_data(query_seller)

    def customer_city_analysis(self):
        """
        Analyze and return popular customer cities based on customer counts.

        Returns:
            pd.DataFrame: A DataFrame with popular customer cities and their counts.
        """
        customer_city_counts = self.customer_data.groupby('customer_city').count()
        sorted_customer_cities = customer_city_counts.sort_values(by=["customer_unique_id"], ascending=False)
        popular_cities = sorted_customer_cities[sorted_customer_cities['customer_id'] >= 1521]
        popular_cities = popular_cities.reset_index()
        
        # Create a bar chart using 
        plt.figure(figsize=(12, 6))
        plt.bar(popular_cities['customer_city'], popular_cities['customer_id'])
        plt.xlabel('Customer City')
        plt.ylabel('Number of Customers')
        plt.title('Popular Customer Cities')

        # Rotate x-axis labels for better readability (optional)
        plt.xticks(rotation=45, ha='right')

        # Show the bar chart
        #plt.tight_layout()
        #plt.show()
        
        return popular_cities

    def payment_type_analysis(self):
        """
        Analyze and return payment type distribution.

        Returns:
            pd.DataFrame: A DataFrame with payment types and their counts.
        """
        payment_type_counts = self.payment_data.groupby('payment_type').count()
        valid_payment_types = payment_type_counts.drop(index="not_defined")
        sorted_payment_types = valid_payment_types.sort_values(by=["order_id"], ascending=False)
        sorted_payment_types = sorted_payment_types.reset_index()
        
        # Create a pie chart 
        sorted_payment_types.plot.pie(
            y='order_id',
            labels=sorted_payment_types['payment_type'],
            autopct='%1.1f%%',
            figsize=(8, 8),
            title='Payment Type Distribution',
            legend=False
        )

        # Show the pie chart
        #plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        #plt.show()
        
        return sorted_payment_types

    def payment_value_median(self):
        """
        Calculate and return the median of payment values.

        Returns:
            float: The median payment value.
        """
        payment_value_median = self.payment_data['payment_value'].median()
        plt.figure(figsize=(8, 6))
        sns.boxplot(y=self.payment_data['payment_value'])
        plt.xlabel('Payment Value')
        plt.title('Box Plot of Payment Value')
        
        plt.show()
        return payment_value_median

    def order_status_customer_city_analysis(self):
        """
        Analyze and return the maximum order counts per status for each customer city.

        Returns:
            pd.DataFrame: A DataFrame with maximum order counts per status for each customer city.
        """
        merged_data = self.customer_data.merge(self.order_data, on=['customer_id'], how='outer')
        data_without_unused_columns = merged_data.drop([
            'customer_zip_code_prefix', 'order_purchase_timestamp',
            'order_approved_at', 'order_delivered_carrier_date',
            'order_delivered_customer_date', 'order_estimated_delivery_date',
            'order_purchase_timestamp',
            'order_approved_at', 'order_delivered_carrier_date',
            'order_delivered_customer_date', 'order_estimated_delivery_date'
        ], axis=1)

        status_and_city_counts = data_without_unused_columns.groupby(['order_status', 'customer_city']).count()
        max_counts_per_city = status_and_city_counts.reset_index(level="customer_city")
        max_counts_per_status = max_counts_per_city.groupby('order_status').max()
        
        # Sample data based on your order_status_customer_city_analysis results
        order_status = ['delivered', 'shipped', 'canceled', 'unavailable', 'invoiced', 'processing', 'approved', 'created']
        counts = [15045, 170, 140, 109, 52, 52, 1, 1]

        # Create a bar chart with sorted data
        sorted_order_status, sorted_counts = zip(*sorted(zip(order_status, counts), key=lambda x: x[1], reverse=True))

        plt.figure(figsize=(10, 6))
        plt.bar(sorted_order_status, sorted_counts, color='royalblue')
        plt.xlabel('Order Status')
        plt.ylabel('Count')
        plt.title('Order Status Distribution (Sorted)')
        plt.xticks(rotation=45, ha='right')

        # Display the count values on top of the bars
        for i, count in enumerate(sorted_counts):
            plt.text(i, count + 50, str(count), ha='center', va='bottom')

        plt.tight_layout()
        plt.show()

        return max_counts_per_status

    def seller_city_analysis(self):
        """
        Analyze and return popular seller cities based on seller counts.

        Returns:
            pd.DataFrame: A DataFrame with popular seller cities and their counts.
        """
        seller_city_counts = self.seller_data.groupby('seller_city').count()
        popular_seller_cities = seller_city_counts[seller_city_counts['seller_id'] >= 52]
        popular_seller_cities = popular_seller_cities.reset_index()
        return popular_seller_cities

# Create an instance of the DataAnalysis class and load data
database_path = 'olist.db'
data_analyzer = DataAnalysis(database_path)
data_analyzer.load_data()

# Perform customer city analysis
popular_customer_cities = data_analyzer.customer_city_analysis()

# Perform payment type analysis
sorted_payment_types = data_analyzer.payment_type_analysis()

# Calculate payment value median
payment_value_median = data_analyzer.payment_value_median()

# Perform order status customer city analysis
max_counts_per_status = data_analyzer.order_status_customer_city_analysis()

# Perform seller city analysis
popular_seller_cities = data_analyzer.seller_city_analysis()
