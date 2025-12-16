[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "7dd85790-2e04-4e40-90a7-f20f50640ed8"]}[Data]{[lakehouseId = "89b26255-9375-4061-9a6e-bdce49bc227f"]}[Data];
[BindToDefaultDestination = true]
shared customer_200 = let
  Source = Excel.Workbook(Web.Contents("https://leverxcorp-my.sharepoint.com/personal/fiodar_hulin_leverx_com/Documents/Apps/Microsoft Power Query/Uploaded Files/customer_200.xlsx"), null, true),
  #"Navigation 1" = Source{[Item = "customer_200", Kind = "Sheet"]}[Data],
  #"Changed column type" = Table.TransformColumnTypes(#"Navigation 1", {{"Column1", Int64.Type}, {"Column2", type text}, {"Column3", Int64.Type}, {"Column4", Int64.Type}, {"Column5", type text}, {"Column6", type text}, {"Column7", type datetime}})
in
  #"Changed column type";
