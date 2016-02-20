#CHALK CRAWLER

import requests
from robobrowser import RoboBrowser
import getpass


class Chalk_Page:
    def __init__(self):
        self.browser = self.login()


    def login(self):
        url = 'https://chalk.uchicago.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1/'

        username = input('enter username: ')
        password = getpass.getpass('enter password: ')

        browser = RoboBrowser(history = True)
        browser.open(url)

        login_form = browser.get_form(action='/webapps/login/')
        login_form['user_id'] = username
        login_form['password'] = password

        browser.session.headers['Referer'] = url
        browser.submit_form(login_form)
        print(browser.parsed)
        return browser


    # def compile_courses(self):
    #    for link in self.browser.find_all(
            






