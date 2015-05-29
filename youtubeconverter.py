from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "replace" #Hidden from you 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	developerKey=DEVELOPER_KEY)	

  	# Call the search.list method to retrieve results matching the specified
  	# query term.

	search_response = youtube.search().list(q=options.q, part="id,snippet", maxResults=options.max_results).execute()	
	videos = []
	channels = []
	playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video": 
			#videos.append("%s (%s)" % (search_result["snippet"]["title"], "https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]))
			videos.append("https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])

  	return videos

def search(search_term):
	argparser.add_argument("--q", help="Search term", default=search_term)
	argparser.add_argument("--max-results", help="Max results", default=5)
	args = argparser.parse_args()

	try:
		return youtube_search(args)
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

def if_youtube_url(url):
	if "youtube" in url:
		return True

def convert_to_download(submission):


if __name__ == '__main__':
	print "\n".join(video for video in search("Tinashe Ft. Dej Loaf - All Hands On Deck (Remix)") if if_youtube_url(video))

