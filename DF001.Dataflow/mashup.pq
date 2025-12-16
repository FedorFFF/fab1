[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "orders_DataDestination", IsNewTarget = false], Settings = [Kind = "Manual", AllowCreation = false, ColumnSettings = [Mappings = {[SourceColumnName = "SalesOrderID", DestinationColumnName = "SalesOrderID"], [SourceColumnName = "OrderDate", DestinationColumnName = "OrderDate"], [SourceColumnName = "CustomerID", DestinationColumnName = "CustomerID"], [SourceColumnName = "LineItem", DestinationColumnName = "LineItem"], [SourceColumnName = "ProductID", DestinationColumnName = "ProductID"], [SourceColumnName = "OrderQty", DestinationColumnName = "OrderQty"], [SourceColumnName = "LineItemTotal", DestinationColumnName = "LineItemTotal"], [SourceColumnName = "MonthNo", DestinationColumnName = "MonthNo"]}], DynamicSchema = false, UpdateMethod = [Kind = "Replace"], TypeSettings = [Kind = "Table"]]]}]
shared orders = let
  Source = Csv.Document(Web.Contents("https://leverxcorp-my.sharepoint.com/personal/fiodar_hulin_leverx_com/Documents/Apps/Microsoft Power Query/Uploaded Files/orders.csv"), [Delimiter = ",", Columns = 7, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"SalesOrderID", Int64.Type}, {"OrderDate", type date}, {"CustomerID", Int64.Type}, {"LineItem", Int64.Type}, {"ProductID", Int64.Type}, {"OrderQty", Int64.Type}, {"LineItemTotal", type number}}),
  #"Added custom" = Table.TransformColumnTypes(Table.AddColumn(#"Changed column type", "MonthNo", each Date.Month([OrderDate])), {{"MonthNo", Int64.Type}}),
  #"Changed column type 1" = Table.TransformColumnTypes(#"Added custom", {{"OrderDate", type date}})
in
  #"Changed column type 1";
shared orders_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = null, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "7dd85790-2e04-4e40-90a7-f20f50640ed8"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "89b26255-9375-4061-9a6e-bdce49bc227f"]}[Data],
  TableNavigation = Navigation_2{[Id = "orders", ItemKind = "Table"]}[Data]
in
  TableNavigation;
