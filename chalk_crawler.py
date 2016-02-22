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
        self.course_material_dict = self.access_courses()
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
        for course_web_element in \
            self.browser.find_elements_by_tag_name('strong'):

            for quarter in self.quarter:
                if quarter.lower() == 'fall':
                    quarter = 'autumn'

                if '({:} '.format(quarter.lower()) + '{:})'.format(self.year) \
                    in course_web_element.text.lower(): 

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

        # for course in self.courses:
        course_material_dict = {}
        course_material_dict[self.courses[0]] = {}
        self.browser.find_element_by_link_text(self.courses[0]).click()
        palette = self.browser.find_element_by_id('courseMenuPalette_contents')
        # for item in palette.find_elements_by_tag_name('li'):
        link = palette.find_elements_by_tag_name('li')[0].find_element_by_tag_name('a')
        course_material_dict[self.courses[0]][link.text] = self.build_course_dict(link)

        return course_material_dict

# (img ... folder_on.gif vs. document_on.gif[exclude ext. links]) vs. \
# no img (grades/discussion/lib.coursereserves/sendemail/tools vs everything else)

    def build_course_dict(self, link):
        material_dict = {}
        link.click()
        content_list_container = link.find_element_by_id('content_listContainer')
        for file_or_folder in link.find_elements_by_tag_name('li'):
            if self.check_img_exists_by_link(file_or_folder):
                #folder_on: gen inner dict
                #document_on: download text, include links
            # no img: download text


        return material_dict


    def check_img_exists_by_link(self, link):

        try:
            link.find_element_by_tag_name('img')
        except NoSuchElementException:
            return False
        return True 





