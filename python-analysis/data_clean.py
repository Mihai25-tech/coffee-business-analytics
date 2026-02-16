# Coffee shop data cleaning script
# Used this to clean 6 months of messy e-commerce data
# Mike B. - Feb 2026

import pandas as pd
import numpy as np
from datetime import datetime

# Suppress warnings - they were annoying
import warnings
warnings.filterwarnings('ignore')

def load_data(file_path):
    """Load Excel with all sheets"""
    print("Loading data...")
    excel = pd.ExcelFile(file_path)
    
    data = {}
    for sheet in excel.sheet_names:
        data[sheet] = pd.read_excel(excel, sheet_name=sheet)
        print(f"Loaded {sheet}: {len(data[sheet])} rows")
    
    return data

def clean_customers(df):
    """
    Clean customer data
    Main issues I found:
    - Duplicate customer IDs
    - Channel names inconsistent (instagram vs Instagram vs facebook)
    - Some missing registration dates
    """
    print("\nCleaning customers...")
    initial = len(df)
    
    # Drop dupes
    df = df.drop_duplicates(subset=['customer_id'], keep='first')
    print(f"Removed {initial - len(df)} duplicates")
    
    # Fix channel names - they were all over the place
    # Decided to group social media as Instagram since that was main channel
    channels = {
        'instagram': 'Instagram',
        'Instagram': 'Instagram',
        'facebook': 'Instagram',
        'Facebook': 'Instagram',
        'website': 'Website',
        'Website': 'Website',
        'marketplace': 'Marketplace',
        'Marketplace': 'Marketplace',
    }
    
    df['channel'] = df['channel'].map(channels).fillna(df['channel'])
    
    # Convert dates
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    
    # Remove rows with missing critical stuff
    df = df.dropna(subset=['customer_id', 'registration_date'])
    
    # Add segment if it doesn't exist
    if 'customer_segment' not in df.columns:
        df['customer_segment'] = 'Standard'
    
    print(f"Final: {len(df)} customers")
    return df

def clean_orders(df):
    """
    Clean order data
    Issues found:
    - Duplicates
    - Some negative revenues (data entry errors?)
    - Inconsistent channel names again
    - Revenue didn't always match price * quantity
    """
    print("\nCleaning orders...")
    initial = len(df)
    
    # Drop dupes
    df = df.drop_duplicates(subset=['order_id'], keep='first')
    
    # Fix dates
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    
    # Remove missing data
    df = df.dropna(subset=['order_id', 'customer_id', 'order_date'])
    
    # Convert numbers - some were stored as text for some reason
    for col in ['quantity', 'price', 'revenue', 'cogs']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove invalid orders (negative revenue, zero quantity, etc)
    bad_orders = len(df[(df['revenue'] <= 0) | (df['quantity'] <= 0)])
    df = df[(df['revenue'] > 0) & (df['quantity'] > 0)]
    print(f"Removed {bad_orders} invalid orders")
    
    # Calculate gross profit
    # Some rows had it, some didn't - just recalc for all
    df['gross_profit'] = df['revenue'] - df['cogs']
    
    # Fix channel names
    # Orders use different channel categories than customers
    channel_fix = {
        'B2B (Wholesale)': 'B2B (Wholesale)',
        'B2C (E-commerce + Social)': 'B2C (E-commerce + Social)',
        'Service (Inst/repair)': 'Service (Installation/Repair)',
        'Instagram': 'B2C (E-commerce + Social)',
        'Website': 'B2C (E-commerce + Social)',
        'Marketplace': 'B2C (E-commerce + Social)'
    }
    
    if 'channel' in df.columns:
        df['channel'] = df['channel'].map(channel_fix).fillna(df['channel'])
    
    # Flag really big orders - might be data errors
    big_orders = len(df[df['revenue'] > 50000])
    if big_orders > 0:
        print(f"WARNING: {big_orders} orders over 50K UAH - double check these")
    
    # Add month for easier grouping later
    df['order_month'] = df['order_date'].dt.to_period('M')
    
    print(f"Final: {len(df)} orders")
    return df

def clean_products(df):
    """Quick product cleanup"""
    print("\nCleaning products...")
    
    # Remove dupes
    df = df.drop_duplicates(subset=['product_id'], keep='first')
    
    # Standardise category names
    df['category'] = df['category'].str.strip().str.title()
    
    # Fix prices
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    print(f"Products: {len(df)}")
    return df

def clean_marketing(df):
    """Clean marketing spend data"""
    print("\nCleaning marketing...")
    
    # Fix dates
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')
    
    # Fix numbers
    for col in ['ad_spend', 'cac']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove missing channels
    df = df.dropna(subset=['channel'])
    
    print(f"Marketing: {len(df)} rows")
    return df

def check_data(customers, orders, products):
    """
    Quick sanity checks
    Make sure everything links up properly
    """
    print("\nData checks...")
    
    # Check if all order customers exist
    order_custs = set(orders['customer_id'].unique())
    cust_ids = set(customers['customer_id'].unique())
    missing = order_custs - cust_ids
    
    if missing:
        print(f"WARNING: {len(missing)} customers in orders but not in customer table")
    else:
        print("✓ All order customers exist")
    
    # Check products if table exists
    if 'product_id' in orders.columns and not products.empty:
        order_prods = set(orders['product_id'].dropna().unique())
        prod_ids = set(products['product_id'].unique())
        missing = order_prods - prod_ids
        
        if missing:
            print(f"WARNING: {len(missing)} products missing")
        else:
            print("✓ All products exist")
    
    # Check revenue calculations
    # Allow small rounding errors (0.01 UAH)
    wrong_revenue = orders[abs(orders['revenue'] - (orders['price'] * orders['quantity'])) > 0.01]
    if len(wrong_revenue) > 0:
        print(f"WARNING: {len(wrong_revenue)} orders have wrong revenue calc")
    else:
        print("✓ Revenue calculations correct")
    
    # Date range
    print(f"Date range: {orders['order_date'].min().date()} to {orders['order_date'].max().date()}")
    
    # Summary
    print(f"\nSummary:")
    print(f"  Customers: {len(customers)}")
    print(f"  Orders: {len(orders)}")
    print(f"  Revenue: {orders['revenue'].sum():,.0f} UAH")
    print(f"  Avg order: {orders['revenue'].mean():,.0f} UAH")

def save_data(data_dict, output='cleaned_data.xlsx'):
    """Save everything to Excel"""
    print(f"\nSaving to {output}...")
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for name, df in data_dict.items():
            df.to_excel(writer, sheet_name=name, index=False)
            print(f"Saved {name}")
    
    print("Done!")

# Main script
if __name__ == "__main__":
    print("="*50)
    print("Coffee Shop Data Cleaning")
    print("="*50)
    
    # Load everything
    input_file = 'Coffee_Business_Analytics_(3)_(1).xlsx'
    raw = load_data(input_file)
    
    # Clean each table
    cleaned = {}
    
    if 'customers' in raw:
        cleaned['customers'] = clean_customers(raw['customers'])
    
    if 'orders' in raw:
        cleaned['orders'] = clean_orders(raw['orders'])
    
    if 'products' in raw:
        cleaned['products'] = clean_products(raw['products'])
    
    if 'marketing_costs' in raw:
        cleaned['marketing_costs'] = clean_marketing(raw['marketing_costs'])
    
    # Validation
    if 'customers' in cleaned and 'orders' in cleaned:
        products = cleaned.get('products', pd.DataFrame())
        check_data(cleaned['customers'], cleaned['orders'], products)
    
    # Save
    save_data(cleaned, 'Coffee_Business_Analytics_CLEANED.xlsx')
    
    print("\n" + "="*50)
    print("All done!")
    print("="*50)
