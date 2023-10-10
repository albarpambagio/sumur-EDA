import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    """
    A class for performing data analysis on the Olist dataset.

    Args:
        database_path (str): The path to the SQLite database file containing the dataset.
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
    
    def clean_data(self, df):
        """
        Clean and analyze the given DataFrame.

        Args:
        df (pd.DataFrame): The DataFrame to be cleaned and analyzed.

        Returns:
        int: The number of duplicate rows.
        pd.Series: A Series containing the count of missing values for each column.
        pd.Series: A Series containing value counts for each unique row.
        """
        duplicate_count = df.duplicated().sum()
        null_count = df.isnull().sum()
        value_counts = df.value_counts()
        return duplicate_count, null_count, value_counts

    
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
        '''
        sns.set_style("whitegrid")

        # Create a bar chart with custom styling
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x='customer_city', y='customer_id', data=popular_cities, palette="Blues_d")
        ax.set(xlabel='Customer City', ylabel='Number of Customers')
        plt.title('Popular Customer Cities', fontsize=16)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(fontsize=12)

        # Add data labels to the bars
        for p in ax.patches:
            ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=12, color='black')
        
        # Remove the top and right spines
        sns.despine()
        '''

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

        """
        # Create a pie chart 
        plt.figure(figsize=(8, 8))
        colors = sns.color_palette('Blues_d')
        explode = (0.1, 0.1, 0.1, 0.1)  # Explode a slice for emphasis (adjust as needed)

        
        # Create the pie chart
        plt.pie(
            sorted_payment_types['order_id'],
            labels=sorted_payment_types['payment_type'],
            autopct='%1.1f%%',
            colors=colors,
            startangle=140,
            pctdistance=0.85,  # Distance of percentage labels from the center
            explode=explode,
        )

        # Draw a circle in the center to make it look like a donut chart (optional)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        # Equal aspect ratio ensures that pie is drawn as a circle
        plt.axis('equal')
        plt.title('Payment Type Distribution', fontsize=16)

        # Add a legend (optional, set legend=False to remove it)
        plt.legend(sorted_payment_types['payment_type'], title='Payment Type', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Add a shadow to the pie chart (optional)
        plt.gca().set_aspect('equal')
        plt.tight_layout()
        """
        
        return sorted_payment_types

    def payment_value_median(self):
        """
        Calculate and return the median of payment values.

        Returns:
            float: The median payment value.
        """
        payment_value_median = self.payment_data['payment_value'].median()

        '''
        sns.set_style("whitegrid")

        # Create a box plot with custom styling
        plt.figure(figsize=(8, 6))
        ax = sns.boxplot(y=self.payment_data['payment_value'], color='royalblue')
        ax.set(xlabel='Payment Value', ylabel='')
        plt.title('Box Plot of Payment Value', fontsize=16)

        # Customize the x-axis and y-axis labels
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        # Remove the top and right spines
        sns.despine()
        '''

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

        '''
        # Sample data based on order_status_customer_city_analysis results
        order_status = ['delivered', 'shipped', 'canceled', 'unavailable', 'invoiced', 'processing', 'approved', 'created']
        counts = [15045, 170, 140, 109, 52, 52, 1, 1]

        # Create a bar chart with sorted data
        sorted_order_status, sorted_counts = zip(*sorted(zip(order_status, counts), key=lambda x: x[1], reverse=True))
        
        sns.set_style("whitegrid")

        # Create a bar chart with custom styling
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=sorted_order_status, y=sorted_counts, color='royalblue')
        ax.set(xlabel='Order Status', ylabel='Count')
        plt.title('Order Status Distribution (Sorted)', fontsize=16)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(fontsize=12)

        # Display the count values on top of the bars
        for i, count in enumerate(sorted_counts):
            ax.annotate(f"{count}", (i, count + 50), ha='center', va='bottom', fontsize=12, color='black')

        # Remove the top and right spines
        sns.despine()

        # Show the plot
        plt.tight_layout()
        '''
        
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
        
        # Sort the DataFrame by 'seller_id' in ascending order
        popular_seller_cities = popular_seller_cities.sort_values(by='seller_id', ascending=False)
        
        # Color palette
        royal_blue = "#4169E1"

        # Create a bar plot 
        sns.set_style("whitegrid")
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=popular_seller_cities, x='seller_city', y='seller_id', color=royal_blue)
        plt.xlabel('Seller City', fontsize=14)
        plt.ylabel('Number of Sellers', fontsize=14)
        plt.title('Popular Seller Cities', fontsize=16, fontweight='medium')  

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=12)
        
        # Display count values on top of the bars
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=12, color='black', fontweight='medium')

        # Add a border to the plot
        sns.despine()
        
        plt.tight_layout()
        plt.show()
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

# Clean and analyze a DataFrame
#duplicate_count, null_count, value_counts = data_analyzer.clean_data()

'''
# Print the results
print("Duplicate Count:", duplicate_count)
print("Null Count per Column:")
print(null_count)
print("Value Counts:")
print(value_counts)
'''