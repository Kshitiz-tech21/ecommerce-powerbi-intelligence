# Data Dictionary

| Table | Column | Data Type | Definition | Example | Business Meaning |
|---|---|---|---|---|---|
| **Fact_Sales** | Order_ID | Int64 | Unique identifier for the order | 100001 | Used to count total orders |
| **Fact_Sales** | Net_Revenue | Decimal | Revenue after discounts | 4500.00 | The actual money earned from the sale |
| **Fact_Sales** | Profit | Decimal | Net Revenue minus Total Cost | 1200.00 | The actual gain from the transaction |
| **Dim_Customer** | Customer_ID | Int64 | Unique identifier for the customer | 501 | Used for RFM and CLV analysis |
| **Dim_Customer** | Customer_Segment | String | Assigned value segment | Gold | Used to target marketing campaigns |
| **Dim_Product** | Product_ID | Int64 | Unique identifier for the product | 101 | Used for product-level profit analysis |
| **Dim_Product** | Margin_Band | String | Expected profit range | High | Identifies high-margin vs low-margin items |
| **Dim_Region** | Region_ID | Int64 | Unique identifier for region | 1 | Used for geographic performance tracking |
| **Dim_Region** | Region | String | Geographic area | North | Aggregates performance by zone |
| **Fact_Targets** | Revenue_Target | Decimal | Monthly revenue goal | 1000000 | Used to calculate Target Variance % |
