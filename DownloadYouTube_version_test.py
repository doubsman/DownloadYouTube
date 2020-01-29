from pytube import YouTube
from os import walk, rename, path
from sys import argv
from urllib import request, parse
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, qDebug


# Fonctions mode run main("D:\\WorkDev\\DownloadYouTube")
def listFolders(PathDownload):
	"""Build list folders."""
	for _, dirs, _ in walk(PathDownload):
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
		print('-> ERROR : Some error in downloading: ', videourl)
		qDebug('-> ERROR : Some error in downloading: ', videourl)

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


class DownloadYouTubeVideos(QObject):
	"""build list folders name, search youtube and download first video find format mp4."""
						
	def __init__(self, PathDownload, filtername, parent=None):
		"""Init."""
		super(DownloadYouTubeVideos, self).__init__(parent)
		self.PathDownload = PathDownload
		self.filtername = filtername
		self.parent = parent
		self.dirs = None

	def processDownload(self):
		"""Download video list."""
		# build list
		self.listFolders()
		# download video list
		for ListItem in self.dirs:
			self.processingVideoYoutube(ListItem)

	def listFolders(self):
		"""Build list folders."""
		for _, dirs, _ in walk(self.PathDownload):
			self.dirs = dirs
			break

	def processingVideoYoutube(self, NameSearch):
		"""Search and Download video with NemaSearch.""" 
		NameFinal = path.join(self.PathDownload, NameSearch + '.mp4')
		if not path.exists(NameFinal):
			print("Processing Video    : ", NameSearch)
			# Search youtube obtain first video link
			print(" --Search YouTube   : ", NameSearch + ' ' + self.filtername)
			YoutubeVideo = self.searchYoutube(NameSearch)
			# download video
			print(" --Download Video   : ", YoutubeVideo)
			NameVideos = self.downloadYouTubeMP4(YoutubeVideo, self.PathDownload)
			print(" --Success Download : ", NameVideos)
			# rename
			print(" --Rename Video     : ", NameFinal)
			rename(NameVideos, NameFinal)
			print(" ** operation successfull ** ")

	def searchYoutube(self, searchName):
		"""Search youtube and extract url video."""
		textToSearch = searchName + ' ' + self.filtername
		query = parse.quote(textToSearch)
		url = "https://www.youtube.com/results?search_query=" + query
		response = request.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')
		for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
			#print('https://www.youtube.com' + vid['href'])
			urlfind = 'https://www.youtube.com' + vid['href']
			break
		return urlfind

	def downloadYouTubeMP4(self, videourl):
		"""Download url youtube to file."""
		yt = YouTube(videourl)
		namevideos = path.join(self.PathDownload, yt.title + ".mp4")
		youstreams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
		try: 
			youstreams.download(self.PathDownload)
			return(namevideos)
		except: 
			print('Some error in downloading: ', videourl)
			qDebug('-> ERROR : Some error in downloading: ', videourl)

if __name__ == '__main__':
	app = QApplication(argv)
	# class
	BuuildProcess = DownloadYouTubeVideos(r'D:\WorkDev\DownloadYouTube', 'Gameplay PC french')
	# download list
	BuuildProcess.processDownload()

