"""
Coffee E-Commerce Data Cleaning Script
Project: 6-Month Business Analytics (May - October 2025)
Author: Mike Busniak
Description: Data cleaning and preparation for Ukrainian coffee startup analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. LOAD RAW DATA
# ==========================================

def load_raw_data(filepath):
    """
    Load raw e-commerce data from Excel file
    
    Parameters:
    filepath (str): Path to Excel file with raw data
    
    Returns:
    dict: Dictionary containing all sheets as DataFrames
    """
    print("Loading raw data from Excel...")
    
    # Load all sheets
    excel_file = pd.ExcelFile(filepath)
    data = {}
    
    for sheet_name in excel_file.sheet_names:
        data[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"  ✓ Loaded {sheet_name}: {data[sheet_name].shape[0]} rows, {data[sheet_name].shape[1]} columns")
    
    return data


# ==========================================
# 2. CLEAN CUSTOMERS DATA
# ==========================================

def clean_customers_data(df):
    """
    Clean and standardise customer data
    
    Data quality issues addressed:
    - Remove duplicate customer_id entries
    - Standardise channel names
    - Convert registration dates to datetime
    - Handle missing values
    
    Returns:
    pd.DataFrame: Cleaned customers dataframe
    """
    print("\nCleaning customers data...")
    
    df_clean = df.copy()
    initial_rows = len(df_clean)
    
    # 1. Remove duplicates based on customer_id
    df_clean = df_clean.drop_duplicates(subset=['customer_id'], keep='first')
    print(f"  ✓ Removed {initial_rows - len(df_clean)} duplicate customers")
    
    # 2. Standardise channel names
    channel_mapping = {
        'Instagram': 'Instagram',
        'instagram': 'Instagram',
        'Website': 'Website',
        'website': 'Website',
        'Marketplace': 'Marketplace',
        'marketplace': 'Marketplace',
        'Facebook': 'Instagram',  # Group social media
        'Organic': 'Website'
    }
    
    df_clean['channel'] = df_clean['channel'].map(channel_mapping).fillna(df_clean['channel'])
    print(f"  ✓ Standardised channel names: {df_clean['channel'].unique()}")
    
    # 3. Convert registration_date to datetime
    df_clean['registration_date'] = pd.to_datetime(df_clean['registration_date'], errors='coerce')
    
    # 4. Remove customers with missing critical data
    df_clean = df_clean.dropna(subset=['customer_id', 'registration_date'])
    
    # 5. Create customer_segment if not exists (based on first purchase behaviour)
    if 'customer_segment' not in df_clean.columns:
        df_clean['customer_segment'] = 'Standard'
    
    print(f"  ✓ Final customer count: {len(df_clean)}")
    
    return df_clean


# ==========================================
# 3. CLEAN ORDERS DATA
# ==========================================

def clean_orders_data(df):
    """
    Clean and validate orders data
    
    Data quality issues addressed:
    - Remove duplicate order_id entries
    - Validate revenue calculations (revenue = price * quantity)
    - Calculate gross_profit (revenue - cogs)
    - Handle negative or zero values
    - Convert dates to datetime
    - Remove outliers (orders > 50,000 UAH flagged for review)
    
    Returns:
    pd.DataFrame: Cleaned orders dataframe
    """
    print("\nCleaning orders data...")
    
    df_clean = df.copy()
    initial_rows = len(df_clean)
    
    # 1. Remove duplicate orders
    df_clean = df_clean.drop_duplicates(subset=['order_id'], keep='first')
    print(f"  ✓ Removed {initial_rows - len(df_clean)} duplicate orders")
    
    # 2. Convert order_date to datetime
    df_clean['order_date'] = pd.to_datetime(df_clean['order_date'], errors='coerce')
    
    # 3. Remove orders with missing critical data
    df_clean = df_clean.dropna(subset=['order_id', 'customer_id', 'order_date'])
    
    # 4. Validate and clean numeric columns
    numeric_columns = ['quantity', 'price', 'revenue', 'cogs']
    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # 5. Remove orders with invalid values (negative or zero revenue)
    invalid_orders = len(df_clean[(df_clean['revenue'] <= 0) | (df_clean['quantity'] <= 0)])
    df_clean = df_clean[(df_clean['revenue'] > 0) & (df_clean['quantity'] > 0)]
    print(f"  ✓ Removed {invalid_orders} orders with invalid revenue/quantity")
    
    # 6. Calculate gross_profit if not exists
    if 'gross_profit' not in df_clean.columns or df_clean['gross_profit'].isna().any():
        df_clean['gross_profit'] = df_clean['revenue'] - df_clean['cogs']
    
    # 7. Standardise channel names (same as customers)
    channel_mapping = {
        'B2B (Wholesale)': 'B2B (Wholesale)',
        'B2C (E-commerce + Social)': 'B2C (E-commerce + Social)',
        'Service (Inst/repair)': 'Service (Installation/Repair)',
        'Instagram': 'B2C (E-commerce + Social)',
        'Website': 'B2C (E-commerce + Social)',
        'Marketplace': 'B2C (E-commerce + Social)'
    }
    
    if 'channel' in df_clean.columns:
        df_clean['channel'] = df_clean['channel'].map(channel_mapping).fillna(df_clean['channel'])
    
    # 8. Flag potential outliers (for manual review, not removal)
    outliers = len(df_clean[df_clean['revenue'] > 50000])
    if outliers > 0:
        print(f"  ⚠ Warning: {outliers} orders with revenue > 50,000 UAH (flagged for review)")
    
    # 9. Create month column for easier analysis
    df_clean['order_month'] = df_clean['order_date'].dt.to_period('M')
    
    print(f"  ✓ Final order count: {len(df_clean)}")
    
    return df_clean


# ==========================================
# 4. CLEAN PRODUCTS DATA
# ==========================================

def clean_products_data(df):
    """
    Clean and standardise product data
    
    Returns:
    pd.DataFrame: Cleaned products dataframe
    """
    print("\nCleaning products data...")
    
    df_clean = df.copy()
    
    # 1. Remove duplicates
    df_clean = df_clean.drop_duplicates(subset=['product_id'], keep='first')
    
    # 2. Standardise category names
    df_clean['category'] = df_clean['category'].str.strip().str.title()
    
    # 3. Validate numeric fields
    if 'price' in df_clean.columns:
        df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')
    
    print(f"  ✓ Products cleaned: {len(df_clean)} unique products")
    
    return df_clean


# ==========================================
# 5. CLEAN MARKETING DATA
# ==========================================

def clean_marketing_data(df):
    """
    Clean marketing costs and CAC data
    
    Returns:
    pd.DataFrame: Cleaned marketing dataframe
    """
    print("\nCleaning marketing data...")
    
    df_clean = df.copy()
    
    # 1. Convert month to datetime
    if 'month' in df_clean.columns:
        df_clean['month'] = pd.to_datetime(df_clean['month'], errors='coerce')
    
    # 2. Clean numeric columns
    numeric_cols = ['ad_spend', 'cac']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # 3. Remove rows with missing critical data
    df_clean = df_clean.dropna(subset=['channel'])
    
    print(f"  ✓ Marketing data cleaned: {len(df_clean)} rows")
    
    return df_clean


# ==========================================
# 6. DATA VALIDATION
# ==========================================

def validate_data(customers, orders, products):
    """
    Validate data integrity and relationships
    
    Checks:
    - All order customers exist in customers table
    - All order products exist in products table
    - Revenue calculations are correct
    - Date ranges are valid
    """
    print("\nValidating data integrity...")
    
    # 1. Check customer_id integrity
    orders_customers = set(orders['customer_id'].unique())
    customers_ids = set(customers['customer_id'].unique())
    missing_customers = orders_customers - customers_ids
    
    if missing_customers:
        print(f"  ⚠ Warning: {len(missing_customers)} customers in orders not found in customers table")
    else:
        print(f"  ✓ All order customers exist in customers table")
    
    # 2. Check product_id integrity (if products table exists)
    if 'product_id' in orders.columns and not products.empty:
        orders_products = set(orders['product_id'].dropna().unique())
        products_ids = set(products['product_id'].unique())
        missing_products = orders_products - products_ids
        
        if missing_products:
            print(f"  ⚠ Warning: {len(missing_products)} products in orders not found in products table")
        else:
            print(f"  ✓ All order products exist in products table")
    
    # 3. Validate revenue calculations
    revenue_errors = orders[abs(orders['revenue'] - (orders['price'] * orders['quantity'])) > 0.01]
    if len(revenue_errors) > 0:
        print(f"  ⚠ Warning: {len(revenue_errors)} orders have revenue calculation mismatches")
    else:
        print(f"  ✓ Revenue calculations validated")
    
    # 4. Check date ranges
    min_date = orders['order_date'].min()
    max_date = orders['order_date'].max()
    print(f"  ✓ Date range: {min_date.date()} to {max_date.date()}")
    
    # 5. Summary statistics
    print("\nData Summary:")
    print(f"  Total customers: {len(customers)}")
    print(f"  Total orders: {len(orders)}")
    print(f"  Total revenue: {orders['revenue'].sum():,.2f} UAH")
    print(f"  Average order value: {orders['revenue'].mean():,.2f} UAH")
    print(f"  Total products: {len(products)}")


# ==========================================
# 7. EXPORT CLEANED DATA
# ==========================================

def export_cleaned_data(data_dict, output_path='cleaned_data.xlsx'):
    """
    Export all cleaned dataframes to Excel file
    
    Parameters:
    data_dict (dict): Dictionary of cleaned dataframes
    output_path (str): Output file path
    """
    print(f"\nExporting cleaned data to {output_path}...")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"  ✓ Exported {sheet_name}")
    
    print(f"\n✓ All data exported successfully to {output_path}")


# ==========================================
# 8. MAIN EXECUTION
# ==========================================

def main():
    """
    Main data cleaning pipeline
    """
    print("="*60)
    print("COFFEE E-COMMERCE DATA CLEANING PIPELINE")
    print("="*60)
    
    # Configuration
    input_file = 'Coffee_Business_Analytics_(3)_(1).xlsx'
    output_file = 'Coffee_Business_Analytics_CLEANED.xlsx'
    
    # Step 1: Load raw data
    raw_data = load_raw_data(input_file)
    
    # Step 2: Clean each table
    cleaned_data = {}
    
    if 'customers' in raw_data:
        cleaned_data['customers'] = clean_customers_data(raw_data['customers'])
    
    if 'orders' in raw_data:
        cleaned_data['orders'] = clean_orders_data(raw_data['orders'])
    
    if 'products' in raw_data:
        cleaned_data['products'] = clean_products_data(raw_data['products'])
    
    if 'marketing_costs' in raw_data:
        cleaned_data['marketing_costs'] = clean_marketing_data(raw_data['marketing_costs'])
    
    # Step 3: Validate data integrity
    if 'customers' in cleaned_data and 'orders' in cleaned_data:
        products = cleaned_data.get('products', pd.DataFrame())
        validate_data(cleaned_data['customers'], cleaned_data['orders'], products)
    
    # Step 4: Export cleaned data
    export_cleaned_data(cleaned_data, output_file)
    
    print("\n" + "="*60)
    print("DATA CLEANING COMPLETED SUCCESSFULLY")
    print("="*60)
    
    return cleaned_data


if __name__ == "__main__":
    cleaned_data = main()
