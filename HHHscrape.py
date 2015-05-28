import praw
import csv
import sys

#Returns a list of submission-types (see: praw) that have the word "[fresh]" in them
def get_fresh(submissions):
	fresh = [submission for submission in submissions if "[fresh]" in str(submission).lower()]
	return fresh

#def csv_writer():


def main():
	#User agent stuff get into reddit
	user_agent = "Freshness by /u/programmeroftheday"
	r = praw.Reddit(user_agent=user_agent)

	#Get the new submissions
	submissions = r.get_subreddit('hiphopheads').get_new(limit=30)
	fresh_subs = get_fresh(submissions)

	with open('passwordList.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(("Title", "Score", "Date", "Comments"))
		for sub in fresh_subs:
			try:
				#This date is a placeholder until I figure out how to get date from a post without manually scraping with BS4
				writer.writerow((sub.title.encode('utf-8'), sub.score, "5/28/15", sub.num_comments))
			except:
				print sys.exc_info()[0]

if __name__ == '__main__':
	main()

