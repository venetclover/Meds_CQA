import os
import simplejson as json

import read_test

from gensim import corpora

stoplist = set('for a of the and to in as'.split())


def lda(text):
	dictionary = corpora.Dictionary(text)
	print dictionary.token2id


def load_pickle(filename):
	f = open(filename, "rb")
	qa_set = pickle.load(f)
	return qa_set


def load_json():
	files = os.listdir('Answers')
	for f in files:
		yield json.loads(open('Answers/'+f, 'rb').read())


def eliminate_punc(text):
	text = text.replace(',', '')
	text = text.replace('.', '')
	text = text.replace(':', '')
	text = text.replace('?', '')
	text = text.replace(';', '')
	text = text.replace('-', '')
	return text.lower()


def extract_q(f_json):
	q = f_json['all']['question'][0]['Subject']
	q += ' ' + f_json['all']['question'][0]['Content']
	return eliminate_punc(q).split()


def extract_a(f_json):
	a_objs = f_json['all']['answers']
	a = []
	for a_obj in a_objs:
		a.append(eliminate_punc(a_obj['Content']).split())
	return a


def main():
	json_gen = load_json()
	q = []
	a = []
	for f_json in json_gen:
		q.append(extract_q(f_json))
		a.extend(extract_a(f_json))

	lda(q)
	lda(a)


if __name__ == '__main__':
	main()
