from sys import argv
from PyQt5.QtWidgets import QApplication
from YouTubeVideosDownload import YouTubeVideosDownload


if __name__ == '__main__':
	app = QApplication(argv)
	# init list folders
	BuildProcess = YouTubeVideosDownload('Gameplay PC french', r'E:\Download')
	# processing download
	BuildProcess.process_download_youtube_gamevideos(True)