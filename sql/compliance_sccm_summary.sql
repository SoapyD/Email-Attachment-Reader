--set language british;
/*CREATE A TEMP TABLE THEN INSERT IT INTO THE PERMENTANT TABLE*/
/*CREATE TABLE compliance_sccm_summary (*/
DECLARE @Temp_Table TABLE(
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    date DATE,
    device_type NVARCHAR(50),
    customer_id INT,
    auth_list NVARCHAR(50),
    collection NVARCHAR(100),
    total_number_of_devices FLOAT,
    devices_up_to_date FLOAT,
    devices_out_of_date FLOAT,
    compliance_percentage FLOAT,
    non_compliance_percentage FLOAT
);
INSERT INTO @Temp_Table
SELECT
    M.date,
    m.device_type,
    ISNULL(c.id,NULL) AS customer_id,
    m.auth_list,
    m.collection,
    ISNULL(com.number_of_computers,0) +
    ISNULL(n_com.number_of_computers,0) AS total_number_of_devices,
    ISNULL(com.number_of_computers,0) AS devices_up_to_date,
    ISNULL(n_com.number_of_computers,0) AS devices_out_of_date,
    ISNULL(com.percentage,0) AS compliance_percentage,
    1 - ISNULL(com.percentage,0) AS non_compliance_percentage
FROM 
    (
    SELECT DISTINCT
        CONVERT(DATE,date) AS date, 
        company,
        auth_list,
        collection,
        device_type
    FROM
        dbo.stg
    ) m
    LEFT JOIN customers c on (c.customer = m.company)

    LEFT JOIN (
    SELECT
        date,
        number_of_computers,
        CONVERT(FLOAT,percentage) / 100 as percentage
    FROM
        dbo.stg
    WHERE
        status = 'Compliant'
    ) com ON (com.date = m.date)

    LEFT JOIN (
    SELECT
        date,
        SUM(CONVERT(FLOAT,number_of_computers)) AS number_of_computers
    FROM
        dbo.stg
    WHERE
        status <> 'Compliant'
    GROUP BY
        date
    ) n_com ON (n_com.date = m.date);

/*MERGE THE TEMP TABLE WITH THE CLOSED INCIDENTS TABLE*/
MERGE [dbo].[compliance_sccm_summary] target
Using @Temp_Table source
ON (
CONVERT(NVARCHAR,target.customer_id) + CONVERT(NVARCHAR,target.date) + target.auth_list + target.collection 
= 
CONVERT(NVARCHAR,source.customer_id) + CONVERT(NVARCHAR,source.date) + target.auth_list + source.collection
)
WHEN MATCHED
THEN UPDATE
SET
TARGET.date = SOURCE.date,
TARGET.device_type = SOURCE.device_type,
TARGET.customer_id = SOURCE.customer_id,
TARGET.auth_list = SOURCE.auth_list,
TARGET.collection = SOURCE.collection,
TARGET.total_number_of_devices = SOURCE.total_number_of_devices,
TARGET.devices_up_to_date = SOURCE.devices_up_to_date,
TARGET.devices_out_of_date = SOURCE.devices_out_of_date,
TARGET.compliance_percentage = SOURCE.compliance_percentage,
TARGET.non_compliance_percentage = SOURCE.non_compliance_percentage
WHEN NOT MATCHED BY TARGET
THEN INSERT 
(
date,
device_type,
customer_id,
auth_list,
collection,
total_number_of_devices,
devices_up_to_date,
devices_out_of_date,
compliance_percentage,
non_compliance_percentage
)
VALUES (
SOURCE.date,
SOURCE.device_type,
SOURCE.customer_id,
SOURCE.auth_list,
SOURCE.collection,
SOURCE.total_number_of_devices,
SOURCE.devices_up_to_date,
SOURCE.devices_out_of_date,
SOURCE.compliance_percentage,
SOURCE.non_compliance_percentage
);
