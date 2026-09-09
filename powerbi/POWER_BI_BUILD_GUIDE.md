# Power BI Build Guide: E-Commerce Intelligence Dashboard

This guide provides step-by-step instructions to reproduce the professional BI solution.

## 1. Data Loading
1. Open Power BI Desktop.
2. Go to **Get Data** -> **Text/CSV**.
3. Load the following files from `data/processed/`:
   - `Fact_Sales.csv`
   - `Dim_Customer.csv`
   - `Dim_Product.csv`
   - `Dim_Region.csv`
   - `Dim_Channel.csv`
   - `Fact_Targets.csv`

## 2. Power Query Transformations
1. Open **Transform Data**.
2. For `Fact_Sales`:
   - Ensure `Date` is set to **Date** type.
   - Ensure all revenue/cost columns are **Decimal Number**.
3. Create a **Date Table** using this DAX (New Table):
   ```dax
   Dim_Date = 
   ADDCOLUMNS(
       CALENDARAUTO(),
       "DateKey", FORMAT([Date], "YYYYMMDD"),
       "Year", YEAR([Date]),
       "Month", FORMAT([Date], "MMMM"),
       "MonthNum", MONTH([Date]),
       "Quarter", "Q" & FORMAT([Date], "Q"),
       "MonthYear", FORMAT([Date], "MMM YYYY"),
       "MonthYearSort", FORMAT([Date], "YYYYMM")
   )
   ```
4. Set **Sort by Column** for `Month` using `MonthNum`.

## 3. Data Modeling (Star Schema)
Create the following relationships (One-to-Many, Single direction):
- `Dim_Date[Date]` -> `Fact_Sales[Date]`
- `Dim_Customer[Customer_ID]` -> `Fact_Sales[Customer_ID]`
- `Dim_Product[Product_ID]` -> `Fact_Sales[Product_ID]`
- `Dim_Region[Region_ID]` -> `Fact_Sales[Region_ID]`
- `Dim_Channel[Channel_ID]` -> `Fact_Sales[Channel_ID]`
- `Dim_Region[Region_ID]` -> `Fact_Targets[Region_ID]` (Link to target table)
- `Dim_Date[Year]` & `Dim_Date[MonthNum]` -> `Fact_Targets[Year]` & `Fact_Targets[Month]`

## 4. Semantic Layer (DAX)
1. Create a new table called `_Measures`.
2. Copy and paste the measures from `powerbi/dax/measures.dax`.

## 5. Visual Layouts

### Page 1: Executive Overview
- **KPI Cards**: Total Revenue, Total Profit, Profit Margin %, Total Orders, Total Customers.
- **Line Chart**: X: `Dim_Date[MonthYear]`, Y: `[Total Revenue]`.
- **Clustered Bar Chart**: X: `[Total Revenue]`, Y: `Dim_Product[Category]`.
- **Map/Bar Chart**: Revenue by `Dim_Region[Region]`.

### Page 2: Sales Intelligence
- **Slicer**: `Dim_Date[Year]`, `Dim_Product[Category]`.
- **Treemap**: Group: `Dim_Product[Category]`, Values: `[Total Revenue]`.
- **Bar Chart (Top N)**: Use a field parameter or filter to show Top 10 Products by Revenue.
- **Line Chart**: Revenue vs LY Revenue.

### Page 3: Customer Analytics
- **Donut Chart**: `Dim_Customer[Customer_Segment]`.
- **Bar Chart**: Revenue by `RFM Segment`.
- **Table**: Top 20 Customers by `[Total Revenue]` (CLV).

### Page 4: Profitability Analysis
- **Scatter Plot**: X: `[Total Revenue]`, Y: `[Profit Margin %]`, Size: `[Total Profit]`, Legend: `Dim_Product[Category]`.
- **Waterfall Chart**: Gross Revenue -> Discounts -> Net Revenue -> Cost -> Profit.

### Page 5: Business Insights
- **Multi-row Card**: Display dynamic insights using DAX measures.
- **Table**: Products with High Revenue but Low Margin.

## 6. Final Polish
1. Import `powerbi/theme/ecommerce_theme.json`.
2. Set Page Size to 16:9.
3. Add a Navigation Bar (Buttons) to all pages.
