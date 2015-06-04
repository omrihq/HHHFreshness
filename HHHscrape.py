import praw
import sys
import datetime
import HTML
import difflib
import youtubeconverter
import soundcloud
import json


#The span to include in the thing
#<span onclick="reply_click(this.id)" id="soundcloud1" class="fa-stack fa-1x"> <i class="fa fa-circle fa-stack-2x"></i> <i class="fa fa-soundcloud fa-inverse fa-stack-1x"></i></span>

#Returns a list of submission-types (see: praw) that have the word "[fresh]" in them
def get_fresh(submissions):
	#For links who didn't post fresh on a song so the mods update it with a fresh flair
	fresh = [submission for submission in submissions if ("[fresh" in str(submission.title.encode('ascii', 'ignore')).lower()) or (submission.link_flair_text and "fresh" in str(submission.link_flair_text.encode('ascii', 'ignore')).lower())]
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

def vimeo_url(url):
	return "vimeo" in url

def get_soundcloud_id(sub):
	title = cut_fresh(sub)
	invalid_id_selectors = "~ ! @ $ % ^ & * ( ) + = , . / ' ; : \" ? > < [ ] \ { } | ` #".split()
	#Add a space
	invalid_id_selectors.append(chr(32))
	spanID = ''.join([c.lower() for c in title if c not in invalid_id_selectors])
	return spanID


def create_span_button(sub):
	if youtube_url(sub.url):
		url = sub.url
		spanID = url[url.find("v=")+2:]
		youtube_tag = "<i class=\"fa fa-circle fa-stack-2x\"></i> <i class=\"fa fa-youtube-play fa-inverse fa-stack-1x\"></i>"
		final_span = "<span onclick=\"reply_click(this.id)\" id=\"" + spanID + "\"class=\"fa-stack fa-1x\">" + youtube_tag + "</span>"
		return final_span
	elif soundcloud_url(sub.url):
		spanID = get_soundcloud_id(sub)

		soundcloud_tag = "<i class=\"fa fa-circle fa-stack-2x\"></i> <i class=\"fa fa-soundcloud fa-inverse fa-stack-1x\"></i>"
		final_span = "<span onClick=\"reply_click(this.id)\" value=\"off\" id=\"" + spanID + "\"class=\"fa-stack fa-1x\">" + soundcloud_tag + "</span>"
		span_with_frame = final_span + get_soundcloud_widget(sub)
		return span_with_frame


def get_soundcloud_widget(sub):
	# create a client object with your app credentials
	try:
		url = sub.url
		client = soundcloud.Client(client_id='YOUR_CLIENT_ID')
	
		# get a tracks oembed data
		embed_info = client.get('/oembed', url=url)
		
		# print the html for the player widget
		beg_frame = embed_info.html
		frameID = get_soundcloud_id(sub)
		endframeID = beg_frame[:7] + " id=\"" + frameID + "-frame\"" + beg_frame[7:]
		return endframeID
	except Exception,e:
		print str(e)


def cut_fresh(sub):
	#Find where the [FRESH] ends and remove it from the title by finding where the "]" is (To account for [Fresh Mixtape], [FRESH Album], etc)
	end_fresh = sub.title.encode('ascii').find("]")
	if end_fresh != -1:
		title = sub.title.encode('ascii')[end_fresh+1:]
		return title
	else:
		title = sub.title.encode('ascii')
		return title


def create_table(fresh_subs):
	t = HTML.Table(header_row=['Title', 'Score', 'Date Posted', 'Comments']) #Need to add artist
	css_soundcloud_ids = []
	for sub in fresh_subs:
		try:
			date = get_date(sub)
			
			title = cut_fresh(sub)

			try:
				if youtube_url(sub.url) or soundcloud_url(sub.url):
					url = sub.url
				else:
					tubeID = youtubeconverter.youtube_search(title)[0]
 					url = "https://www.youtube.com/watch?v=" + tubeID
 					print url
 			except: 
 				pass
			
			span = create_span_button(sub)

			if soundcloud_url(sub.url):
				css_soundcloud_ids.append(get_soundcloud_id(sub))

			comments = HTML.link(sub.num_comments, sub.permalink)
			link = HTML.link(title, url)

			t.rows.append([link + span, sub.score, date, comments])
		except Exception,e:
			print sub
			print str(e)
	return str(t), css_soundcloud_ids


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
	txt.close()

	#The sooner you replace this the better	
	new_index = open(filename, 'w')
	new_index.write(newhtml)


def insert_css_rules(frame_ids):
	filename = "HHHSite/css/custom.css"
	txt = open(filename, 'r')
	start = txt.read().find("hand;}")
	txt.seek(0,0)
	newhtml = txt.read()[:start+7]
	for ID in frame_ids:
		txt.seek(0,0)
		newhtml += "#" + ID + "-frame { height: 0px; overflow: hidden; transition: all .5s linear; }" + "\n"

	txt.close()

	new_index = open(filename, 'w')
	new_index.write(newhtml)




def main():
	#User agent stuff get into reddit
	user_agent = "Freshness by /u/programmeroftheday"
	r = praw.Reddit(user_agent=user_agent)

	#Get the new submissions
	submissions = r.get_subreddit('hiphopheads').get_hot(limit=100)
	fresh_subs = get_fresh(submissions)

	table, frame_ids = create_table(fresh_subs)

	#No column with no sort tag yet, will save for DL conversion
	html_code = add_sortable_tag(table)

	insert_table(html_code)

	insert_css_rules(frame_ids)



if __name__ == '__main__':
	main()

