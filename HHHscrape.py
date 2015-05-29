import praw
import sys
import datetime
import HTML

#Returns a list of submission-types (see: praw) that have the word "[fresh]" in them
def get_fresh(submissions):
	fresh = [submission for submission in submissions if "[fresh]" in str(submission).lower()]
	return fresh

def get_date(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)	

def main():
	#User agent stuff get into reddit
	user_agent = "Freshness by /u/programmeroftheday"
	r = praw.Reddit(user_agent=user_agent)

	#Get the new submissions
	submissions = r.get_subreddit('hiphopheads').get_new(limit=30)
	fresh_subs = get_fresh(submissions)

	#Testing HTML.py
	t = HTML.Table(header_row=['Title', 'Score', 'Date Posted', 'Comments']) #Need to add artist

	for sub in fresh_subs:
		try:
			date = get_date(sub)
			t.rows.append([sub.title.encode('utf-8'), sub.score, date, sub.num_comments])
		except Exception,e:
			print sub
			print str(e)
	html_code = str(t)
	print html_code	


if __name__ == '__main__':
	main()

