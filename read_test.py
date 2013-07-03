from readability_score.calculators.fleschkincaid import *
from yahoo_q import *
from write_sqlite import writer

import json
import os
import cPickle as pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

__partial = 0

def cal_read(text):
	return FleschKincaid(text, locale='en_US').min_age


def create_question_obj(fp):
	qa_json = json.loads(fp.read())

	'''question part'''
	q = qa_json['all']['question'][0]
	q_id = q['Id']
	q_cate = q['CategoryId']
	q_date = q['Date']
	q_auth = q['UserId']
	q_choose = q['ChosenAnswererId']
	q_obj = yahoo_q(q_id, q_cate, q_date, q_auth, q_choose)
	q_obj.set_read_score(cal_read(q['Subject'] + ' ' + q['Content']))
	if __partial == 1:
		print 'q age', q_obj.read
	
	'''answer part'''
	a_list = qa_json['all']['answers']
	for a in a_list:
		a_auth = a['UserId']
		a_date = a['Date']
		a_best = a['Best']
		a_obj = yahoo_a(a_auth, a_date, a_best)
		a_obj.set_read_score(cal_read(a['Content']))
		q_obj.add_answers(a_obj)
		if __partial == 1:
			print 'a age', a_auth, a_best, a_obj.read

	return q_obj


def persist(qa_list):
	pickle.dump(qa_list, open("persist/qa.pickle", 'wb'))


def extract_q_a():
	files = os.listdir('Answers')
	qas = []
	for f in files:
		fp = open('Answers/' + f, 'rb')
		qa_obj = create_question_obj(fp)
		qas.append(qa_obj)

	persist(qas)


def write_to_db():
	db_writer = writer()
	files = os.listdir('Answers')

	for f in files:
		fp = open('Answers/' + f, 'rb')
		qa_json = json.loads(fp.read())

		'''question part'''
		q = qa_json['all']['question'][0]
		q_id = q['Id']
		q_sub = q['Subject']
		q_content = q['Content']
		q_cate = q['CategoryId']
		q_date = q['Date']
		q_auth = q['UserId']
		q_choose = q['ChosenAnswererId']
		 
		rlt = db_writer.write_question(q_id, q_sub, q_content, q_date, q_cate, q_auth, q_choose)
		
		if not rlt:
			'''answer part'''
			a_list = qa_json['all']['answers']
			for a in a_list:
				a_auth = a['UserId']
				a_date = a['Date']
				a_best = a['Best']
				a_content = a['Content']
				db_writer.write_answer(q_id, a_content, a_best, a_auth, a_data)
				
		db_writer.commit()
	db_writer.close()

def stats_readtest():
	f = open("persist/qa.pickle", "rb")
	qa_set = pickle.load(f)

	i = 0
	total = 0
	rlt = np.zeros((41, 2), dtype=np.int)
	for qa in qa_set:
		for a in qa.answers:
			total += 1
			diff = qa.read - a.read
			if qa.chosen_ans == a.anth:
				if np.absolute(diff) <= 20:
					rlt[diff+20, 0] += 1
					i += 1
			else:
				if np.absolute(diff) <= 20:
					rlt[diff+20, 1] += 1
					i += 1

	print str(float(i)/total) +  '%'
	bin1 = [x for x in range(-20, 21)]
	bin2 = [x+0.35 for x in range(-20, 21)]
	r1 = plt.bar(bin1, rlt[:, 0], 0.35, color='r', linewidth=0)
	r2 = plt.bar(bin2, rlt[:, 1], 0.35, color='y', linewidth=0)
	plt.ylabel('number of question-answer set')
	plt.xlabel('readability: qestion\'s - answer\'s')
	plt.legend( (r1[0], r2[0]), ('Best Answers', 'Other Answers'))
	plt.show()


def stats_readtest_old():
	f = open("persist/qa.pickle", "rb")
	qa_set = pickle.load(f)

	'''
	red is for readability of non-best answer
	blue is for readability of best answer
	'''
	red_x = []
	red_y = []
	blue_x = []
	blue_y = []
	for qa in qa_set:
		for a in qa.answers:
			if qa.chosen_ans == a.anth:
				blue_x.append(qa.read)
				blue_y.append(a.read)
			else:
				red_x.append(qa.read)
				red_y.append(a.read)

	plt.plot(red_x, red_y, 'ro', markersize=7.0, markerfacecolor='w')
	plt.plot(blue_x, blue_y, 'b+', markersize=7.0)
	plt.title('Readability')
	plt.xlabel('Questions\' Readability')
	plt.ylabel('Answers\' Readability')
	plt.show()

if __name__ == '__main__':
#	extract_q_a()
	write_to_db()
#	stats_readtest()
