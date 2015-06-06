import praw
import sys
import datetime
import HTML
import difflib
import youtubeconverter
import soundcloud
import json
import socket
from time import sleep


#The span to include in the thing
#<span onclick="reply_click(this.id)" id="soundcloud1" class="fa-stack fa-1x"> <i class="fa fa-circle fa-stack-2x"></i> <i class="fa fa-soundcloud fa-inverse fa-stack-1x"></i></span>

#Returns a list of submission-types (see: praw) that have the word "[fresh]" in them
def get_fresh(submissions):
	#For links who didn't post fresh on a song so the mods update it with a fresh flair
	fresh = [submission for submission in submissions if ("[fresh" in str(submission.title.encode('ascii', 'ignore')).lower()) or (submission.link_flair_text and "fresh" in str(submission.link_flair_text.encode('ascii', 'ignore')).lower())]

	return set(fresh)

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

def is_connected():
  REMOTE_SERVER = "www.google.com"
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False


def get_soundcloud_id(sub):
	title = cut_fresh(sub)
	invalid_id_selectors = "~ ! @ $ % ^ & * ( ) + = , . / ' ; : \" ? > < [ ] \ { } | ` #".split()
	#Add a space
	invalid_id_selectors.append(chr(32))
	spanID = ''.join([c.lower() for c in title if c not in invalid_id_selectors])
	return spanID

def get_youtube_id(url):
	spanID = url[url.find("v=")+2:]

	invalid_id_selectors = "~ ! @ $ % ^ & * ( ) + = , . / ' ; : \" ? > < [ ] \ { } | ` #".split()
	#Add a space
	invalid_id_selectors.append(chr(32))
	tubeID = ''.join([c for c in spanID if c not in invalid_id_selectors])
	return tubeID

def create_soundcloud_span(sub):
	spanID = get_soundcloud_id(sub)

	soundcloud_tag = "<i class=\"fa fa-circle fa-stack-2x\"></i> <i class=\"fa fa-soundcloud fa-inverse fa-stack-1x\"></i>"
	final_span = "<span onClick=\"reply_click(this.id)\" value=\"off\" id=\"" + spanID + "\"class=\"fa-stack fa-1x\">" + soundcloud_tag + "</span>"
	span_with_frame = final_span + get_soundcloud_widget(sub)
	return span_with_frame

def create_youtube_span(url):
	spanID = url[url.find("v=")+2:]

	invalid_id_selectors = "~ ! @ $ % ^ & * ( ) + = , . / ' ; : \" ? > < [ ] \ { } | ` #".split()
	#Add a space
	invalid_id_selectors.append(chr(32))
	spanID = ''.join([c for c in spanID if c not in invalid_id_selectors])

	youtube_tag = "<i class=\"fa fa-circle fa-stack-2x\"></i> <i class=\"fa fa-youtube-play fa-inverse fa-stack-1x\"></i>"
	final_span = "<span onclick=\"reply_click(this.id)\" value=\"off\" id=\"a" + spanID + "\"class=\"fa-stack fa-1x\">" + youtube_tag + "</span><br>"
	span_with_frame = final_span + get_youtube_widget(spanID)
	return span_with_frame

def get_youtube_widget(tubeID):

	invalid_id_selectors = "~ ! @ $ % ^ & * ( ) + = , . / ' ; : \" ? > < [ ] \ { } | ` #".split()
	#Add a space
	invalid_id_selectors.append(chr(32))
	tubeID = ''.join([c for c in tubeID if c not in invalid_id_selectors])

	#Start all widget ids with "a" to avoid ids starting with numbers
	frame = "<iframe id=\"a" + tubeID + "-frame\" width=\"400\" height=\"315\" src=\"https://www.youtube.com/embed/" + tubeID + "\" frameborder=\"0\" allowfullscreen></iframe>"
	return frame

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
		#Insert the ID into the frame so the css can insert it
		endframeID = beg_frame[:7] + " id=\"" + frameID + "-frame\"" + beg_frame[7:]
		return endframeID
	except Exception,e:
		print str(e)


def cut_fresh(sub):
	#Find where the [FRESH] ends and remove it from the title by finding where the "]" is (To account for [Fresh Mixtape], [FRESH Album], etc)
	end_fresh = sub.title.encode('ascii', 'ignore').find("]")
	if end_fresh != -1:
		title = sub.title.encode('ascii', 'ignore')[end_fresh+1:]
		return title
	else:
		title = sub.title.encode('ascii', 'ignore')
		return title


def create_table(fresh_subs):
	t = HTML.Table(header_row=['Title', 'Score', 'Date Posted', 'Comments']) #Need to add artist
	css_ids = []
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
 			except Exception, e: 
 				print str(e), title
			

			if soundcloud_url(url):
				span = create_soundcloud_span(sub)
				css_ids.append(get_soundcloud_id(sub))
			elif youtube_url(url):
				span = create_youtube_span(url)
				#Youtube IDs
				css_ids.append("a" + get_youtube_id(url))


			comments = HTML.link(sub.num_comments, sub.permalink)
			link = HTML.link(title, url)
			linkspan = link + span

			t.rows.append([linkspan.encode('ascii', 'ignore'), sub.score, date, comments.encode('ascii', 'ignore')])
		except Exception,e:
			print sub
			print str(e)
	return str(t), css_ids


def similarity(sub1, sub2):
	title1 = cut_fresh(sub1).lower()
	title2 = cut_fresh(sub2).lower()
	ratio = .62
	return difflib.SequenceMatcher(None, title1, title2).ratio() >= ratio

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
	try:
		user_agent = "Freshness by /u/programmeroftheday"
		r = praw.Reddit(user_agent=user_agent)
	
		#Get the new submissions
		submissions = r.get_subreddit('hiphopheads').get_hot(limit=100)
		fresh_subs = get_fresh(submissions)
	
		table, frame_ids = create_table(fresh_subs)
	
		html_code = add_sortable_tag(table)
	
		insert_table(html_code)
	
		insert_css_rules(frame_ids)
	except Exception, e:
		print str(e)


if __name__ == '__main__':
	if is_connected():
		main()
	else:
		#Sleep for 30 minutes then try again
		sleep(1800)
		if is_connected():
			main()
		else:
			sys.exit()
