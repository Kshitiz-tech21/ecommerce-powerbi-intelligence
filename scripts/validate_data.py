import pandas as pd
import numpy as np
import os

def validate_data():
    print("Starting Data Validation Report...\n")
    path = "C:/Users/hp/AppData/Local/Temp/opencode/ecommerce-powerbi-intelligence/data/processed"
    
    try:
        df_sales = pd.read_csv(f"{path}/Fact_Sales.csv")
        df_customer = pd.read_csv(f"{path}/Dim_Customer.csv")
        df_product = pd.read_csv(f"{path}/Dim_Product.csv")
        df_region = pd.read_csv(f"{path}/Dim_Region.csv")
        df_channel = pd.read_csv(f"{path}/Dim_Channel.csv")
        df_targets = pd.read_csv(f"{path}/Fact_Targets.csv")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    checks = {}
    
    # 1. PKs
    checks["Dim_Customer Primary Key"] = df_customer['Customer_ID'].is_unique
    checks["Dim_Product Primary Key"] = df_product['Product_ID'].is_unique
    checks["Dim_Region Primary Key"] = df_region['Region_ID'].is_unique
    checks["Dim_Channel Primary Key"] = df_channel['Channel_ID'].is_unique
    checks["Fact_Sales Composite Key (Line ID)"] = df_sales['Order_Line_ID'].is_unique

    # 2. Logic (Using tolerances for float precision)
    checks["No Negative Quantities"] = (df_sales['Quantity'] > 0).all()
    
    # Net Revenue = Gross - Discount
    net_calc = df_sales['Gross_Revenue'] - df_sales['Discount_Amount']
    checks["Revenue Calculation Consistency"] = np.allclose(df_sales['Net_Revenue'], net_calc, atol=0.01)
    
    # Profit = Net Revenue - Total Cost
    profit_calc = df_sales['Net_Revenue'] - df_sales['Total_Cost']
    checks["Profit Calculation Consistency"] = np.allclose(df_sales['Profit'], profit_calc, atol=0.01)
    
    checks["Discount Range Validity"] = ((df_sales['Discount_Pct'] >= 0) & (df_sales['Discount_Pct'] <= 0.5)).all()

    # 3. FKs
    checks["Customer FK Integrity"] = df_sales['Customer_ID'].isin(df_customer['Customer_ID']).all()
    checks["Product FK Integrity"] = df_sales['Product_ID'].isin(df_product['Product_ID']).all()
    checks["Region FK Integrity"] = df_sales['Region_ID'].isin(df_region['Region_ID']).all()
    checks["Channel FK Integrity"] = df_sales['Channel_ID'].isin(df_channel['Channel_ID']).all()

    print(f"{'Check':<40} | {'Status':<10}")
    print("-" * 52)
    for check, status in checks.items():
        status_str = "PASS" if status else "FAIL"
        print(f"{check:<40} | {status_str:<10}")

if __name__ == "__main__":
    validate_data()
