let
    Source = Csv.Document(File.Contents("C:\Users\hp\AppData\Local\Temp\opencode\ecommerce-powerbi-intelligence\data\processed\Fact_Sales.csv"), [Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"Order_ID", Int64.Type}, {"Order_Line_ID", type text}, {"Date", type date}, 
        {"Customer_ID", Int64.Type}, {"Product_ID", Int64.Type}, {"Region_ID", Int64.Type}, 
        {"Channel_ID", Int64.Type}, {"Quantity", Int64.Type}, {"Unit_Price", type number}, 
        {"Unit_Cost", type number}, {"Discount_Pct", type number}, {"Discount_Amount", type number}, 
        {"Gross_Revenue", type number}, {"Net_Revenue", type number}, {"Total_Cost", type number}, 
        {"Profit", type number}, {"Shipping_Cost", type number}
    }),
    CleanStrings = Table.TransformColumns(ChangeTypes, {{"Order_Line_ID", Text.Trim, type text}}),
    RemoveDuplicates = Table.Distinct(CleanStrings, {"Order_Line_ID"})
in
    RemoveDuplicates
