#CHALK CRAWLER
# RoboBrowser: http://robobrowser.readthedocs.org/en/latest/api.html
# bs4: http://www.crummy.com/software/BeautifulSoup/bs4/doc/

import requests
from robobrowser import RoboBrowser
import getpass


class Chalk_Page:
    def __init__(self):
        self.url = 'https://chalk.uchicago.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1'
        self.browser = self.login()


    def login(self):
        username = input('enter username: ')
        password = getpass.getpass('enter password: ')

        browser = RoboBrowser(history = True)
        browser.open(self.url)

        login_form = browser.get_form(action='/webapps/login/')
        login_form['user_id'] = username
        login_form['password'] = password

        browser.session.headers['Referer'] = self.url
        browser.submit_form(login_form)
        
        return browser


    def compile_courses(self):
       # print(self.browser.find(id='module:_25_1'))
       # for link_tag in self.browser.find_all('a'):
       #  if link_tag.has_attr('title'):
       #      if link_tag['title'] == "Manage Chalk Course List Module Settings":
       #          print(link_tag)
       #          print(self.browser.follow_link(link_tag))

        print(self.browser.find('a'))
        print(self.browser.follow_link((self.browser.find('a')))

        return None











