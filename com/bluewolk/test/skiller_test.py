'''
Created on Nov 30, 2018

@author: adogarci
'''
'''
@author: EscalanteA
'''

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from com.bluewolk.engine.skiller import SkillerBrowser, Skiller
import datetime
import logging
import subprocess
import smtplib

import configparser
import re


def setup_logging():
    logging.basicConfig(filename='genesys.log', format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

def get_property(prop):
    config = configparser.RawConfigParser()
    config.read('cache_check_site.skiller')
    return config.get('CivSection', prop)

if __name__ == '__main__':
    setup_logging()

    app = QApplication(sys.argv)

    '''
        # QT Application Settings
        QWebEngineSettings.defaultSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        QWebEngineSettings.defaultSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        QWebEngineSettings.defaultSettings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        QWebEngineSettings.defaultSettings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        QWebEngineSettings.defaultSettings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True )
        QWebEngineSettings.defaultSettings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True )
    '''
    # Navigation URLS
    url_home = 'https://www.bluewolk.com/'


    window = SkillerBrowser()
    Skiller.instance().addWindow(window)

    window.webPage.loadPage(url_home)
    #instance_status = window.webPage.searchTextHtml('title', 'Bluewolk')

    login_status = False
    message_status = False
    todo_status = False

    #if instance_status:
        # Login
    #        window.webPage.fill_input_name('input', 'text', 'userName', param_user)
    #        window.webPage.fill_input_name('input', 'Password', 'password', param_password)
    #        window.webPage.click('div#mainCol>div:nth-child(3)>table>tbody>tr:nth-child(3)>td:nth-child(2)>input')
    #        login_status = window.webPage.searchTextHtml('h1', 'My Applications')

    #   logging.info('Applications tab running: Success')

    # Exit Application
    #window.webPage.app.closeAllWindows()
    #window.webPage.app.quit()
    #window.skillerWebView.close()
    #window.close()
    #app.quit()
    app.exec_()
    #sys.exit(Skiller.instance().app.exec_())