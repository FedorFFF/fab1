CREATE   PROC What_DB_is_this
AS
SELECT DB_NAME() AS ThisDB;

/*@@SERVERNAME servname
--, @@SERVICENAME	
,	@@version version
 , @@LANGUAGE LANGUAGE  
 --, @@CONNECTIONS conn1
 --, suser_id() suser_Id
, suser_sid() suser_Sid 
*/
--raiserror('Obsolete file odsole.sql.  Please remove use.',0,1)
-- SELECT HOST_NAME() AS HostName
SELECT 
@@SERVERNAME servname
--, @@SERVICENAME	SERVICENAME
,	@@version version
 , @@LANGUAGE LANGUAGE  
 --, @@CONNECTIONS conn1
 --, suser_id() suser_Id
, suser_sid() suser_Sid 
,CURRENT_USER CURR_USER
--, HOST_NAME() AS HostName
, SUSER_NAME() NT_user
--, SUSER_ID () AS SUSER_ID  
, USER_NAME() user1
, SYSTEM_USER sys_user
, CURRENT_TIMESTAMP CURR_TIME
, convert(char,CURRENT_TIMESTAMP,8)time1
, db_NAME() db_NAME
, DB_ID ( ) DB_ID 
--, @@LANGID  LANGID
, @@TRANCOUNT TRANCOUNT