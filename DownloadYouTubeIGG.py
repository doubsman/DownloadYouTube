from sys import argv
from PyQt5.QtWidgets import QApplication
from YouTubeVideosDownload import YouTubeVideosDownload


if __name__ == '__main__':
	app = QApplication(argv)
	# init class
	BuildProcess = YouTubeVideosDownload('Gameplay PC french')
	# no download
	BuildProcess.process_download_youtube_gameIGG(False)

