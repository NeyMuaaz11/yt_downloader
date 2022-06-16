# import libraries
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys, os
import requests
from pytube import YouTube
from pytube.exceptions import PytubeError

# window class
class Window(QMainWindow):
    # constructor to initialize the basic layout of the window
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("YouTube Audio & Video Downloader")
        self.setWindowIcon(PyQt5.QtGui.QIcon("icon.jpg"))
        self.setGeometry(600,200,800,700)
        self.setStyleSheet("background-color: rgb(153, 0, 0)")
        self.initUI()

    # initialize the widgets in the window
    def initUI(self):
        # create search bar where user searches for video
        self.search_bar = QtWidgets.QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for a video...")
        self.search_bar.resize(400,30)
        self.search_bar.setStyleSheet("background-color: white; border-radius: 10px")
        self.search_bar.move(200,90)

        # create mp3 and mp4 radio buttons so user can choose which format to download
        self.mp3 = QtWidgets.QRadioButton(self)
        self.mp3.setText("mp3")
        self.mp3.setCheckable(True)
        self.mp3.setStyleSheet("background:transparent")
        self.mp3.move(380, 130)

        self.mp4 = QtWidgets.QRadioButton(self)
        self.mp4.setStyleSheet("background:transparent")
        self.mp4.setCheckable(True)
        self.mp4.setText("mp4")
        self.mp4.move(440,130)

        # create push button to trigger API call
        self.search = QtWidgets.QPushButton(self)
        self.search.setCursor(PyQt5.QtGui.QCursor(PyQt5.QtCore.Qt.PointingHandCursor))
        self.search.setText("Search")
        self.search.move(500,130)
        self.search.setDefault(True)
        self.search.setStyleSheet("background-color: white; border-radius: 10px")
        self.search.clicked.connect(self.print_results)
    
        # create shortcut for triggering API call
        self.shortcut = QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence("return"), self) 
        self.shortcut.activated.connect(self.print_results)
        
    # function to retrieve and print data from YouTube's API according to 
    # query entered by the user in the search bar
    def print_results(self):
        # use get_videos to retrieve data from API
        self.videos = get_videos(self.search_bar.text())
        self.search_bar.clear()
        self.results = QtWidgets.QGroupBox(self)
        self.results.setTitle("Top Results")
        self.results.move(10,170)
        self.results.resize(780,450)
        self.results.show()

        # loop over the videos and print their name and channels
        y_name = 190
        y_channel = 210
        for i in range(5):
            self.name = QtWidgets.QLabel(self)
            self.name.setText(self.videos[i]["snippet"]["title"])
            self.name.move(15,y_name)
            self.name.show()
            self.name.adjustSize()
            self.name.setStyleSheet("background:transparent")

            self.channel = QtWidgets.QLabel(self)
            self.channel.setText(self.videos[i]["snippet"]["channelTitle"])
            self.channel.move(15,y_channel)
            self.channel.show()
            self.channel.adjustSize()
            self.channel.setStyleSheet("background:transparent")

            y_name += 80
            y_channel += 80

        # create 5 PushButtons that will trigger the download of the respective video
        self.down_one = QtWidgets.QPushButton(self)
        self.down_one.setCursor(PyQt5.QtGui.QCursor(PyQt5.QtCore.Qt.PointingHandCursor))
        self.down_one.setText("Download")
        self.down_one.show()
        self.down_one.setStyleSheet("background-color: green; border-radius: 10px")
        self.down_one.move(15,235)
        self.down_one.resize(100,25)

        self.down_two = QtWidgets.QPushButton(self)
        self.down_two.setCursor(PyQt5.QtGui.QCursor(PyQt5.QtCore.Qt.PointingHandCursor))
        self.down_two.setText("Download")
        self.down_two.show()
        self.down_two.setStyleSheet("background-color: green; border-radius: 10px")
        self.down_two.move(15,315)
        self.down_two.resize(100,25)

        self.down_three = QtWidgets.QPushButton(self)
        self.down_three.setCursor(PyQt5.QtGui.QCursor(PyQt5.QtCore.Qt.PointingHandCursor))
        self.down_three.setText("Download")
        self.down_three.show()
        self.down_three.setStyleSheet("background-color: green; border-radius: 10px")
        self.down_three.move(15,395)
        self.down_three.resize(100,25)

        self.down_four = QtWidgets.QPushButton(self)
        self.down_four.setCursor(PyQt5.QtGui.QCursor(PyQt5.QtCore.Qt.PointingHandCursor))
        self.down_four.setText("Download")
        self.down_four.show()
        self.down_four.setStyleSheet("background-color: green; border-radius: 10px")
        self.down_four.move(15,475)
        self.down_four.resize(100,25)

        self.down_five = QtWidgets.QPushButton(self)
        self.down_five.setCursor(PyQt5.QtGui.QCursor(PyQt5.QtCore.Qt.PointingHandCursor))
        self.down_five.setText("Download")
        self.down_five.show()
        self.down_five.setStyleSheet("background-color: green; border-radius: 10px")
        self.down_five.move(15,555)
        self.down_five.resize(100,25)

        # connect the download buttons to the download function
        self.down_one.clicked.connect(lambda:download(0, self.videos[0]['id']['videoId'], self))
        self.down_two.clicked.connect(lambda:download(1, self.videos[1]['id']['videoId'], self))
        self.down_three.clicked.connect(lambda:download(2, self.videos[2]['id']['videoId'], self))
        self.down_four.clicked.connect(lambda:download(3, self.videos[3]['id']['videoId'], self))
        self.down_five.clicked.connect(lambda:download(4, self.videos[4]['id']['videoId'], self))
        
# create pop-up message window to indicate the beginning of the download
def initiating(win, i):
    win.msg = QtWidgets.QMessageBox(win)
    win.msg.setWindowTitle("Download Initiated")
    win.msg.setText(f"Press Enter, Click Ok, or close this window to continue downloading\n{win.videos[i]['snippet']['title']} by {win.videos[i]['snippet']['channelTitle']}...")
    win.msg.setIcon(QtWidgets.QMessageBox.Information)
    win.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
    x = win.msg.exec_()

# create pop-up window to remind user to choose a valid format for downloading
def invalid_format(win):
    win.msg = QtWidgets.QMessageBox(win)
    win.msg.setWindowTitle("Format Error")
    win.msg.setText("Please select a valid format")
    win.msg.setIcon(QtWidgets.QMessageBox.Critical)
    win.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
    x = win.msg.exec_()

# create pop-up window to update user regarding download status
def completed(win):
    win.msg = QtWidgets.QMessageBox(win)
    win.msg.setWindowTitle("Completed!")
    win.msg.setText("Download completed successfully!")
    win.msg.setIcon(QtWidgets.QMessageBox.Information)
    win.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
    x = win.msg.exec_()

# create pop-up window to inform user that the desired file already exists
def already_exists(win):
    win.msg = QtWidgets.QMessageBox(win)
    win.msg.setWindowTitle("Error!")
    win.msg.setText("File already exists!")
    win.msg.setIcon(QtWidgets.QMessageBox.Critical)
    win.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
    x = win.msg.exec_()

# pop-up window created when any pytube exception raised
def unknown(win):
    win.msg = QtWidgets.QMessageBox(win)
    win.msg.setWindowTitle("Error!")
    win.msg.setText("Unknown error occured!\nTry downloading again.\n If it does not work then try another video.")
    win.msg.setIcon(QtWidgets.QMessageBox.Critical)
    win.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
    x = win.msg.exec_()

# pop-up window created when user tries to download a live stream
def live_error(win):
    win.msg = QtWidgets.QMessageBox(win)
    win.msg.setWindowTitle("Error!")
    win.msg.setText("Live-streams cannot be downloaded")
    win.msg.setIcon(QtWidgets.QMessageBox.Critical)
    win.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
    x = win.msg.exec_()

# use YouTube's API to get data related to the user's query
def get_videos(query):
    params = {'q':query,
            'type':'video',
            'part':'snippet',
            'key':'AIzaSyBBZkXjWQhX-WuqmYhAKdIStUfIRAL-EGM'}

    url = 'https://www.googleapis.com/youtube/v3/search'
    r = requests.get(url, params = params)
    data = r.json()
    videos = data["items"]
    return videos

# download the video in the required format using pytube
def download(i, videoID, win):
    initiating(win, i)
    url = f"https://www.youtube.com/watch?v={videoID}" # create url using videoID
    vid = YouTube(url)

    # error handling if user tries to download a live-stream
    if win.videos[i]['snippet']['liveBroadcastContent'] == 'live':
        live_error(win)
        return

    # if-condition to download mp3 or mp4 according to user's choice
    # including general exception handling
    if win.mp4.isChecked():
        audio = vid.streams.filter(file_extension='mp4')
        try:
            audio[0].download(output_path = f'{os.getcwd()}\mp4')
            completed(win)
        except FileExistsError:
            already_exists(win)
    elif win.mp3.isChecked():
        audio = vid.streams.filter(only_audio = True)
        try:
            out_file = audio[0].download(output_path = f'{os.getcwd()}\mp3')
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            completed(win)
        except FileExistsError:
            already_exists(win)
            os.remove(out_file)
        except PytubeError:
            unknown(win)
    else:
        invalid_format(win)
        


# function to display the window
def window():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

window()
