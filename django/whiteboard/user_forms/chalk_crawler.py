# Chalk_Crawler w/ Selenium
# https://chalk.uchicago.edu/bbcswebdav/pid-3030087-dt-content-rid-6454815_1/courses/2016.01.80030000M2/Transaction%20Analysis%20and%20Financial%20Statement%20Design%20BLANK%20-%20Jan%205%202014%281%29.pdf

from selenium import webdriver
import time
import getpass
import folders as local_dir
import os
import urllib
import requests

class Chalk_Page:
    
    def __init__(self, quarter, year): # dict

        self.url = 'https://chalk.uchicago.edu'
        self.username = ''
        self.password = ''
        self.quarter = quarter # dict['quarter']
        self.year = year # dict['year']
        self.default_folder = '../../Classes'
        self.browser = self.login() 

        self.all_courses_list = [] # all course ids
        self.course_list = [] # list of lists: course_id, prof, tas, students
        self.all_courses, self.courses = self.compile_courses()
        self.course_material_dict = {}
        self.access_courses()

        local_dir.make_dirs(self.course_material_dict, self.default_folder)  


    def login(self):

        self.username = input('enter username: ') # self.username
        self.password = getpass.getpass('enter password: ') # self.password
        
        browser = webdriver.Firefox()
        browser.implicitly_wait(2)

        browser.get(self.url)
        browser.find_element_by_name('user_id').send_keys(self.username)
        browser.find_element_by_name('password').send_keys(self.password)

        login_form = browser.find_element_by_id('entry-login')
        login_form.submit() 


        return browser


    def compile_courses(self): 

        all_courses = []
        courses = []

        if len(str(self.year)) == 4:
            self.year = str(self.year)[2:]

        #Handle invalid logins        
    
        self.browser.find_element_by_xpath('//*[@title="Manage Chalk Course List Module Settings"]').click()
        for course_web_element in \
            self.browser.find_elements_by_tag_name('strong'):

            all_courses.append(course_web_element.text)

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
                        course_instructor_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Instructors"]')
                        course_instructor_box.click()

        course_form = self.browser.find_element_by_id('moduleEditForm')
        course_form.submit()

        return all_courses, courses


    def access_courses(self):

        self.course_material_dict[self.username] = {}

        for ind, course in enumerate(self.courses): 
            self.course_material_dict[self.username][local_dir.check_folder_name(course[20:])] = {}
            material_dict = self.course_material_dict[self.username][local_dir.check_folder_name(course[20:])]
            self.build_course_dict(course, ind, material_dict) 

        return None


    def build_course_dict(self, first_key, prof_ind, material_dict):
        course = [first_key]
        
        professor = self.browser.find_elements_by_class_name('courseInformation')[prof_ind].text
        prof_cnt = professor.count(';')
        course.append(professor.replace('Instructor: ', '').split('; ')[:prof_cnt])

        self.browser.find_element_by_link_text(first_key).click()

        
        for item_index in range(len(self.browser.find_element_by_id('courseMenuPalette_contents').find_elements_by_tag_name('li'))):
            item = self.browser.find_element_by_id('courseMenuPalette_contents').find_elements_by_tag_name('li')[item_index]

            if item.text == 'Announcements':
                material_dict[item.text] = {}
                local_dir.make_dirs(self.course_material_dict, self.default_folder)  

                item.find_element_by_tag_name('a').click()              
                if self.check_id_exists('content_listContainer'): 

                    content_list_container = self.browser.find_element_by_id('content_listContainer')
                    announcement_text = ''

                    for file_or_folder in content_list_container.find_elements_by_tag_name('li'):
                        announcement_text += file_or_folder.text + '\n' 

                else:
                    content = self.browser.find_element_by_id('content')
                    announcement_text = content.find_element_by_id('announcementList').text
                self.download_text('Announcements', announcement_text, '{:}/{:}/{:}/Announcements/'.format(self.default_folder, self.username, str(local_dir.check_folder_name(first_key[20:]))))

            elif item.text == 'Send Email':
                item.find_element_by_tag_name('a').click()
                
                self.browser.find_element_by_link_text('All Teaching Assistant Users').click()
                list_of_tas = []
                if not self.check_id_exists('inlineReceipt_bad'):
                    list_of_tas = self.browser.find_element_by_id('stepcontent1').find_elements_by_tag_name('li')[0].text[3:].split('; ')
                    course.append(list_of_tas)
                self.browser.execute_script("window.history.go(-1)")
                
                if self.check_link_text_exists('Select Users'):
                    self.browser.find_element_by_link_text('Select Users').click()
                    list_of_students_web_elements = self.browser.find_element_by_id('stepcontent1').find_element_by_name('USERS_AVAIL').find_elements_by_tag_name('option')
                    list_of_students = []
                    for student_web_element in list_of_students_web_elements:
                        if student_web_element.text not in professor and student_web_element.text not in list_of_tas and 'PreviewUser' not in student_web_element.text:
                            list_of_students.append(student_web_element.text)
                    course.append(list_of_students)
                    self.browser.execute_script("window.history.go(-1)")


            elif item.text not in ['Home', 'Announcements', 'Send Email', \
                'My Grades', 'Discussion Board', 'Discussions', \
                'Library Course Reserves', 'Tools', 'Groups']:

                component = local_dir.check_folder_name(item.text)
                material_dict[component] = {}
                local_dir.make_dirs(self.course_material_dict, self.default_folder)
                item.find_element_by_tag_name('a').click()
                # store item_url

                if self.check_xpath_exists('//*div[@class = "noItems container-empty"]'):
                    continue

                elif self.check_id_exists('content_listContainer'):
                    num_of_items = len(self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li'))
                    for unit_index in range(num_of_items):
                        unit = self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li')[unit_index]
                        if self.check_tag_exists_in_web_element(unit, 'img'):
                            img = unit.find_element_by_tag_name('img')
                            if img.get_attribute('class') == 'item_icon':
                                if 'folder_on' in img.get_attribute('src'):
                                    folder_name = local_dir.check_folder_name(unit.find_element_by_tag_name('a').text)
                                    material_dict[component][folder_name] = self.gen_folder(unit)
                                
                                elif 'file_on' in img.get_attribute('src'):
                                    unit_name = unit.find_element_by_tag_name('a').text
                                    file_url = unit.find_element_by_tag_name('a').get_attribute('href')
                                    
                                    s = requests.session()
                                    s.get(file_url, auth = (self.username, self.password))
                                    r = s.get(file_url, stream = True, auth = (self.username, self.password))
                                    with open(self.default_folder + '/{:}/{:}/{:}/{:}'.format(self.username, course[0][20:], component, unit_name), 'wb') as f:
                                        r.raw.decode_content = True
                                        f.write(r.content)

                                    


                        # elif 'document_on' in img.get_attribute('src')):
                        # download text for all

        self.course_list.append(course)
        self.browser.find_element_by_id('My Chalk').find_element_by_tag_name('a').click()

  
        return material_dict


    def check_id_exists(self, id_): 
        try:
            self.browser.find_element_by_id(id_)
        except:
            return False
        return True


    def check_link_text_exists(self, link_text): 
        try:
            self.browser.find_element_by_link_text(link_text)
        except:
            return False
        return True


    def check_tag_exists_in_web_element(self, web_element, tag):
        try:
            web_element.find_element_by_tag_name(tag)
        except:
            return False
        return True 


    def check_xpath_exists(self, xpath):
        try:
            web_element.find_element_by_xpath(xpath)
        except:
            return False
        return True 


    def gen_folder(self, unit): 
        folder_dict = {}
        unit.find_element_by_tag_name('a').click() # clicking 'Additional Practice problems'
        if self.check_id_exists('content_listContainer'):
            num_of_items = len(self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li'))
            for unit_index in range(num_of_items):
                inner_unit = self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li')[unit_index]
                if self.check_tag_exists_in_web_element(inner_unit, 'img'):
                    img = self.browser.find_element_by_tag_name('img')
                    if img.get_attribute('class') == 'item_icon':
                        if 'folder_on' in img.get_attribute('src'):
                            folder_dict[local_dir.check_folder_name(inner_unit.text)] = self.gen_folder(inner_unit)
        self.browser.execute_script("window.history.go(-1)")


                        # elif 'file_on' in img.get_attribute('src')):

                        # elif 'document_on' in img.get_attribute('src')):
                        # download text for all


        return folder_dict


    def download_text(self, filename, text, path):

        if os.path.exists(path + filename + '.txt'):
            print('File already exists. Updating file.')
            os.remove(path + filename + '.txt')

        with open(path + filename + '.txt', 'w') as f:
            f.write(text)









