from data_analysis_one_organized import DataAnalysis


def main():
    # Specify the path to your SQLite database
    database_path = 'olist.db'

    # Create an instance of the DataAnalysis class
    data_analyzer = DataAnalysis(database_path)

    # Load the data from the database
    data_analyzer.load_data()

    # Perform customer city analysis
    popular_customer_cities = data_analyzer.customer_city_analysis()
    print("Customer City Analysis:")
    print(popular_customer_cities)

    # Perform payment type analysis
    sorted_payment_types = data_analyzer.payment_type_analysis()
    print("\nPayment Type Analysis:")
    print(sorted_payment_types)

    # Calculate payment value median
    payment_value_median = data_analyzer.payment_value_median()
    print("\nPayment Value Median:")
    print(payment_value_median)

    # Perform order status customer city analysis
    max_counts_per_status = data_analyzer.order_status_customer_city_analysis()
    print("\nOrder Status & Customer City Analysis:")
    print(max_counts_per_status)

    # Perform seller city analysis
    popular_seller_cities = data_analyzer.seller_city_analysis()
    print("\nSeller City Analysis:")
    print(popular_seller_cities)



if __name__ == "__main__":
    main()


