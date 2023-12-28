from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtMultimedia import *

class ChaitanyaBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ChaitanyaBrowser, self).__init__(*args, **kwargs)
        self.setWindowTitle("Chaitanya godly browser")
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage("Chaitanya \u00A9 2023")

        self.media_player = QMediaPlayer(self) 
        self.showMaximized()

        self.create_tab()

    def create_tab(self, url="http://google.com"):
        self.tab = QWidget()
        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()
        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(32)
        self.go_button = QPushButton("Go to: ")
        self.go_button.setMinimumHeight(32)
        self.back_button = QPushButton("Back")
        self.back_button.setMinimumHeight(32)
        self.forward_button = QPushButton("Forward")
        self.forward_button.setMinimumHeight(32)
        self.create_new_tab_button = QPushButton("New Tab")
        self.create_new_tab_button.setMinimumHeight(32)
        self.create_new_tab_button.clicked.connect(self.create_tab)

        self.close_tab_button = QPushButton("x")
        self.close_tab_button.setFixedSize(20, 20)
        self.close_tab_button.clicked.connect(self.close_tab)

        self.history_button = QPushButton("History")
        self.history_button.setMinimumHeight(32)
        self.history_button.clicked.connect(self.show_history)

        self.history = []
        self.current_index = -1

        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_button)
        self.horizontal.addWidget(self.back_button)
        self.horizontal.addWidget(self.forward_button)
        self.horizontal.addWidget(self.create_new_tab_button)
        self.horizontal.addWidget(self.history_button)
        self.horizontal.addWidget(self.close_tab_button)

        self.browser = QWebEngineView()

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)
        self.tab.setLayout(self.layout)
        self.central_widget.addTab(self.tab, "New Tab")
        try:
            self.browser.setUrl(QUrl(url))
        except Exception as e:
            print(f"Error setting URL: {e}")

        self.go_button.clicked.connect(self.navigate)
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.browser.titleChanged.connect(self.update_tab_title)  
        self.browser.page().profile().downloadRequested.connect(self.download_requested)  
    def navigate(self):
        url = self.url_bar.toPlainText()
        if not url.startswith("http"):
            url = "http://" + url
            self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))
        self.update_history(url)

    def update_history(self, url):
        if self.current_index < len(self.history) - 1:
            del self.history[self.current_index + 1:]
        self.history.append(url)
        self.current_index = len(self.history) - 1
        self.update_buttons()

    def update_buttons(self):
        self.back_button.setEnabled(self.current_index > 0)
        self.forward_button.setEnabled(self.current_index < len(self.history) - 1)

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            url = self.history[self.current_index]
            self.browser.setUrl(QUrl(url))
            self.update_buttons()

    def go_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            url = self.history[self.current_index]
            self.browser.setUrl(QUrl(url))
            self.update_buttons()

    def update_tab_title(self, title):
        current_index = self.central_widget.currentIndex()
        self.central_widget.setTabText(current_index, title)

    def download_requested(self, download):
        # Handle download requests
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        if dialog.exec_() == QDialog.Accepted:
            download.setPath(dialog.selectedFiles()[0])
            download.accept()
        else:
            download.cancel()

    def show_history(self):
        history_text = "\n".join(self.history)
        QMessageBox.about(self, "History", f"Visited Websites:\n{history_text}")

    def close_tab(self):
        current_index = self.central_widget.currentIndex()
        self.central_widget.removeTab(current_index)
        if self.central_widget.count() == 0:
            QApplication.instance().quit()

app = QApplication([])
window = ChaitanyaBrowser()
app.exec_()
