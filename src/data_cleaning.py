import pandas as pd
import numpy as np


class DataCleaner:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.file_path)

    def clean_data(self):

        df = self.df

        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]

        # Clean column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Convert datatypes
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce')
        df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
        df['profit'] = pd.to_numeric(df['profit'], errors='coerce')
        df['postal_code'] = df['postal_code'].astype(str)

        # Remove missing
        df.dropna(subset=['order_date', 'ship_date', 'sales', 'profit'], inplace=True)

        # Feature Engineering
        df['year_month'] = df['order_date'].dt.to_period('M')
        df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days

        # Remove invalid shipping
        df = df[df['shipping_days'] >= 0]

        # Remove extreme outliers
        df = df[df['sales'] <= df['sales'].quantile(0.99)]

        # Sort by time
        df = df.sort_values(by='order_date').reset_index(drop=True)

        self.df = df
        return df
