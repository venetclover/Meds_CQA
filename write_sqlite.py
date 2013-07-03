from datetime import datetime

import sqlite3


class writer():
	def __init__(self):
		self.conn = sqlite3.connect('ans_meds')
		self.c = self.conn.cursor()


	def write_question(self, qid, subject, content='', date=datetime.now(), category='396545018', userid='', chosenans=''):
		try:
			self.c.execute("INSERT into QUESTION VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (qid, subject, content, date, category, userid, chosenans, datetime.now(), 0))
		except sqlite3.IntegrityError:
			self.c.execute("SELECT REPEATED from QUESTION WHERE ID=?", (qid,))
			repeated = self.c.fetchone()
			self.c.execute("UPDATE QUESTION SET REPEATED=? WHERE ID=?", (repeated[0]+1, qid))
			return 1

		return 0


	def write_answer(self, qid, content='', best=0, aid='', date=datetime.now()):
		try:
			self.c.execute("INSERT into ANSWER VALUES (?, ?, ?, ?, ?)", (qid, content, best, aid, date))
		except:
			return 1

		return 0


	def commit(self):
		self.conn.commit()

	
	def close(self):
		self.c.close()


def main():
	db_writer = writer()
	result = db_writer.write_question(qid='123', subject='test', content='test contect', date=datetime.now(), category='345', userid='aurora', chosenans='ans1')
	db_writer.commit()

	if not result:
		db_writer.write_answer(qid='123', content='test ans', best=5, aid='lin', date=datetime.now())
		db_writer.commit()


if __name__ == '__main__':
	main()
