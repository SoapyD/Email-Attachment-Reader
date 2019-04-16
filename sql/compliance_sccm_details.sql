DECLARE
@first_pass_script INT = 0;
/*CREATE A TEMP TABLE THEN INSERT IT INTO THE PERMENTANT TABLE*/
/*CREATE TABLE compliance_sccm_details (*/
DECLARE @Temp_Table TABLE(
    id DECIMAL IDENTITY(1,1) NOT NULL PRIMARY KEY,
    company NVARCHAR(50),
    date DATE,
    status_code INT,
    status NVARCHAR(30),
    auth_list NVARCHAR(50),
    collection_id NVARCHAR(50),
    collection NVARCHAR(70),
    collection_shortname NVARCHAR(30),
    resource_id FLOAT,
    machine_name NVARCHAR(100),
    last_logged_on_user NVARCHAR(200),
    assigned_site NVARCHAR(30),
    client_version NVARCHAR(50)
);
INSERT INTO @Temp_Table
SELECT
    company,
    date,
    Status,
    status_text,  
    auth_list,
    collection,
    CI_ID,
    CollectionID,
    ResourceID,
    MachineName,
    LastLoggedOnUser,
    AssignedSite,
    ClientVersion
FROM 
dbo.stg stg;

/*DELETE THE OLD COMPANY COLLECTION DATA*/
IF @first_pass_script = 1
BEGIN
    DELETE d
    FROM dbo.compliance_sccm_details d
    INNER JOIN @Temp_Table t ON (t.company = d.company AND t.collection_id = d.collection_id)
END
/**/

/*MERGE THE TEMP TABLE WITH THE CLOSED INCIDENTS TABLE*/
MERGE dbo.compliance_sccm_details target
Using @Temp_Table source
ON (
target.company + target.machine_name + target.collection_id
= 
source.company + source.machine_name + source.collection_id
)
WHEN MATCHED
THEN UPDATE
SET
TARGET.company = SOURCE.company,
TARGET.date = SOURCE.date,
TARGET.status_code = SOURCE.status_code,
TARGET.status = SOURCE.status,
TARGET.auth_list = SOURCE.auth_list,
TARGET.collection_id = SOURCE.collection_id,
TARGET.collection = SOURCE.collection,
TARGET.collection_shortname = SOURCE.collection_shortname,
TARGET.resource_id = SOURCE.resource_id,
TARGET.machine_name = SOURCE.machine_name,
TARGET.last_logged_on_user = SOURCE.last_logged_on_user,
TARGET.assigned_site = SOURCE.assigned_site,
TARGET.client_version = SOURCE.client_version
WHEN NOT MATCHED BY TARGET
THEN INSERT 
(
company,
date,
status_code,
status,
auth_list,
collection_id,
collection,
collection_shortname,
resource_id,
machine_name,
last_logged_on_user,
assigned_site,
client_version
)
VALUES (
SOURCE.company,
SOURCE.date,
SOURCE.status_code,
SOURCE.status,
SOURCE.auth_list,
SOURCE.collection_id,
SOURCE.collection,
SOURCE.collection_shortname,
SOURCE.resource_id,
SOURCE.machine_name,
SOURCE.last_logged_on_user,
SOURCE.assigned_site,
SOURCE.client_version
);
