import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

def generate_ecommerce_data():
    print("Generating synthetic e-commerce dataset...")
    
    # 1. DIM_REGION
    regions_data = [
        {"Region_ID": 1, "Region": "North", "State": "Delhi", "City": "Delhi NCR"},
        {"Region_ID": 2, "Region": "North", "State": "Rajasthan", "City": "Jaipur"},
        {"Region_ID": 3, "Region": "North", "State": "Uttar Pradesh", "City": "Lucknow"},
        {"Region_ID": 4, "Region": "West", "State": "Maharashtra", "City": "Mumbai"},
        {"Region_ID": 5, "Region": "West", "State": "Maharashtra", "City": "Pune"},
        {"Region_ID": 6, "Region": "West", "State": "Gujarat", "City": "Ahmedabad"},
        {"Region_ID": 7, "Region": "South", "State": "Karnataka", "City": "Bengaluru"},
        {"Region_ID": 8, "Region": "South", "State": "Telangana", "City": "Hyderabad"},
        {"Region_ID": 9, "Region": "South", "State": "Tamil Nadu", "City": "Chennai"},
        {"Region_ID": 10, "Region": "East", "State": "West Bengal", "City": "Kolkata"},
        {"Region_ID": 11, "Region": "East", "State": "Bihar", "City": "Patna"},
        {"Region_ID": 12, "Region": "Central", "State": "Madhya Pradesh", "City": "Indore"},
    ]
    df_region = pd.DataFrame(regions_data)

    # 2. DIM_CHANNEL
    channels_data = [
        {"Channel_ID": 1, "Channel": "Website"},
        {"Channel_ID": 2, "Channel": "Mobile App"},
        {"Channel_ID": 3, "Channel": "Marketplace"},
        {"Channel_ID": 4, "Channel": "Social Commerce"},
    ]
    df_channel = pd.DataFrame(channels_data)

    # 3. DIM_PRODUCT
    categories = {
        "Electronics": ["Smartphones", "Laptops", "Accessories", "Audio"],
        "Fashion": ["Men's Wear", "Women's Wear", "Footwear", "Accessories"],
        "Home & Kitchen": ["Appliances", "Furniture", "Decor", "Cookware"],
        "Beauty": ["Skincare", "Makeup", "Haircare", "Fragrance"],
        "Sports": ["Equipment", "Apparel", "Footwear", "Fitness"],
        "Books": ["Fiction", "Non-Fiction", "Educational", "Comics"],
        "Accessories": ["Watches", "Jewelry", "Bags", "Wallets"]
    }
    
    products = []
    prod_id = 1
    for cat, subcats in categories.items():
        for subcat in subcats:
            for i in range(1, 11):
                base_price = np.random.uniform(500, 50000)
                margin_roll = random.random()
                if margin_roll > 0.8:
                    margin = np.random.uniform(0.4, 0.6)
                    band = "High"
                elif margin_roll > 0.3:
                    margin = np.random.uniform(0.2, 0.4)
                    band = "Mid"
                else:
                    margin = np.random.uniform(0.05, 0.19)
                    band = "Low"
                base_cost = base_price * (1 - margin)
                products.append({
                    "Product_ID": prod_id,
                    "Product_Name": f"{subcat} Pro {i}",
                    "Category": cat,
                    "Subcategory": subcat,
                    "Brand": random.choice(["Apex", "Nova", "Zenith", "Omni", "Vertex"]),
                    "Base_Price": round(base_price, 2),
                    "Base_Cost": round(base_cost, 2),
                    "Margin_Band": band
                })
                prod_id += 1
    df_product = pd.DataFrame(products)

    # 4. DIM_CUSTOMER
    num_customers = 2000
    customer_segments = ["Bronze", "Silver", "Gold", "Platinum"]
    acq_channels = ["Organic", "Paid Ads", "Referral", "Social Media"]
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    
    customers = []
    for c_id in range(1, num_customers + 1):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2024, 12, 31)
        signup_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        customers.append({
            "Customer_ID": c_id,
            "Customer_Name": f"Customer_{c_id}",
            "Gender": random.choice(["Male", "Female", "Other"]),
            "Age_Group": random.choice(age_groups),
            "Region_ID": random.randint(1, 12),
            "Signup_Date": signup_date,
            "Acquisition_Channel": random.choice(acq_channels),
            "Customer_Segment": random.choice(customer_segments)
        })
    df_customer = pd.DataFrame(customers)
    df_customer = df_customer.merge(df_region[['Region_ID', 'City', 'State', 'Region']], on='Region_ID', how='left')

    # 5. FACT_SALES
    num_orders = 10000
    sales = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 12, 31)
    total_days = (end_date - start_date).days
    
    for o_id in range(100000, 100000 + num_orders):
        days_offset = random.randint(0, total_days)
        order_date = start_date + timedelta(days=days_offset)
        
        if order_date.month in [10, 11, 12]:
            num_lines = random.randint(2, 5)
            discount_modifier = 0.15
        else:
            num_lines = random.randint(1, 3)
            discount_modifier = 0.05
            
        if order_date.month == 11 and 20 <= order_date.day <= 30:
            num_lines += random.randint(1, 2)
            discount_modifier = 0.25

        customer = random.choice(df_customer.to_dict('records'))
        channel = random.choice(df_channel.to_dict('records'))
        
        for line_id in range(1, num_lines + 1):
            product = random.choice(df_product.to_dict('records'))
            qty = random.randint(1, 5)
            unit_price = product['Base_Price']
            unit_cost = product['Base_Cost']
            discount_pct = np.clip(discount_modifier + random.uniform(0, 0.1), 0, 0.5)
            gross_revenue = qty * unit_price
            discount_amount = gross_revenue * discount_pct
            net_revenue = gross_revenue - discount_amount
            shipping_cost = np.random.uniform(50, 500)
            total_cost = (qty * unit_cost) + shipping_cost
            profit = net_revenue - total_cost
            
            sales.append({
                "Order_ID": o_id,
                "Order_Line_ID": f"{o_id}_{line_id}",
                "Date": order_date,
                "Customer_ID": customer['Customer_ID'],
                "Product_ID": product['Product_ID'],
                "Region_ID": customer['Region_ID'],
                "Channel_ID": channel['Channel_ID'],
                "Quantity": qty,
                "Unit_Price": unit_price,
                "Unit_Cost": unit_cost,
                "Discount_Pct": round(discount_pct, 4),
                "Discount_Amount": round(discount_amount, 2),
                "Gross_Revenue": round(gross_revenue, 2),
                "Net_Revenue": round(net_revenue, 2),
                "Total_Cost": round(total_cost, 2),
                "Profit": round(profit, 2),
                "Shipping_Cost": round(shipping_cost, 2)
            })
            
    df_sales = pd.DataFrame(sales)
    
    # 6. FACT_TARGETS
    targets = []
    years = [2023, 2024, 2025, 2026]
    months = range(1, 13)
    for y in years:
        for m in months:
            for r in df_region['Region_ID'].unique():
                base_target = 1000000 
                variance = np.random.uniform(0.8, 1.2)
                targets.append({
                    "Year": y,
                    "Month": m,
                    "Region_ID": r,
                    "Revenue_Target": round(base_target * variance, 2),
                    "Profit_Target": round(base_target * variance * 0.15, 2)
                })
    df_targets = pd.DataFrame(targets)

    path = "C:/Users/hp/AppData/Local/Temp/opencode/ecommerce-powerbi-intelligence/data/processed"
    if not os.path.exists(path):
        os.makedirs(path)
    df_sales.to_csv(f"{path}/Fact_Sales.csv", index=False)
    df_customer.to_csv(f"{path}/Dim_Customer.csv", index=False)
    df_product.to_csv(f"{path}/Dim_Product.csv", index=False)
    df_region.to_csv(f"{path}/Dim_Region.csv", index=False)
    df_channel.to_csv(f"{path}/Dim_Channel.csv", index=False)
    df_targets.to_csv(f"{path}/Fact_Targets.csv", index=False)
    
    print(f"Successfully generated dataset with {len(df_sales)} sales records.")
    return df_sales, df_customer, df_product, df_region, df_channel, df_targets

if __name__ == "__main__":
    generate_ecommerce_data()
