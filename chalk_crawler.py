# Chalk_Crawler w/ Selenium

# import pickle for cookies
from selenium import webdriver
import time
import getpass

class Chalk_Page:
    def __init__(self, quarter, year): # username, password
        self.url = 'https://chalk.uchicago.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1'
        self.browser = self.login()
        self.quarter = quarter
        self.year = year
        self.courses = self.compile_courses()
        # self.cookies = []


    def login(self):
        username = input('enter username: ')
        password = getpass.getpass('enter password: ')

        browser = webdriver.Firefox()
        browser.delete_all_cookies()
        browser.implicitly_wait(7)

        browser.get(self.url)
        browser.find_element_by_name('user_id').send_keys(username)
        browser.find_element_by_name('password').send_keys(password)

        login_form = browser.find_element_by_id('entry-login')
        login_form.submit()

        time.sleep(3)
        # self.cookies.append(browser.get_cookies)

        # Save cookies to file.
        # with open('cookies.txt', mode ='w') as f:
        #     for cookie in self.cookies:
        #         line = '%s\tTRUE\t%s\t%s\t%s\t%s\t%s' % ( \
        #             cookie['domain'], cookie['path'], 'TRUE' if cookie['secure'] else 'FALSE', \
        #             cookie['expiry'] if cookie['expiry'] else 0, cookie['name'], cookie['value'])
        #         f.write(line.encode('utf-8') + '\n')
 
        # print 'DONE - Collected {:} cookies'.format(len(self.cookies))
        # driver.close()
        
        return browser


    def compile_courses(self): 
        courses = []

        if len(str(self.year)) == 4:
            self.year = str(self.year)[2:]

        self.browser.find_element_by_xpath('//*[@title="Manage Chalk Course List Module Settings"]').click()
        for course_web_element in self.browser.find_elements_by_tag_name('strong'):
            for quarter in self.quarter:
                if quarter.lower() == 'fall':
                    quarter = 'autumn'
                if '({:} '.format(quarter.lower()) + '{:})'.format(self.year) in course_web_element.text.lower(): 
                    if 'Unavailable' not in course_web_element.text:
                        courses.append(course_web_element.text)
                        course_name_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Course Name"]')
                        course_name_box.click()
                        course_id_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Course ID"]')
                        course_id_box.click()

        course_form = self.browser.find_element_by_id('moduleEditForm')
        course_form.submit()

        return courses


        def access_courses(self):
