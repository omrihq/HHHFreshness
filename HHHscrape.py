import praw
import sys
import datetime
import HTML
import difflib
import youtubeconverter

#Returns a list of submission-types (see: praw) that have the word "[fresh]" in them
def get_fresh(submissions):
	#For links who didn't post fresh on a song so the mods update it with a fresh flair
	fresh = [submission for submission in submissions if ("[fresh" in str(submission).lower()) or ("fresh" in str(submission.link_flair_text).lower())]
	return fresh

def get_date(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)	

def add_sortable_tag(html_code):
	insert_pos = html_code.find("TABLE") + 6
	html_code = html_code[:insert_pos] + 'class=\"sortable\" ' + html_code[insert_pos:]
	return html_code

def add_non_sort_tag(html_code):
	insert_pos = html_code.find("Youtube link")
	html_code = html_code[:insert_pos-1] + ' class=\"sorttable_nosort\"' + html_code[insert_pos-1:]
	return html_code

def create_table(fresh_subs):
	t = HTML.Table(header_row=['Title', 'Score', 'Date Posted', 'Comments', 'Youtube link']) #Need to add artist
	for sub in fresh_subs:
		try:
			date = get_date(sub)

			end_fresh = sub.title.encode('utf-8').find("]")
			if end_fresh != -1:
				title = sub.title.encode('utf-8')[end_fresh+1:]
			else:
				title = sub.title.encode('utf-8')
			link = HTML.link(title, sub.url)

			if youtubeconverter.youtube_url(sub.url):
				url = sub.url
			else:
 				url = youtubeconverter.search(sub.title.encode('ascii', 'ignore'))[0]

			comments = HTML.link(sub.num_comments, sub.permalink)
			url = HTML.link("Track", url)
			t.rows.append([link, sub.score, date, comments, url])
		except Exception,e:
			print sub
			print str(e)
	return str(t)

def similarity(title1, title2):
	title1 = title1.lower().replace("[fresh]", "")
	title2 = title2.lower().replace("[fresh]", "")
	ratio = .75
	return difflib.SequenceMatcher(None, title1.lower(), title2.lower()).ratio() >= ratio



def main():
	#User agent stuff get into reddit
	user_agent = "Freshness by /u/programmeroftheday"
	r = praw.Reddit(user_agent=user_agent)

	#Get the new submissions
	submissions = r.get_subreddit('hiphopheads').get_hot(limit=100)
	fresh_subs = get_fresh(submissions)

	table = create_table(fresh_subs)

	html_code = add_non_sort_tag(add_sortable_tag(table))

	print html_code


if __name__ == '__main__':
	main()

