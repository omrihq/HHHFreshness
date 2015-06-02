import mechanize
import httplib2
import os
import pafy

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow




# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.


def youtube_search(search_string, max_results=5):
	API_KEY = open("API_KEY.txt", "r")
	DEVELOPER_KEY = API_KEY.read()
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

def create_playlist():
	# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
	# the OAuth 2.0 information for this application, including its client_id and
	# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
	# the Google Developers Console at
	# https://console.developers.google.com/.
	# Please ensure that you have enabled the YouTube Data API for your project.
	# For more information about using OAuth2 to access the YouTube Data API, see:
	#   https://developers.google.com/youtube/v3/guides/authentication
	# For more information about the client_secrets.json file format, see:
	#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
	CLIENT_SECRETS_FILE = "client_secrets.json"
	
	# This variable defines a message to display if the CLIENT_SECRETS_FILE is
	# missing.
	MISSING_CLIENT_SECRETS_MESSAGE = """
	WARNING: Please configure OAuth 2.0
	
	To make this sample run you will need to populate the client_secrets.json file
	found at:
	
	   %s
	
	with information from the Developers Console
	https://console.developers.google.com/
	
	For more information about the client_secrets.json file format, please visit:
	https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
	""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
	                                   CLIENT_SECRETS_FILE))
	
	# This OAuth 2.0 access scope allows for full read/write access to the
	# authenticated user's account.
	YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"
	
	flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, message=MISSING_CLIENT_SECRETS_MESSAGE, scope=YOUTUBE_READ_WRITE_SCOPE)
	
	storage = Storage("oauth2.json") #% sys.argv[0])
	credentials = storage.get()
	
	if credentials is None or credentials.invalid:
	  flags = argparser.parse_args()
	  credentials = run_flow(flow, storage, flags)
	
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))
	
	# This code creates a new, private playlist in the authorized user's channel.
	playlists_insert_response = youtube.playlists().insert(
	  part="snippet,status",
	  body=dict(
	    snippet=dict(
	      title="Test Playlist",
	      description="A private playlist created with the YouTube API v3"
	    ),
	    status=dict(
	      privacyStatus="private"
	    )
	  )
	).execute()

	print "New playlist id: %s" % playlists_insert_response["id"]



#if __name__ == '__main__':
#	create_playlist()
