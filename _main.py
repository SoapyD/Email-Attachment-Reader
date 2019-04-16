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


start_date = datetime.datetime.now()
start_date = start_date - datetime.timedelta(days=20.0)
start_date = start_date.strftime('%Y-%m-%d')

end_date = datetime.datetime.now()
end_date = end_date.strftime('%Y-%m-%d')

access_token = get_windows_accesstoken(lf_tenantid, 'etl_email_access', etl_clientid, etl_clientsecret, 'https://outlook.office.com/')

#################################################################################GET THE SUMMARY COMPLIANCE SCCM INFO
read_attachments(
	start_date=start_date, end_date=end_date,
	attachment_name='compliance_report_SUMMARY',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_summary')

#################################################################################GET THE DETAIL COMPLIANCE SCCM INFO
read_attachments(
	start_date=start_date, end_date=end_date,
	attachment_name='compliance_report_DETAILS',attachment_exact=False, 
	attachment_suffix='.csv',
	sql_filename='compliance_sccm_details')


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