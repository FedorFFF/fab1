CREATE TABLE [etl].[file_mapping] (

	[src_file_folder] varchar(900) NULL, 
	[src_file_mask] varchar(200) NULL, 
	[trg_scheme] varchar(100) NULL, 
	[trg_table] varchar(200) NULL
);