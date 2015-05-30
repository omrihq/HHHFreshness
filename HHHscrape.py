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
	#Not useful until mp3conversion
	insert_pos = html_code.find("Song Link")
	html_code = html_code[:insert_pos-1] + ' class=\"sorttable_nosort\"' + html_code[insert_pos-1:]
	return html_code

def youtube_url(url):
	return "youtube" in url

def soundcloud_url(url):
	return "soundcloud" in url

def audiomack_url(url):
	return "audiomack" in url

def create_table(fresh_subs):
	t = HTML.Table(header_row=['Title', 'Score', 'Date Posted', 'Comments']) #Need to add artist
	for sub in fresh_subs:
		try:
			date = get_date(sub)

			#Find where the [FRESH] ends and remove it from the title by finding where the "]" is (To account for [Fresh Mixtape], [FRESH Album], etc)
			end_fresh = sub.title.encode('utf-8').find("]")
			if end_fresh != -1:
				title = sub.title.encode('utf-8')[end_fresh+1:]
			else:
				title = sub.title.encode('utf-8')


			if youtube_url(sub.url) or soundcloud_url(sub.url) or audiomack_url(sub.url):
				url = sub.url
			else:
 				url = youtubeconverter.youtube_search(title)[0]
 				#print title, url


			comments = HTML.link(sub.num_comments, sub.permalink)
			link = HTML.link(title, url)

			t.rows.append([link, sub.score, date, comments])
		except Exception,e:
			print sub
			print str(e)
	return str(t)

def similarity(title1, title2):
	title1 = title1.lower().replace("[fresh]", "")
	title2 = title2.lower().replace("[fresh]", "")
	ratio = .75
	return difflib.SequenceMatcher(None, title1.lower(), title2.lower()).ratio() >= ratio

def insert_table(html_table):
	#VERY SKETCHY/find an alternative, this hack is an abomination
	filename = "HHHSite/index.html"
	txt = open(filename, 'r')
	start = txt.read().find("<TABLE")
	txt.seek(0,0)
	end = txt.read().find("</TABLE>")
	txt.seek(0,0)
	newhtml = txt.read()[:start]
	txt.seek(0,0)
	newhtml += html_table
	txt.seek(0,0)
	newhtml += txt.read()[end+8:]
	print newhtml

#	newHtml = txt.read()[:start+1] + html_table
#	txt.seek(0,0)
#	newHtml += txt.read()[end+1:]
#	txt.close()
#
#	print newHtml
	#newtxt = open(filename, 'w')
	#newtxt.write(newHtml)
	#print newHtml


def main():
	#User agent stuff get into reddit
	user_agent = "Freshness by /u/programmeroftheday"
	r = praw.Reddit(user_agent=user_agent)

	#Get the new submissions
	submissions = r.get_subreddit('hiphopheads').get_hot(limit=100)
	fresh_subs = get_fresh(submissions)

	table = create_table(fresh_subs)

	#No column with no sort tag yet, will save for DL conversion
	html_code = add_sortable_tag(table)

	insert_table(html_code)


if __name__ == '__main__':
	main()

