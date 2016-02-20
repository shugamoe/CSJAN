#CHALK CRAWLER
# RoboBrowser: http://robobrowser.readthedocs.org/en/latest/api.html
# bs4: http://www.crummy.com/software/BeautifulSoup/bs4/doc/

import requests
from robobrowser import RoboBrowser
import getpass


class Chalk_Page:
    def __init__(self, quarter, year):
        self.url = 'https://chalk.uchicago.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1'
        self.browser = self.login()
        self.quarter = quarter
        self.year = year
        self.courses = self.compile_courses()


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
        courses = []

        if self.quarter.lower() == 'fall':
            self.quarter = 'autumn'

        if len(str(self.year)) == 4:
            self.year = str(self.year)[2:]

        link_tag = self.browser.find(title="Manage Chalk Course List Module Settings")
        self.browser.follow_link(link_tag)
        for course_tag in self.browser.find_all('option'):
            if '({:} '.format(self.quarter.lower()) + '{:})'.format(self.year) in course_tag.string.lower(): 
                courses.append(course_tag)

        course_form = self.browser.get_form(action='bbcourseorg')
        for course in courses:
            course_form['amc.showcourse.{:}'.format(course['value'])] = ['true']
            course_form['amc.showcourseid.{:}'.format(course['value'])] = ['true']
        self.browser.back(1) # is the form still updated?
        # self.browser.submit_form(course_form, submit = course_form['top_Submit'])
        print(self.browser.find('title'))


    # def access_courses(self):
    #     print(self.browser.find(id='module:_25_1'))
