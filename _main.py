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
u_print("RUNNING GIT REFRESH PROCESS")
u_print('########################################')

start_time = datetime.datetime.now() #need for process time u_printing


access_token = get_windows_accesstoken(lf_tenantid, 'etl_email_access', etl_clientid, etl_clientsecret, 'https://outlook.office.com/')



end_database = 2
database = 'INF_DATA'

start_date = datetime.datetime.now()
start_date = start_date - datetime.timedelta(days=1.0)
start_date = start_date.strftime('%Y-%m-%d')

end_date = datetime.datetime.now() + datetime.timedelta(days=1.0)
end_date = end_date.strftime('%Y-%m-%d')

u_print('')
u_print('email search range from: '+str(start_date)+" to: "+str(end_date))
u_print('')

#################################################################################GET THE SUMMARY COMPLIANCE SCCM INFO
read_attachments(
	start_date=start_date, end_date=end_date,
	attachment_name='compliance_report_SUMMARY',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_summary',
	end_database=end_database, database=database)

#################################################################################GET THE DETAIL COMPLIANCE SCCM INFO
read_attachments(
	start_date=start_date, end_date=end_date,
	attachment_name='compliance_report_DETAILS',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_details',
	end_database=end_database, database=database)


finish_time = datetime.datetime.now()

u_print('')
u_print('########################################')
u_print("PROCESS COMPLETE")
u_print("Number of Errors: "+str(error_count))
u_print('Start: '+str(start_time))
u_print('End: '+str(finish_time))
u_print('Time Taken: '+str(finish_time - start_time))
u_print('########################################')

save_process(start_time, finish_time, str(finish_time - start_time), "Email-Attachment-Reader")