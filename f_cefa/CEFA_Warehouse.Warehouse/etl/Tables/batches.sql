CREATE TABLE [etl].[batches] (

	[sf_batch_id] bigint NOT NULL, 
	[process_name] varchar(500) NOT NULL, 
	[stage_name] varchar(500) NOT NULL, 
	[batch_status] smallint NOT NULL, 
	[is_success] bit NOT NULL, 
	[dtm_start] datetime2(0) NOT NULL, 
	[dtm_end] datetime2(0) NULL, 
	[sf_user_id] varchar(500) NOT NULL, 
	[pipeline_run_id] varchar(500) NULL, 
	[src_file_name] varchar(8000) NULL, 
	[cnt_ins_rows] bigint NULL, 
	[cnt_upd_rows] bigint NULL, 
	[cnt_del_rows] bigint NULL
);