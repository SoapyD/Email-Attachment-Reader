import os
path = os.getcwd() #get the current path
string_pos = path.index('Python') #find the python folder
base_path = path[:string_pos]+'Python\\' #create a base filepath string

func_dir = base_path+"functions\\"
exec(open(func_dir+"functions.py").read()) #file contains all sql reading and db interaction scripts
exec(open("read_attachments.py").read())

import datetime
global error_count

u_print('########################################')
u_print("RUNNING EMAIL-ATTACHMENT-READER PROCESS")
u_print('########################################')

start_time = datetime.datetime.now() #need for process time u_printing


access_token = get_windows_accesstoken(lf_tenantid, 'etl_email_access', etl_clientid, etl_clientsecret, 'https://outlook.office.com/')

print_internal = 0
print_details = False


end_database = 2
#database = 'LF-SQL-DEV'
#staging_tablename='stg'
database = 'INF_DATA'
staging_tablename='stg_attachments'
delete_staging = True

start_date = datetime.datetime.now()
start_date = start_date - datetime.timedelta(days=0.0)
start_date = start_date.strftime('%Y-%m-%d')

end_date = datetime.datetime.now() + datetime.timedelta(days=1.0)
end_date = end_date.strftime('%Y-%m-%d')

if print_internal > 0:
	u_print('')
	u_print('email search range from: '+str(start_date)+" to: "+str(end_date))
	u_print('')

#################################################################################GET THE SUMMARY COMPLIANCE SCCM INFO

#CAFCASS
read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance summary - cafcass - CF10001D',subject_exact=True,
	attachment_name='compliance_report_SUMMARY',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_summary',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance summary - cafcass - CF100077',subject_exact=True,
	attachment_name='compliance_report_SUMMARY',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_summary',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

#FARROW & BALL
read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance summary - farrow&ball- FB1000044',subject_exact=True,
	attachment_name='compliance_report_SUMMARY',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_summary',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance summary - farrow&ball- FB1000045',subject_exact=True,
	attachment_name='compliance_report_SUMMARY',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_summary',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

#UKEF
read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance summary - ukef - EF100087',subject_exact=True,
	attachment_name='compliance_report_SUMMARY',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_summary',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

#################################################################################GET THE DETAIL COMPLIANCE SCCM INFO

#CAFCASS
read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance details - cafcass - CF10001D',subject_exact=True,
	attachment_name='compliance_report_DETAILS',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_details',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance details - cafcass - CF100077',subject_exact=True,
	attachment_name='compliance_report_DETAILS',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_details',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

#FARROW & BALL
read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance details - farrow&ball- FB1000044',subject_exact=True,
	attachment_name='compliance_report_DETAILS',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_details',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance details - farrow&ball- FB1000045',subject_exact=True,
	attachment_name='compliance_report_DETAILS',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_details',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

#UKEF
read_attachments(
	start_date=start_date, end_date=end_date,
	subject_text='sccm compliance details - ukef - EF100087',subject_exact=True,
	attachment_name='compliance_report_DETAILS',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_details',
	end_database=end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging, 
	print_internal=print_internal, print_details=print_details)

finish_time = datetime.datetime.now()

u_print('')
u_print('########################################')
u_print("PROCESS COMPLETE")
u_print("Number of Errors: "+str(error_count))
u_print('Start: '+str(start_time))
u_print('End: '+str(finish_time))
u_print('Time Taken: '+str(finish_time - start_time))
u_print('########################################')

save_process(start_time, finish_time, str(finish_time - start_time), "Email-Attachment-Reader", "daily")