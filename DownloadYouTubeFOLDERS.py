from sys import argv
from PyQt5.QtWidgets import QApplication
from YouTubeVideosDownload import YouTubeVideosDownload


if __name__ == '__main__':
	app = QApplication(argv)
	if len(argv)>1:
		# prod
		myfilter = argv[1]
		logname = 'IGGGames'
	else:
		# test envt
		myfilter = 'Gameplay PC french'
		logname = 'IGGGames_TEST'
	# init list folders
	BuildProcess = YouTubeVideosDownload(r'D:\WorkDev\DownloadYouTube', logname, myfilter)
	# processing download
	BuildProcess.process_download_youtube_gamevideos(True)