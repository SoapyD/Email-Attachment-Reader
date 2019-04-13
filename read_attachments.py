def read_attachments(
	subject_text='', subject_exact=False,
	attachment_name='', attachment_exact=True,
	attachment_suffix='',
	sql_filename=''
	):

	attachment_df = get_emails(
		access_token, etl_folderid, 
		subject_text=subject_text,subject_exact=subject_exact, 
		attachment_name=attachment_name,attachment_exact=attachment_exact,
		attachment_suffix=attachment_suffix, 
		get_attachments=True)
	#print(attachment_df['FileName'])
 
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

	u_print('DELETING ATTACHMENTS')
	for filepath in attachment_df['filepath']:
		os.remove(filepath)
	u_print('ATTACHMENTS DELETED')