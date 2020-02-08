
from os import rename, path
from sys import path as syspath
from urllib.request import Request, urlopen
from urllib import parse
from pytube import YouTube
from bs4 import BeautifulSoup
from PyQt5.QtCore import QObject, qDebug, QDateTime
# log
syspath.append(path.dirname(path.dirname(path.abspath(__file__))))
from LogPrintFile.LogPrintFile import LogPrintFile
from FilesProcessing.FilesProcessing import FilesProcessing

class YouTubeVideosDownload(QObject):
	"""Youtube list download."""
						
	def __init__(self, PathDownload = None, logname = 'DEV', filtername = '', parent=None):
		"""Init."""
		super(YouTubeVideosDownload, self).__init__(parent)
		self.parent = parent
		self.listgames = []
		self.dirs = []
		self.filtername = filtername
		self.PathDownload = PathDownload
		self.logProcess = LogPrintFile(path.join(path.dirname(path.abspath(__file__)), 'LOG'), logname, True, 7)
		if PathDownload:
			self.FilesProcess = FilesProcessing(self)

	def process_download_youtube_gamevideos(self, download = False):
		"""Download video list."""
		# download video list
		self.dirs = self.FilesProcess.folder_list_folders(self.PathDownload)
		for ListItem in self.dirs:
			self.processingVideoYoutube(ListItem, download)

	def process_download_youtube_gameIGG(self, download = False):
		"""Search youtube and extract url video."""
		self.logProcess.write_log_file('GAME IGG', '', False)
		soup = self.get_webhtml("https://igg-games.com/")
		for vid in soup.findAll(attrs={'class':'wk-display-block wk-link-reset'}):
			game  = vid.img['alt'].replace(' Free Download','')
			self.listgames.append(game)
			self.processingVideoYoutube(game, download)
			self.logProcess.write_log_file('-'*22, '', False)
		self.logProcess.view_log_file()

	def processingVideoYoutube(self, NameSearch, download = False):
		"""Search and Download video with NemaSearch.""" 
		self.logProcess.write_log_file('Processing Video', NameSearch)
		# Search youtube obtain first video link
		self.logProcess.write_log_file('Search YouTube', NameSearch + ' ' + self.filtername)
		YoutubeVideo = self.searchYoutube(NameSearch)
		self.logProcess.write_log_file('url YouTube', YoutubeVideo)
		if download:
			NameFinal = path.join(self.PathDownload, NameSearch + '.mp4')
			if not path.exists(NameFinal):
				# download video
				self.logProcess.write_log_file('Download Video', YoutubeVideo)
				NameVideos = self.downloadYouTubeMP4(YoutubeVideo)
				self.logProcess.write_log_file('Success Download', NameVideos)
				# rename
				self.logProcess.write_log_file('Rename Video', NameFinal)
				rename(NameVideos, NameFinal)

	def searchYoutube(self, searchName):
		"""Search youtube and extract url video."""
		vid = None
		textToSearch = searchName + ' ' + self.filtername
		soup = self.get_webhtml("https://www.youtube.com/results?search_query=", textToSearch)
		for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
			#print('https://www.youtube.com' + vid['href'])
			break
		if vid is None:
			return 'unknow'
		else:
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
			self.logProcess.write_log_file('Some error in downloading: ', videourl)
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



