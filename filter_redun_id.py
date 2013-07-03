def filter_data(id_file):
	try:
		with open(id_file, 'rb') as fp:
			idlist = fp.readlines()
			idpool = set(idlist)
			fp.close()
	
		with open(id_file, 'wb') as fp1:
			text = ''.join(idpool)
			fp1.write(text)
			fp1.close()
		return True

	except IOError as e:
		print e.strerror
		return False
