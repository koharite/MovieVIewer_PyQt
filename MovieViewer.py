# -*- coding:utf-8 -*-

"""
Created on Dec. 12. 2018
@author : koharite

Function：
Viewer for Movie file using PyQt and OpenCV.

"""

import sys
import cv2

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QHBoxLayout, QLabel, QPushButton, QAction, QStyle, QFileDialog)
from PyQt5.QtGui import(QIcon, QImage, QPixmap, QPainter, QColor)
from PyQt5.QtCore import (pyqtSlot, QTimer, Qt)


# メインウィンドウの構成
class MainWindow(QMainWindow):

    # メインウィンドウの初期値を設定
    def __init__(self):
        # ウィンドウのステータス
        super().__init__()
        self.title = 'Movie Viewer for PDET'
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 960

        # 動画のステータス
        self.framePos = 0
        #self.image = QImage()
        self.image = None
        self.moviePlayFlg = False
        self.imgWidth = 0
        self.imgHeight = 0
        self.frameRate = 0

        self.initUI()

    # 初期化処理をまとめておく
    def initUI(self):
        # メインウィンドウのタイトルを設定する
        self.setWindowTitle(self.title)
        # メインウィンドウの初期位置
        self.setGeometry(self.left, self.top, self.width, self.height)
        hbox = QHBoxLayout(self)

        # メインウィンドウのメニューを設定する
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        optionMenu = mainMenu.addMenu('Option')
        helpMenu = mainMenu.addMenu('Help')

        # ファイルを開くメニューを設定する
        fileOpenButton = QAction(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogStart')), 'File Open', self)
        fileOpenButton.setShortcut('Ctrl+O')
        fileOpenButton.triggered.connect(self.openFileDialog)
        fileMenu.addAction(fileOpenButton)

        # アプリの終了メニューを設定する
        exitButton = QAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogCloseButton')), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # メインウィンドウに部品を配置する
        # 画像描画領域を設定する
        #self.showFrameLabel = QLabel(self)
        #self.painter = QPainter()
        #self.showFramePixmap = QPixmap()
        #self.painter.drawPixmap(0,0, self.imgWidth, self.imgHeight, self.showFramePixmap)
        #self.showFrameLabel.setPixmap(self.showFramePixmap)
        #self.resize(self.showFramePixmap.width(), self.showFramePixmap.height())

        #hbox.addWidget(self.showFrameLabel)
        self.setLayout(hbox)

        # 動画の再生ボタンを設定する
        moviePlayBtn = QPushButton(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')), 'Play', self)
        moviePlayBtn.move(20, self.height-50)
        moviePlayBtn.clicked.connect(self.moviePlay)

        # 動画の停止ボタンを設定する
        movieStopBtn = QPushButton(self.style().standardIcon(getattr(QStyle, 'SP_MediaStop')), 'Stop', self)
        movieStopBtn.move(120, self.height-50)
        movieStopBtn.clicked.connect(self.movieStop)

        # 描画更新用タイマー
        #self.updateTimer = QTimer(self)
        #self.updateTimer.timeout.connect(self.showNextFrame)
        ##self.updateTimer.start(self)

        # メインウィンドウの表示
        self.show()

    def openFileDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        inputFileName, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Movie files(*.avi *.wmv)', options=options)
        # デバッグ用にステータスバーにファイル名を表示する
        #self.statusBar().showMessage(inputFileName[0])
        self.statusBar().showMessage(inputFileName)
        print(inputFileName)

        # OpenCVで動画を読み込む
        self.video = cv2.VideoCapture(inputFileName)
        # デバッグ
        print('OpenCV movie read success.')
        # フレーム数を取得
        self.frameNum = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        # デバッグ
        print('movie frameNum: ', str(self.frameNum))
        # フレームレートを取得
        self.frameRate = self.video.get(cv2.CAP_PROP_FPS)
        # デバッグ
        print('movie frameRate: ', str(self.frameRate))

        # 最初のフレームを表示する
        self.framePos = 0
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.framePos)
        ret, frame = self.video.read()
        # デバッグ
        print('openCV current frame read')
        # 再生フレームをOpenCV形式からPyQtのQImageに変換する
        self.image = self.openCV2Qimage(frame)
        # デバッグ
        print('convert openCV to QImage')
        self.imgWidth = self.image.width()
        self.imgHeith = self.image.height()
        # 表示
        # デバッグ
        print('movie properties read success')
        #self.painter.drawPixmap(0, 0, self.imgWidth, self.imgHeight, self.image)

    def moviePlay(self):
        self.moviePlayFlg = True
        self.updateTimer.start((1/self.frameRate) * 1000)

    def movieStop(self):
        self.moviePlayFlg = False
        self.updateTimer.stop()

    def showNextFrame(self):
        if self.moviePlayFlg == False:
            return

        self.framePos += 1
        # OpenCVで動画の再生フレーム位置を設定する
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.framePos)
        ret, frame = self.video.read()
        # 再生フレームをOpenCV形式からPyQtのQImageに変換する
        self.image = self.openCV2Qimage(frame)
        #self.imgWidth = self.image.width()
        #self.imgHeith  self.image.height()

    def paintEvent(self, event):
        # デバッグ用
        print('paintEvent Start')
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor('#FFFFFF'))
        painter.setBrush(Qt.white)
        painter.drawRect(event.rect())
        # デバッグ用
        print('painter tool set')

        if self.image == None:
            return

        #image = QtGui.QImage('./sample01.jpg')
        #x = (self.width() - self.image.width()) / 2
        #y = (self.height() - self.image.height()) / 2

        #painter.drawImage(x, y, image)
        painter.drawPixmap(0, 0, self.ImgWidth, self.imgHeight, self.image)
        painter.end()



    def openCV2Qimage(self, cvImage):
        height, width, channel = cvImage.shape
        bytesPerLine = channel * width
        cvImageRGB = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        image = QImage(cvImageRGB, width, height, bytesPerLine, QImage.Format_RGB888)
        #image = QImage(cvImage, width, height, bytesPerLine, QImage.Format_RGB888)
        #image = image.rgbSwapped()

        return image



# アプリの実行
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())