from sys import argv
from os import path, startfile
from urllib.request import Request, urlopen
from urllib import parse
from codecs import open
from pytube import YouTube
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, qDebug, QDateTime


class YouTubeVideosDownload(QObject):
	"""build list games name IGG-GAME."""
						
	def __init__(self, PathDownload = '', filtername = '', parent=None):
		"""Init."""
		super(YouTubeVideosDownload, self).__init__(parent)
		self.parent = parent
		self.listgames = []
		self.filtername = filtername
		self.PathDownload = PathDownload
		self.logFileName = QDateTime.currentDateTime().toString('yyMMddhhmmss') + "_IGGGames.log"
		self.logFileName = path.join(path.dirname(path.abspath(__file__)), "LOG", self.logFileName)

	def process_download_youtube_gamevideos(self):
		"""Download video list."""
		# build list
		self.listFolders()
		# download video list
		for ListItem in self.dirs:
			self.processingVideoYoutube(ListItem)

	def process_download_youtube_gameIGG(self, download = False):
		"""Search youtube and extract url video."""
		self.write_log_file('GAME IGG', '', False)
		soup = self.get_webhtml("https://igg-games.com/")
		for vid in soup.findAll(attrs={'class':'wk-display-block wk-link-reset'}):
			game  = vid.img['alt'].replace(' Free Download','')
			self.listgames.append(game)
			self.processingVideoYoutube(game, download)
			self.write_log_file('-'*22, '', False)
		startfile(self.logFileName)

	def processingVideoYoutube(self, NameSearch, download = True):
		"""Search and Download video with NemaSearch.""" 
		self.write_log_file('Processing Video', NameSearch)
		# Search youtube obtain first video link
		self.write_log_file('Search YouTube', NameSearch + ' ' + self.filtername)
		YoutubeVideo = self.searchYoutube(NameSearch)
		self.write_log_file('url YouTube', YoutubeVideo)
		if download:
			NameFinal = path.join(self.PathDownload, NameSearch + '.mp4')
			if not path.exists(NameFinal):
				# download video
				self.write_log_file('Download Video', YoutubeVideo)
				NameVideos = self.downloadYouTubeMP4(YoutubeVideo, self.PathDownload)
				self.write_log_file('Success Download', NameVideos)
				# rename
				self.write_log_file('Rename Video', NameFinal)
				rename(NameVideos, NameFinal)

	def listFolders(self):
		"""Build list folders."""
		for _, dirs, _ in walk(self.PathDownload):
			self.dirs = dirs
			break

	def searchYoutube(self, searchName):
		"""Search youtube and extract url video."""
		textToSearch = searchName + ' ' + self.filtername
		soup = self.get_webhtml("https://www.youtube.com/results?search_query=", textToSearch)
		for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
			#print('https://www.youtube.com' + vid['href'])
			break
		return 'https://www.youtube.com' + vid['href']

	def downloadYouTubeMP4(self, videourl):
		"""Download url youtube to file."""
		yt = YouTube(videourl)
		namevideos = path.join(self.PathDownload, yt.title + ".mp4")
		youstreams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
		try: 
			youstreams.download(self.PathDownload)
			return(namevideos)
		except: 
			self.write_log_file('Some error in downloading: ', videourl)
			qDebug('-> ERROR : Some error in downloading: ', videourl)

	def get_webhtml(self, url, query = None):
		"""Product soup dict from web url."""
		if query:
			query = parse.quote(query)
			url += query
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		soup = BeautifulSoup(webpage, 'html.parser')
		return soup

	def write_log_file(self, operation, line, modification = True, writeconsole = True):
		"""Write log file."""
		if modification:
			logline = '{:>22} : {}  '.format(operation, line)
		else:
			if line == "":
				logline = operation + "\n"
			else:
				logline = '{} "{}"'.format(operation, line)
		text_file = open(self.logFileName, "a", 'utf-8')
		text_file.write(logline+"\n")
		text_file.close()
		if writeconsole:
			print(logline)

if __name__ == '__main__':
	app = QApplication(argv)
	# download list folders
	#BuildProcess = YouTubeVideosDownload("E:\\Download", 'Gameplay PC french')
	#BuildProcess.process_download_youtube_gamevideos()
	# search url video youtube
	BuildProcess = YouTubeVideosDownload()
	BuildProcess.process_download_youtube_gameIGG()

