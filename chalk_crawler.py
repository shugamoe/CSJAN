# Chalk_Crawler w/ Selenium

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

        # time.sleep(3)
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
        course_material_dict[self.courses[0]] = self.build_course_dict(self.courses[0])

        return course_material_dict


    def build_course_dict(self, first_key):
        self.browser.find_element_by_link_text(first_key).click()
        
        material_dict = {}

        for item_number in range(len(self.browser.find_element_by_id('courseMenuPalette_contents').find_elements_by_tag_name('li'))):
            item = self.browser.find_element_by_id('courseMenuPalette_contents').find_elements_by_tag_name('li')[item_number]
            # if item.text == 'Announcements':
            #     material_dict[item.text] = None
            #     item.find_element_by_tag_name('a').click()              
            #     content_list_container = self.browser.find_element_by_id('content_listContainer')
            #     for file_or_folder in content_list_container.find_elements_by_tag_name('li'):
                    # print(file_or_folder.text + '\n')  announcements page to download               

            # My Grades?

            # elif item.text == 'Send Email':
            #     item.find_element_by_tag_name('a').click()
            #     self.browser.find_element_by_link_text('All Instructor Users').click()

            #     professor = self.browser.find_element_by_id('stepcontent1').find_elements_by_tag_name('li')[0].text[2:]
            #     # print(professor)

            #     self.browser.execute_script("window.history.go(-1)")
            #     self.browser.find_element_by_link_text('All Teaching Assistant Users').click()

            #     list_of_tas = self.browser.find_element_by_id('stepcontent1').find_elements_by_tag_name('li')[0].text[3:].split('; ')
            #     # print(list_of_tas)

            #     self.browser.execute_script("window.history.go(-1)")
            #     self.browser.find_element_by_link_text('Select Users').click()

            #     list_of_students_web_elements = self.browser.find_element_by_id('stepcontent1').find_element_by_name('USERS_AVAIL').find_elements_by_tag_name('option')
            #     list_of_students = []
            #     for student_web_element in list_of_students_web_elements:
            #         if student_web_element.text not in professor and student_web_element.text not in list_of_tas and 'PreviewUser' not in student_web_element.text:
            #             list_of_students.append(student_web_element.text)
            #     # print(list_of_students)

            if item.text != 'Announcements' and item.text != 'Send Email':
                item.find_element_by_tag_name('a').click()
                if self.check_content_exists_by_link(): #always returning False
                    if self.check_icon_exists_by_link(item): #always returning False
                        print(item.text)
                    else:
                        continue
                else:
                    continue
                #folder_on: gen inner dict
                #document_on: download text, include links
                #file_on
            # no img: download text
                self.browser.execute_script("window.history.go(-1)")

        return material_dict

    def check_content_exists_by_link(self):
        try:
            self.browser.find_elements_by_id('content_listContainer')
        except:
            return False
        return True


    def check_icon_exists_by_link(self, container):
        try:
            container.find_element_by_tag_name('img')
        except:
            return False
        return True 





