import os

def compare(id_file):
	with open(id_file, 'rb') as fp:
		all_ids = fp.readlines()
		fp.close()

	new_ids = []
	for id in all_ids:
		new_ids.append(id[:-1])
	all_data = os.listdir('Answers')
	
	all_ids_set = set(new_ids)
	all_data_set = set(all_data)

	diff = all_ids_set-all_data_set

	new_file_name = id_file + "-left"
	with open(new_file_name, 'w') as fp1:
		fp1.write('\n'.join(diff))
		fp1.write('\n')
		fp1.close()
	
	return new_file_name
