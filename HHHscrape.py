import praw
import csv
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
"""
	table_data = [
        ['Last name',   'First name',   'Age'],
        ['Smith',       'John',         30],
        ['Carpenter',   'Jack',         47],
        ['Johnson',     'Paul',         62],
    ]
	htmlcode = HTML.table(table_data)
	print htmlcode
"""
	with open('passwordList.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(("Title", "Score", "Date", "Comments"))
		for sub in fresh_subs:
			try:
				date = get_date(sub)
				writer.writerow((sub.title.encode('utf-8'), sub.score, date, sub.num_comments))
			except:
				print sub
				print sys.exc_info()[0]

if __name__ == '__main__':
	main()

