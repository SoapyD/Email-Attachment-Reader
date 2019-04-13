--set language british;
/*CREATE A TEMP TABLE THEN INSERT IT INTO THE PERMENTANT TABLE*/
/*CREATE TABLE compliance_sccm_summary (*/
DECLARE @Temp_Table TABLE(
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [company] NVARCHAR(50),
    date DATE,
    [status] NVARCHAR(30),
    [number_of_computers] FLOAT,
    [percentage] FLOAT,
    [title] NVARCHAR(100),
    [auth_list] NVARCHAR(50),
    [collection] NVARCHAR(100)
);
INSERT INTO @Temp_Table
SELECT
    company,
    CONVERT(DATE,date), 
    [status],
    [number_of_computers],
    [percentage],
    [title],
    [auth_list],
    [collection]
FROM 
[dbo].[stg] stg;

/*MERGE THE TEMP TABLE WITH THE CLOSED INCIDENTS TABLE*/
MERGE [dbo].[compliance_sccm_summary] target
Using @Temp_Table source
ON (
target.company + CONVERT(NVARCHAR,target.date) + target.status + target.auth_list + target.collection 
= 
source.company + CONVERT(NVARCHAR,source.date) + source.status + target.auth_list + source.collection
)
WHEN MATCHED
THEN UPDATE
SET
TARGET.company = SOURCE.company,
TARGET.date = SOURCE.date,
TARGET.status = SOURCE.status,
TARGET.number_of_computers = SOURCE.number_of_computers,
TARGET.percentage = SOURCE.percentage,
TARGET.title = SOURCE.title,
TARGET.auth_list = SOURCE.auth_list,
TARGET.collection = SOURCE.collection
WHEN NOT MATCHED BY TARGET
THEN INSERT 
(
[company],
date,
[status],
[number_of_computers],
[percentage],
[title],
[auth_list],
[collection]
)
VALUES (
SOURCE.company,
SOURCE.date,
SOURCE.status,
SOURCE.number_of_computers,
SOURCE.percentage,
SOURCE.title,
SOURCE.auth_list,
SOURCE.collection
);
