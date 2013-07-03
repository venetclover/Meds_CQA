from filter_redun_id import *
from compare_id_data import *

import urllib
import json
import os
import sys
import argparse
import logging

'''http://answers.yahooapis.com/AnswersService/V1/getByCategory?appid=VyK5pOXV34FFe96isM9r1FST4g4rTN8GjbZnC94evkA9vnRSfROR9t278xsNsDu29ME-&category_id=396545664&start=20&results=20&output=json&type=resolved
'''

url_base = 'http://answers.yahooapis.com/AnswersService/V1/'
get_by_category = 'getByCategory?'
get_by_question = 'getQuestion?'

str_appid = 'appid=VyK5pOXV34FFe96isM9r1FST4g4rTN8GjbZnC94evkA9vnRSfROR9t278xsNsDu29ME-'
category_id = 0

batch_n = 50

def collect_data(input_file):
	global url_base, get_by_question, str_appid
	with open(input_file, 'rb') as fp:
		qids = fp.readlines()
		fp.close()

	for qid_i in qids:
		qid = qid_i[:-1]
		str_qid = '&question_id='+str(qid)
		str_format = '&output=json'
		uri = url_base+get_by_question+str_appid+str_format+str_qid
#		print uri
		print qid
		try:
			response = urllib.urlopen(uri)
			response = json.load(response)
			text = json.dumps(response)
#			print '---raw data---', text
			with open('Answers/'+str(qid), "wb") as fp2:
				fp2.write(text)
			qids.remove(qid_i)
		except ValueError:
			print 'Error: won\'t write to file'
			break

	'''Put unsuccessfully rendering question id in <CATEGORY_ID>-left'''
	with open(input_file, 'wb') as fp:
		fp.write(''.join(qids))
		fp.close()


def collect_id_byCate():
	new_file_name = 'ids/' + str(category_id) + '-cate'
	with open(new_file_name, 'wb') as fp:
		fp.close()
	
	q_ids = []
	start_n = 0
	for i in xrange(100):
		str_category_id = '&category_id='+str(category_id)
		str_start = '&start='+str(start_n)
		str_results = '&results='+str(batch_n)
		str_format = '&output=json'
		str_type = '&type=resolved'
		print 'Collecting ' + str(start_n) + '~' + str(start_n+49) + ' by category'
		uri = url_base+get_by_category+str_appid+str_category_id+str_start+str_results+str_format+str_type
#		print uri
		try:
			response = urllib.urlopen(uri)
#			print '---raw data---', response.read()
			response = json.load(response)
			results = response["all"]["questions"]
			for line in results:
				q_ids.append(line["Id"])
			with open(new_file_name, "a") as fp2:
				fp2.write('\n'.join(q_ids))
				fp2.write('\n')
			start_n += batch_n
		except ValueError:
			print "Fail to render ids."
			break
		except KeyError:
			print response
			break

	return new_file_name


def collect_id_byDate():
	new_file_name = 'ids/' + category_id + '-date'
	with open(new_file_name, 'wb') as fp:
		fp.close()
	
	with open("ids/index", 'rb') as fp1:
		start_n = int(fp1.read())
		fp1.close()
		 
	q_ids = []
	for i in xrange(50):
		str_category_id = '&category_id='+str(category_id)
		str_sort = '&sort=date_asc'
		str_start = '&start='+str(start_n)
		str_results = '&results='+str(batch_n)
		str_format = '&output=json'
		str_type = '&type=resolved'
		uri = url_base+get_by_category+str_appid+str_category_id+str_sort+str_start+str_results+str_format+str_type
#		print uri
		print 'Collecting ' + str(start_n + batch_n*i) + '~' + str(start_n + batch_n * (i+1)) + ' by date'
		response = urllib.urlopen(uri)
#       print '---raw data---', response.read()
		try:
			response = json.load(response)
			results = response["all"]["questions"]
			for line in results:
				q_ids.append(line["Id"])
			
			with open(new_file_name, "a") as fp2:
				fp2.write('\n'.join(q_ids))
				fp2.write('\n')
				start_n += batch_n * (i + 1)
			 
			'''record index'''
			with open("ids/index", 'wb') as fp1:
				fp1.write(str(start_n))
				fp1.close()
		except ValueError:
			print "Fail to render ids."
			break
		except KeyError:
			print response
			break
	return new_file_name


def get_categoryId():
	with open("meds_categories", 'rb') as fp:
		ids = fp.readlines()
	
	return ids[0][:-1]


'''
get_data.py [OPTIONS]

	-h 				: help
	-f <INPUTFILE> 	: filter duplicate ids in the input file
	-co <INPUTFILE> : compare ids with existing data in "Answers"
	-cc 			: collect data using '<category_id>-left'
'''
def main(argv):
	parser = argparse.ArgumentParser()
	group1 = parser.add_mutually_exclusive_group()
	group1.add_argument("-s", "--separate", action='store_true')
	parser.add_argument("-options", choices=['cate', 'date'])
	group1.add_argument("-f", "--filter", action='store_true')
	group1.add_argument("-c", "--compare", action='store_true')
	parser.add_argument("-a", "--all", action='store_true')
	parser.add_argument("-o", "--collect", action='store_true')
	args = parser.parse_args()

	global category_id
	category_id = get_categoryId()

	if args.all:
		'''collect by category first'''
		print 'Collect data by category and date'
		file_cate = collect_id_byCate()
		filter_data(file_cate)
		prepared_ids = compare(file_cate)
		collect_data(prepared_ids)
		'''...and then collect by date'''
		file_date = collect_id_byDate()
		filter_data(file_date)
		prepared_ids = compare(file_date)
		collect_data(prepared_ids)
	
	elif args.separate:
		if args.options == 'date':
			file_date = collect_id_byDate()
			filter_data(file_date)
			prepared_ids = compare(file_date)
			collect_data(prepared_ids)
		elif args.options == 'cate':
			file_cate = collect_id_byCate()
			filter_data(file_cate)
			prepared_ids = compare(file_cate)
			collect_data(prepared_ids)
	
	elif args.filter:
		files = os.listdir('ids')
		f_show = []
		for f in files:
			if f.endswith('cate') or f.endswith('date'):
				f_show.append(f)

		file_str = []
		for i, f in enumerate(f_show):
			file_str.append(str(i) + ': ' + f)
		i = raw_input('Choose ID file you want to filter:\n'+'\n'.join(file_str)+'\n' + '[0-n]: ')
		filter_data('ids/' + f_show[int(i)])

	elif args.compare:
		files = os.listdir('ids')
		f_show = []
		for f in files:
			if f.endswith('cate') or f.endswith('date'):
				f_show.append(f)

		file_str = []
		for i, f in enumerate(f_show):
			file_str.append(str(i) + ': ' + f)
		i = raw_input('Choose ID file you want to compare:\n'+'\n'.join(file_str)+'\n' + '[0-n]: ')
		prepared_ids = compare('ids/' + f_show[int(i)])
		print 'Results generated to ' + prepared_ids

	elif args.collect:
		idfiles = os.listdir('ids')
		for idfile in idfiles:
			if idfile.endswith('cate-left') or idfile.endswith('date-left'):
				'''Collect data that is not existing in "/Answers"'''	
				prepared_ids = compare('ids/' + idfile)
				os.remove('ids/' + idfile)
				os.rename('ids/' + prepared_ids, 'ids/' + idfile)
				print 'Collect data from ' + str(idfile)
				collect_data('ids/' + idfile)

if __name__ == '__main__':
	main(sys.argv[1:])
