from pytube import YouTube
from os import walk, rename, path
from urllib import request, parse
from bs4 import BeautifulSoup

def listFolders(PathDownload):
	"""Build list folders."""
	for root, dirs, files in walk(PathDownload):
		return dirs

def searchYoutube(name):
	"""Search youtube and extract url video."""
	textToSearch = name + ' Gameplay PC french'
	query = parse.quote(textToSearch)
	url = "https://www.youtube.com/results?search_query=" + query
	response = request.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		#print('https://www.youtube.com' + vid['href'])
		return 'https://www.youtube.com' + vid['href']

def downloadYouTubeMP4(videourl, PathDownload):
	"""Download url youtube to file."""
	yt = YouTube(videourl)
	namevideos = path.join(PathDownload, yt.title + ".mp4")
	youstreams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
	try: 
		youstreams.download(PathDownload)
		return(namevideos)
	except: 
		print('Some error in downloading: ', videourl)

def downloadVideoYoutube(NameSearch, PathDownload):
	"""Search and Download video with NemaSearch.""" 
	NameFinal = path.join(PathDownload, NameSearch + '.mp4')
	if not path.exists(NameFinal):
		print("Processing Video    : ", NameSearch)
		# Search youtube obtain first video link
		print(" --Search YouTube   : ", NameSearch)
		YoutubeVideo = searchYoutube(NameSearch)
		# download video
		print(" --Download Video   : ", YoutubeVideo)
		NameVideos = downloadYouTubeMP4(YoutubeVideo,PathDownload)
		print(" --Success Download : ", NameVideos)
		# rename
		print(" --Rename Video     : ", NameFinal)
		rename(NameVideos,NameFinal)
		print(" ** operation successfull ** ")

def main(PathDownload):
	# build list
	ListItems = listFolders(PathDownload)
	# download video list
	for ListItem in ListItems:
		downloadVideoYoutube(ListItem, PathDownload)

# download
main("e:\\working")
