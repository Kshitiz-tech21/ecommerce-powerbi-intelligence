# Interview Guide: E-Commerce BI Project

This document prepares you to defend the technical and business decisions made in this project during a BI/Data Analyst interview.

## 🛠️ Technical Questions

**1. Why did you choose a Star Schema over a Flat Table?**
*Answer:* A star schema reduces data redundancy and improves query performance in Power BI. By separating dimensions (Customer, Product) from facts (Sales), I ensure that filters propagate efficiently and the model remains scalable as the dataset grows.

**2. How did you handle the Date Dimension?**
*Answer:* I created a dedicated `Dim_Date` table. Using a Date table is critical for Power BI's Time Intelligence functions (like `TOTALYTD` or `SAMEPERIODLASTYEAR`). It ensures there are no gaps in the date sequence, which would otherwise break these calculations.

**3. Why calculate KPIs in DAX instead of adding calculated columns in Power Query?**
*Answer:* Calculated columns are computed during data refresh and stored in memory, increasing file size. DAX measures are computed on-the-fly based on the current filter context, making them dynamic and memory-efficient.

**4. Explain your RFM implementation.**
*Answer:* RFM stands for Recency, Frequency, and Monetary. I created measures to calculate the days since the last purchase, the total order count, and total spend per customer. I then assigned scores (1-5) based on quintiles/thresholds and concatenated them to create segments like "Champions" or "At Risk".

**5. Why avoid bi-directional filtering?**
*Answer:* Bi-directional filtering can introduce ambiguity in the data model, leading to incorrect results and slower performance. I stuck to one-to-many single-direction filters to maintain a clear flow of data from dimensions to facts.

## 📈 Business Questions

**6. What is the most important KPI for the Executive Overview?**
*Answer:* While Revenue is key, **Profit Margin %** is the most critical. Revenue without profit is just vanity. Tracking the margin allows management to see if growth is sustainable or if it's being "bought" with excessive discounts.

**7. How did you identify "Loss Making Products"?**
*Answer:* I created a measure `Profit = [Net Revenue] - [Total Cost]`. By filtering the Product dimension where this measure is negative, I can immediately list products where the unit cost and shipping exceed the discounted selling price.

**8. What business action would you recommend if "Electronics" has high revenue but low profit?**
*Answer:* I would recommend:
1. Reviewing the discount strategy (reducing deep discounts on high-demand items).
2. Negotiating better procurement costs with vendors.
3. Analyzing if the shipping costs for electronics are disproportionately high.
