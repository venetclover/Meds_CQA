class yahoo_q:
	def __init__(self, q_id, cate, date, auth, chosen_ans):
		self.q_id = q_id
		self.category = cate
		self.date = date
		self.auth = auth
		self.chosen_ans = chosen_ans
		self.read = 0
		self.answers = []

	def set_read_score(self, score):
		self.read = score

	def add_answers(self, ans):
		self.answers.append(ans)
	

class yahoo_a:
	def __init__(self, answerer_id, date, best):
		self.anth = answerer_id
		self.date = date
		self.best = best
		self.read = 0

	def set_read_score(self, score):
		self.read = score
