[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "7dd85790-2e04-4e40-90a7-f20f50640ed8"]}[Data]{[lakehouseId = "d5c2ab53-a721-42c1-8b28-07f0079cf878"]}[Data];
[BindToDefaultDestination = true]
shared products = let
  Source = Csv.Document(Web.Contents("https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/products.csv"), [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"ProductID", Int64.Type}, {"ProductName", type text}, {"Category", type text}, {"ListPrice", type number}})
in
  #"Changed column type";
