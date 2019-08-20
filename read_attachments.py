def read_attachments(
	subject_text='', subject_exact=False,
	start_date=None, end_date=None,
	attachment_name='', attachment_exact=True,
	attachment_suffix='',
	sql_filename='',
	end_database=2, database='',staging_tablename='stg_attachments', delete_staging=True,
	error_if_missing=True, print_internal=0, print_details=False
	):

	global error_count


	#u_print("SEARCHING FOR...")
	#u_print("Subject: "+subject_text)
	#u_print("Attachment: "+attachment_name)
	#u_print("Attachment Suffix: "+attachment_suffix)
	u_print("SEARCHING FOR | Subject: "+subject_text+"| Attachment: "+attachment_name+" | Attachment Suffix: "+attachment_suffix)

	return_info = get_emails(
		access_token, etl_folderid, 
		subject_text=subject_text,subject_exact=subject_exact, 
		start_date=start_date, end_date=end_date,
		attachment_name=attachment_name,attachment_exact=attachment_exact,
		attachment_suffix=attachment_suffix, 
		get_attachments=True, print_details=False
		)

	email_df = return_info[0]	
	attachment_df = return_info[1]

	if attachment_df.empty == False:
		#SORT TABLE BY EMAIL DELIVERY DATE
		#ascending is true because we want to process the older files first
		attachment_df.sort_values(by=['sentdate'], ascending=True, axis=0, inplace=True)

		if print_internal > 0:
			u_print('ATTACHMENT FILES FOUND')
		
		for filepath in attachment_df['filepath']:
			output_df = pd.read_csv(filepath)

			column_list = output_df.columns.tolist()
			#replace unwanted characters in column names
			column_list = [w.replace('?', '') for w in column_list]
			output_df.columns = column_list

			sql_filepath = 'sql/'
			tablename = ''
			fields = ''

			merge_with_database(
				output_df, sql_filepath, sql_filename, tablename, fields, 
				end_database, database=database, staging_tablename=staging_tablename, delete_staging=delete_staging) #in FUNCTIONS_sql

			#merge_with_db_powershell(output_df, sql_filepath, sql_filename, tablename, fields, 
			#	end_database, database, staging_tablename, delete_staging, 
			#	print_details=print_details, merge_sql=merge_sql) #in FUNCTIONS_sql

		if print_internal > 1:
			#u_print('')
			u_print('DELETING LOCAL ATTACHMENT FILES')
		for filepath in attachment_df['filepath']:
			os.remove(filepath)
		if print_internal > 1:
			u_print('LOCAL ATTACHMENTS DELETED')
	else:
		
		if error_if_missing == True:
			u_print('ERROR: NO ATTACHMENTS FOUND')
			error_count += 1
		else:
			if print_internal > 0:
				u_print('NO ATTACHMENTS FOUND')

	u_print('')