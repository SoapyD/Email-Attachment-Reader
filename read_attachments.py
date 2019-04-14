def read_attachments(
	subject_text='', subject_exact=False,
	start_date=None, end_date=None,
	attachment_name='', attachment_exact=True,
	attachment_suffix='',
	sql_filename=''
	):

	attachment_df = get_emails(
		access_token, etl_folderid, 
		subject_text=subject_text,subject_exact=subject_exact, 
		start_date=start_date, end_date=end_date,
		attachment_name=attachment_name,attachment_exact=attachment_exact,
		attachment_suffix=attachment_suffix, 
		get_attachments=True)
	#print(attachment_df['FileName'])

	if attachment_df.empty == False:
		#SORT TABLE BY EMAIL DELIVERY DATE
		attachment_df.sort_values(by=['sentdate'], ascending=False, axis=0, inplace=True)

		for filepath in attachment_df['filepath']:
			output_df = pd.read_csv(filepath)

			column_list = output_df.columns.tolist()
			#replace unwanted characters in column names
			column_list = [w.replace('?', '') for w in column_list]
			output_df.columns = column_list

			sql_filepath = 'sql/'
			tablename = ''
			fields = ''

			merge_with_database(output_df, sql_filepath, sql_filename, tablename, fields, 2) #in FUNCTIONS_sql

		u_print('')
		u_print('DELETING LOCAL ATTACHMENT FILES')
		for filepath in attachment_df['filepath']:
			os.remove(filepath)
		u_print('LOCAL ATTACHMENTS DELETED')
	else:
		u_print('NO ATTACHMENTS FOUND')