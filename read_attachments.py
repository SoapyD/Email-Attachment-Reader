def read_attachments(
	subject_text='', subject_exact=False,
	start_date=None, end_date=None,
	attachment_name='', attachment_exact=True,
	attachment_suffix='',
	sql_filename='',
	end_database=2, database='',staging_tablename='stg_attachments'
	):

	u_print("SEARCHING FOR...")
	u_print("Subject: "+subject_text)
	u_print("Attachment: "+attachment_name)
	u_print("Attachment Suffix: "+attachment_suffix)
	u_print("")

	return_info = get_emails(
		access_token, etl_folderid, 
		subject_text=subject_text,subject_exact=subject_exact, 
		start_date=start_date, end_date=end_date,
		attachment_name=attachment_name,attachment_exact=attachment_exact,
		attachment_suffix=attachment_suffix, 
		get_attachments=True
		)

	email_df = return_info[0]	
	attachment_df = return_info[1]

	if attachment_df.empty == False:
		#SORT TABLE BY EMAIL DELIVERY DATE
		#ascending is true because we want to process the older files first
		attachment_df.sort_values(by=['sentdate'], ascending=True, axis=0, inplace=True)
		
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
				end_database, database=database, staging_tablename=staging_tablename) #in FUNCTIONS_sql

		u_print('')
		u_print('DELETING LOCAL ATTACHMENT FILES')
		for filepath in attachment_df['filepath']:
			os.remove(filepath)
		u_print('LOCAL ATTACHMENTS DELETED')
	else:
		u_print('NO ATTACHMENTS FOUND')