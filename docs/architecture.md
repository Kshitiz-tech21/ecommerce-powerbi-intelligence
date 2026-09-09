# Architecture Documentation

## Data Pipeline Flow
The project follows a standard BI architectural pattern to ensure data integrity and report performance.

```mermaid
graph LR
    A[Python Data Gen] --> B[CSV Storage]
    B --> C[Power Query ETL]
    C --> D[Star Schema Model]
    D --> E[DAX Calculation Layer]
    E --> F[Power BI Visuals]
```

## Data Model (Star Schema)
The model is designed as a **Star Schema** to optimize for Power BI's VertiPaq engine.

### Tables:
- **Fact_Sales**: The central table containing quantitative measures (Revenue, Cost, Profit).
- **Dim_Date**: Used for all time-based slicing (Years, Quarters, Months).
- **Dim_Customer**: Attributes for customer segmentation.
- **Dim_Product**: Attributes for product and category analysis.
- **Dim_Region**: Geographic attributes.
- **Dim_Channel**: Channel-based attributes.

### Relationship Strategy:
- **Cardinality**: All relationships are **One-to-Many** (Dimension $\rightarrow$ Fact).
- **Direction**: Single-direction filtering to avoid circular dependencies and performance lag.
- **Keys**: Integrated using integer IDs (Surrogate Keys) for faster joining.
