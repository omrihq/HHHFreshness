import mechanize
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.


def youtube_search(search_string, max_results=5):
	DEVELOPER_KEY = "Replace me" #Hidden from you 
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"

	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)	

  	# Call the search.list method to retrieve results matching the specified
  	# query term.
  	search_response = youtube.search().list(q=search_string, part="id,snippet", maxResults=max_results).execute()
	#search_response = youtube.search().list(q=options.q, part="id,snippet", maxResults=options.max_results).execute()	
	videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video": 
			#videos.append("%s (%s)" % (search_result["snippet"]["title"], "https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]))
			videos.append("https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
	try:
  		return videos
  	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


def convert_to_download(vidID):

	vid =  pafy.new(vidID)
	music = vid.getbestaudio()
	song = music.getbest("m4a").download()

if __name__ == '__main__':
	print "\n".join(video for video in search("Ace hood - 4 A Minute"))
#	print "\n".join(video for video in search("Ted talks") if youtube_url(video))
