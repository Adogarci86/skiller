'''
Created on Nov 30, 2018

@author: adogarci
'''
import sys
import logging
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QVBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt, QUrl, QEvent, QEventLoop, QMarginsF
from PyQt5.QtGui import QPageLayout, QPageSize
from typing import List
from bs4 import BeautifulSoup

__version__ = "0.0.1"
PY3 = sys.version > '3'

if PY3:
    unicode = str
    long = int
    basestring = str


default_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 " +\
    "(KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2"
    
def setup_logging():
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)

class WebPopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.m_view = QWebEngineView(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.m_view)
        self.skweb = SkillerWebPage2(self.m_view)
        self.m_view.setPage(self.skweb)
        self.m_view.setFocus()
        self.m_view.page().windowCloseRequested.connect(self.close)
        
    def view(self) -> QWebEngineView:
        return self.m_view
    
class SkillerWebView(QWebEngineView):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        setup_logging()
        
    def mousePressEvent(self, evnt):
        if evnt.type() == QEvent.MouseButtonPress:
            self
            logging.info('Mouse pressed WebView')
    
    def createWindow(self, qtType: QWebEnginePage.WebWindowType) -> QWebEngineView:
        if qtType == QWebEnginePage.WebBrowserTab:
            logging.debug('skiller tab1...')
            mainWindow = self.window()
            return mainWindow.tabWidget().createTab(False)
        if qtType == QWebEnginePage.WebBrowserBackgroundTab:
            logging.debug('skiller tab2...')
            mainWindow = self.window()
            return mainWindow.tabWidget().createTab(False)
        if qtType == QWebEnginePage.WebBrowserWindow:
            logging.debug('skiller tab3...')
            mainWindow = SkillerBrowser()
            Skiller.instance().addWindow(mainWindow)
            return mainWindow.currentTab()
        if qtType == QWebEnginePage.WebDialog:
            logging.debug('skiller tab4...')
            popup = WebPopupWindow()
            Skiller.instance().addWindow(popup)
            Skiller.instance().set_popup(popup)
            return popup.view()
        print('createWindow: unhandled type', qtType)
        return None

class SkillerBrowser(QMainWindow):
    def __init__(self, parent: QWidget=None, flags: Qt.WindowFlags=Qt.Widget):
        super().__init__(parent, flags)
        self.skillerWebView = SkillerWebView()
        self.showMaximized()
        self.webPage = SkillerWebPage(self.skillerWebView)
        self.skillerWebView.setPage(self.webPage)
        centralWidget = QWidget(self)
        layout = skillerContainer()
        layout.addWidget(self.skillerWebView)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
       
    def executeJavascript(self, query: str):
        setup_logging()
        logging.debug(self.webPage.isAudioMuted())
        self.webPage.runJavaScript(query)
        
    def mousePressEvent(self, evnt):
        if evnt.type() == QEvent.MouseButtonPress:
            self.skillerWebView
            self.skillerWebView.reload()
            logging.info('Mouse pressed Browser')
            
class SkillerWebPage2(QWebEnginePage):
    def __init__(self, skillerWebView:QWebEngineView):
        QWebEnginePage.__init__(self, QWebEngineProfile.defaultProfile(), skillerWebView)
        logging.debug('New WebPage popup')
        self.loadFinished.connect(self._on_load_finished)
        self.profile().downloadRequested.connect(self.download_requested)
        self.html = ''
        
    def _on_load_finished(self):
        self.load_complete = False
        self.html = self.toHtml(self.Callable)
        logging.debug('Load finished popup')
        
    def Callable(self, html_str):
        logging.debug('callable popup...')
        self.html = html_str
        Skiller.instance().set_popup_status(True)
        
    def download_requested(self, item):
        logging.debug("Unsupported content %s", str(item.url()))
        if 'checkDocumentType' in str(item.url()):
            item.setPath('D:/BlankTemplate.pdf')
        if 'generateReport' in str(item.url()):
            item.setPath('D:/ReleaseNoteReport.xlsx')
        logging.debug('downloading to %s', item.path())
        item.accept()
        Skiller.instance().set_pdf_status(True)
        Skiller.instance().get_popup().close()
        

class SkillerWebPage(QWebEnginePage):
    def __init__(self, skillerWebView:QWebEngineView):
        QWebEnginePage.__init__(self, QWebEngineProfile.defaultProfile(), skillerWebView)
        self.html = ''
        self.html2 = ''
        self.load_complete = False
        self.form_filled = False
        self.popup_loaded = False
        
    def loadPage(self, page: str):
        self.loadPageUrl(QUrl.fromUserInput(page))

    def loadPageUrl(self, url: QUrl):
        self.loadFinished.connect(self._on_load_finished)
        self.load(url)
        self.wait_until_load()
        
    def wait_until_load(self):
        self.app = QApplication(sys.argv)
        while self.load_complete is False:
            self.app.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
        self.app.quit()
            
    def submit(self):
        while self.load_complete is False:
            self.app.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
        self.app.quit()
        logging.debug('Submiting...' + str(self.load_complete))
        self.load_complete = False
        self.runJavaScript('submitForm();', 0)
    
    def mousePressEvent(self, evnt):
        if evnt.type() == QEvent.MouseButtonPress:
            logging.info('Mouse pressed WebPage')

    def _on_load_finished(self):
        self.load_complete = False
        self.html = self.toHtml(self.Callable)
        logging.debug('Load finished')
        
    def Callable(self, html_str):
        logging.debug('callable...')
        self.html = html_str
        self.load_complete = True

class skillerContainer(QVBoxLayout):
    def mousePressEvent(self, evnt):
        if evnt.type() == QEvent.MouseButtonPress:
            logging.info('Mouse pressed Container')
                
class Skiller:
    def __init__(self):
        self.m_windows = []
        self.popup_ready = False
        self.pdf_ready = False
        self.popup = None
        self.html = ''

    @staticmethod
    def instance() -> 'Skiller':
        global skiller_instance
        return skiller_instance
            
    def set_popup(self, webpopw: WebPopupWindow):
        logging.debug('Setting popup...')
        self.popup = webpopw
        
    def get_popup(self) -> WebPopupWindow:
        return self.popup
    
    def windows(self) -> List[SkillerBrowser]:
        return self.m_windows
    
    def set_popup_status(self, status):
        logging.debug('Updating popup status')
        self.popup_ready = status
        
    def get_popup_status(self):
        return self.popup_ready
    
    def set_pdf_status(self, status):
        logging.debug('Updating pdf status')
        self.pdf_ready = status
        
    def get_pdf_status(self):
        return self.pdf_ready

    def addWindow(self, mainWindow: SkillerBrowser):
        setup_logging()
        logging.debug('skiller adding window...')
        if mainWindow in self.m_windows:
            return
        self.m_windows.insert(0, mainWindow)
        mainWindow.destroyed.connect(lambda: self.m_windows.remove(mainWindow))
        mainWindow.show()
        
skiller_instance = Skiller()

