import sys
from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.currentPlaylist = QMediaPlaylist()
		self.player = QMediaPlayer()
		self.userAction = -1			
		self.player.mediaStatusChanged.connect(self.qmp_mediaStatusChanged)
		self.player.stateChanged.connect(self.qmp_stateChanged)
		self.player.positionChanged.connect(self.qmp_positionChanged)
		self.player.setVolume(60)
		self.statusBar().showMessage('No Media :: %d'%self.player.volume())
		self.homeScreen()
		
	def homeScreen(self):
		self.createMenubar()
		self.createToolbar()
		controlBar = self.addControls()
		centralWidget = QWidget()
		centralWidget.setLayout(controlBar)
		self.setCentralWidget(centralWidget)
		self.resize(640,400)
		self.show()
		
	def createMenubar(self):
		menubar = self.menuBar()
		filemenu = menubar.addMenu('File')
		filemenu.addAction(self.fileOpen())
	
	def createToolbar(self):
		pass
	
	def addControls(self):
		controlArea = QVBoxLayout()		
		seekSliderLayout = QHBoxLayout()
		controls = QHBoxLayout()
		#playlistCtrlLayout = QHBoxLayout()
		
		label1 = QLabel()
		pixmap = QPixmap('foo1.png') #changes dynamically
		label1.setPixmap(pixmap)
		
		playBtn = QPushButton('Play')		
		stopBtn = QPushButton('Stop')		

		seekSlider = QSlider()
		seekSlider.setMinimum(0)
		seekSlider.setMaximum(100)
		seekSlider.setOrientation(Qt.Horizontal)
		seekSlider.setTracking(False)
		seekSlider.sliderMoved.connect(self.seekPosition)
		
		seekSliderLabel1 = QLabel('0.00')
		seekSliderLabel2 = QLabel('0.00')
		seekSliderLayout.addWidget(seekSliderLabel1)
		seekSliderLayout.addWidget(seekSlider)
		seekSliderLayout.addWidget(seekSliderLabel2)
		
		playBtn.clicked.connect(self.playHandler)
		stopBtn.clicked.connect(self.stopHandler)

		controls.addWidget(playBtn)
		controls.addWidget(stopBtn)

		controlArea.addWidget(label1)
		controlArea.addLayout(seekSliderLayout)
		controlArea.addLayout(controls)
		#controlArea.addLayout(playlistCtrlLayout)
		return controlArea
	
	def playHandler(self):
		self.userAction = 1
		self.statusBar().showMessage('Playing at Volume %d'%self.player.volume())
		if self.player.state() == QMediaPlayer.StoppedState :
			if self.player.mediaStatus() == QMediaPlayer.NoMedia:
				print(self.currentPlaylist.mediaCount())
				if self.currentPlaylist.mediaCount() == 0:
					self.openFile()
				if self.currentPlaylist.mediaCount() != 0:
					self.player.setPlaylist(self.currentPlaylist)
			elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
				self.player.play()
			elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
				self.player.play()
		elif self.player.state() == QMediaPlayer.PlayingState:
			pass
		elif self.player.state() == QMediaPlayer.PausedState:
			self.player.play()
			
	def stopHandler(self):
		self.userAction = 0
		self.statusBar().showMessage('Stopped at Volume %d'%(self.player.volume()))
		if self.player.state() == QMediaPlayer.PlayingState:
			self.stopState = True
			self.player.stop()
		elif self.player.state() == QMediaPlayer.PausedState:
			self.player.stop()
		elif self.player.state() == QMediaPlayer.StoppedState:
			pass
		
	def qmp_mediaStatusChanged(self):
		if self.player.mediaStatus() == QMediaPlayer.LoadedMedia and self.userAction == 1:
			durationT = self.player.duration()
			self.centralWidget().layout().itemAt(0).layout().itemAt(1).widget().setRange(0,durationT)
			self.centralWidget().layout().itemAt(0).layout().itemAt(2).widget().setText('%d:%02d'%(int(durationT/60000),int((durationT/1000)%60)))
			self.player.play()
			
	def qmp_stateChanged(self):
		if self.player.state() == QMediaPlayer.StoppedState:
			self.player.stop()
		
	def qmp_positionChanged(self, position,senderType=False):
		sliderLayout = self.centralWidget().layout().itemAt(0).layout()
		if senderType == False:
			sliderLayout.itemAt(1).widget().setValue(position)
		#update the text label
		sliderLayout.itemAt(0).widget().setText('%d:%02d'%(int(position/60000),int((position/1000)%60)))
	
	def seekPosition(self, position):
		sender = self.sender()
		if isinstance(sender,QSlider):
			if self.player.isSeekable():
				self.player.setPosition(position)

	def fileOpen(self):
		fileAc = QAction('Open File',self)
		fileAc.setShortcut('Ctrl+O')
		fileAc.setStatusTip('Open File')
		fileAc.triggered.connect(self.openFile)
		return fileAc
		
	def openFile(self):
		fileChoosen = QFileDialog.getOpenFileUrl(self,'Open Music File', expanduser('~'),'Audio (*.mp3 *.ogg *.wav)','*.mp3 *.ogg *.wav')
		if fileChoosen != None:
			self.currentPlaylist.addMedia(QMediaContent(fileChoosen[0]))

	def closeEvent(self,event):
		reply = QMessageBox.question(self,'Message','Pres Yes to Close.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
		
		if reply == QMessageBox.Yes :
			qApp.quit()
		else :
			try:
				event.ignore()
			except AttributeError:
				pass
			
	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())