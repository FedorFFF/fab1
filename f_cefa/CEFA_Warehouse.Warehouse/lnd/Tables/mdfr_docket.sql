CREATE TABLE [lnd].[mdfr_docket] (

	[record_type] varchar(50) NULL, 
	[docket_num] varchar(100) NULL, 
	[agency_code] varchar(50) NULL, 
	[cit_ref_id] varchar(100) NULL, 
	[court_date] varchar(50) NULL, 
	[court_time] varchar(50) NULL, 
	[judge_id] varchar(100) NULL, 
	[room_id] varchar(100) NULL, 
	[hearing_type] varchar(100) NULL, 
	[case_status] varchar(100) NULL, 
	[attorney_id] varchar(100) NULL, 
	[continuance_count] varchar(50) NULL, 
	[last_action_date] varchar(50) NULL, 
	[system_ts] varchar(100) NULL, 
	[sf_batch_id] bigint NULL, 
	[sf_src_file_name] varchar(8000) NULL
);