# Chalk_Crawler w/ Selenium

from selenium import webdriver
import time
import getpass
try:
    from .folders import check_folder_name, make_dirs, convert_pdf
except:
    from folders import check_folder_name, make_dirs, convert_pdf
import os
import urllib
import requests


def create_object(input_dict):
    
    a = Courses(input_dict['quarter'], input_dict['year'], input_dict['cnet_id'], input_dict['cnet_pw'])
    
    return a


def get_courses(input_dict):
    
    a = create_object(input_dict)

    return a.courses


def dl_specific_courses(list_of_courses, cnet_id, passwd):

    a = Courses([], [], cnet_id, passwd, dl = True)
    a.access_courses(list_of_courses)
    a.browser.close()
    return a.course_info, a.file_list



class Courses:
    
    def __init__(self, quarter, year, cnet_id, cnet_pw, dl = False): # dict

        self.url = 'https://chalk.uchicago.edu'
        self.quarter = quarter # dict['quarter']
        self.year = year # dict['year']
        self.username = cnet_id
        self.password = cnet_pw
        self.default_folder = '../../Classes'
        
        self.browser = self.login() 

        if not dl:
            self.all_courses, self.courses = self.compile_courses()



        self.course_info = [] # list of lists: course_id, prof, tas, students
        self.course_material_dict = {}

        # 'list of dicts, {'owner', 'course', 'heading', 'description', 'body', 
        # 'path', 'format'}; format is in the form of 'application/...'
        self.file_list = [] 
   

    def login(self):
        
        browser = webdriver.Firefox()
        # browser = webdriver.PhantomJS(executable_path='/home/student/Desktop/phantomjs/bin/phantomjs', service_args = ['--ignore-ssl-errors=true'])
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
        
        if self.quarter == []:
            self.quarter = ''

        self.browser.find_element_by_xpath('//*[@title="Manage Chalk Course List Module Settings"]').click()
        for course_web_element in \
            self.browser.find_elements_by_tag_name('strong'):

            all_courses.append(course_web_element.text[20:])

            if self.quarter != '':
                for quarter in self.quarter:

                    if '({:} '.format(quarter.lower()) + '{:})'.format(self.year)[2:] \
                        in course_web_element.text.lower(): 


                        if 'Unavailable' not in course_web_element.text:
                            courses.append(course_web_element.text[20:])
                            course_name_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Course Name"]')
                            course_name_box.click()
                            course_id_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Course ID"]')
                            course_id_box.click()
                            course_instructor_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Instructors"]')
                            course_instructor_box.click()

            else:
                if '{:})'.format(str(self.year)[2:]) in \
                    course_web_element.text.lower(): 

                    if 'Unavailable' not in course_web_element.text:
                        courses.append(course_web_element.text[20:])
                        course_name_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Course Name"]')
                        course_name_box.click()
                        course_id_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Course ID"]')
                        course_id_box.click()
                        course_instructor_box = self.browser.find_element_by_xpath('//*[@title="{:}'.format(course_web_element.text) + ': Instructors"]')
                        course_instructor_box.click()


        course_form = self.browser.find_element_by_id('moduleEditForm')
        course_form.submit()

        return all_courses, courses


    def access_courses(self, list_of_courses):
        self.course_material_dict[self.username] = {}
        
        for course in list_of_courses: 
            course_list = [course]
            self.course_material_dict[self.username][check_folder_name(course)] = {}
            material_dict = self.course_material_dict[self.username][check_folder_name(course)]
            for course_link in self.browser.find_element_by_id('div_25_1').find_elements_by_tag_name('li'):
                if course in course_link.text:
                    professor = course_link.find_element_by_class_name('name').text
                    prof_cnt = professor.count(';')
                    course_list.append(professor.split('; ')[:prof_cnt])

            self.build_course_dict(self.course_info, material_dict, professor, course, course_list) 

        return None


    def build_course_dict(self, course_info, material_dict, professor, course, course_list):

        self.browser.find_element_by_partial_link_text(course).click()
        
        for item_index in range(len(self.browser.find_element_by_id('courseMenuPalette_contents').find_elements_by_tag_name('li'))):
            item = self.browser.find_element_by_id('courseMenuPalette_contents').find_elements_by_tag_name('li')[item_index]

            if item.text == 'Announcements':
                material_dict[item.text] = {}
                make_dirs(self.course_material_dict, self.default_folder)  

                item.find_element_by_tag_name('a').click()              
                if self.check_id_exists('content_listContainer'): 

                    content_list_container = self.browser.find_element_by_id('content_listContainer')
                    announcement_text = ''

                    for file_or_folder in content_list_container.find_elements_by_tag_name('li'):
                        announcement_text += file_or_folder.text + '\n\n' 

                else:
                    content = self.browser.find_element_by_id('content')
                    if self.check_id_exists('announcementList'):
                        announcement_text = content.find_element_by_id('announcementList').text
                    else:
                        announcement_text = ''
                self.download_text('Announcements', announcement_text, '{:}/{:}/{:}/Announcements/'.format(self.default_folder, self.username, str(check_folder_name(course))))

            elif item.text == 'Send Email':
                list_of_tas = []
                list_of_students = []
                item.find_element_by_tag_name('a').click()
                
                self.browser.find_element_by_link_text('All Teaching Assistant Users').click()
                
                if not self.check_id_exists('inlineReceipt_bad'):
                    list_of_tas = self.browser.find_element_by_id('stepcontent1').find_elements_by_tag_name('li')[0].text[3:].split('; ')
                course_list.append(list_of_tas)
                self.browser.execute_script("window.history.go(-1)")
                
                if self.check_link_text_exists('Select Users'):
                    self.browser.find_element_by_link_text('Select Users').click()
                    list_of_students_web_elements = self.browser.find_element_by_id('stepcontent1').find_element_by_name('USERS_AVAIL').find_elements_by_tag_name('option')
                    prof_cnt = professor.count(';')
                    for student_web_element in list_of_students_web_elements:
                        for professor in professor.split('; ')[:prof_cnt]:
                            prof_str = professor.split(' ')[1] + ', ' + professor.split(' ')[0]
                            if student_web_element.text not in prof_str and student_web_element.text not in list_of_tas and 'PreviewUser' not in student_web_element.text:
                                list_of_students.append(student_web_element.text)
                    self.browser.execute_script("window.history.go(-1)")
                course_list.append(list_of_students)
                self.course_info.append(course_list)


            elif item.text not in ['Home', 'Announcements', 'Send Email', \
                'My Grades', 'Discussion Board', 'Discussions', \
                'Library Course Reserves', 'Tools', 'Groups']:

                component = check_folder_name(item.text)
                material_dict[component] = {}
                make_dirs(self.course_material_dict, self.default_folder)
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
                                    folder_name = check_folder_name(unit.find_element_by_tag_name('a').text)
                                    material_dict[component][folder_name] = {}
                                    make_dirs(self.course_material_dict, self.default_folder)
                                    self.gen_folder(unit, '{:}/{:}/{:}'.format(check_folder_name(course), component, folder_name), material_dict[component][folder_name], course)
                                
                                elif 'file_on' in img.get_attribute('src'):
                                    unit_name = unit.find_element_by_tag_name('a').text
                                    file_url = unit.find_element_by_tag_name('a').get_attribute('href')
                                    heading = unit.find_element_by_tag_name('h3').text
                                    file_dict = {'course': course, 'heading': heading, 'description': ''}
                                    self.download_file_or_doc(unit_name, file_url, unit, check_folder_name(course) + '/' + component, file_dict)
                                    self.file_list.append(file_dict)

                                elif 'document_on' in img.get_attribute('src'):
                                    if self.check_tag_exists_in_web_element(unit, 'a'):
                                        for download_file in unit.find_elements_by_tag_name('a'):                                             
                                            unit_name = download_file.text
                                            file_url = download_file.get_attribute('href')
                                            heading = unit.find_element_by_tag_name('h3').text
                                            description = ''
                                            for paragraph in unit.find_elements_by_tag_name('p'):
                                                description += paragraph.text + '\n'
                                            file_dict = {'course': course, 'heading': heading, 'description': description}
                                            self.download_file_or_doc(unit_name, file_url, download_file, check_folder_name(course) + '/' + component, file_dict)      
                                            self.file_list.append(file_dict)
                    
                    if material_dict[component] == {}:
                        del material_dict[component]

                    make_dirs(self.course_material_dict, self.default_folder)

                            # download href for all links;
                            # download text for all units 

        self.browser.find_element_by_id('My Chalk').find_element_by_tag_name('a').click()

  
        return material_dict


    def gen_folder(self, unit, path, folder_dict, course): 
        unit.find_element_by_tag_name('a').click() 
        if self.check_id_exists('content_listContainer'):
            num_of_items = len(self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li'))
            for unit_index in range(num_of_items):
                inner_unit = self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li')[unit_index]
                if self.check_tag_exists_in_web_element(inner_unit, 'img'):
                    img = inner_unit.find_element_by_tag_name('img')
                    if img.get_attribute('class') == 'item_icon':
                        if 'folder_on' in img.get_attribute('src'):
                            folder_name = check_folder_name(inner_unit.find_element_by_tag_name('a').text)
                            folder_dict[folder_name] = {}
                            make_dirs(self.course_material_dict, self.default_folder)
                            self.gen_folder(inner_unit, path + '/{:}'.format(folder_name), folder_dict[folder_name])


                        elif 'file_on' in img.get_attribute('src'):
                            unit_name = inner_unit.find_element_by_tag_name('a').text
                            file_url = inner_unit.find_element_by_tag_name('a').get_attribute('href')
                            heading = inner_unit.find_element_by_tag_name('h3').text
                            file_dict = {'course': course, 'heading': heading, 'description': ''}
                            self.download_file_or_doc(unit_name, file_url, inner_unit, path, file_dict)
                            self.file_list.append(file_dict)
                        

                        elif 'document_on' in img.get_attribute('src'):
                            if self.check_tag_exists_in_web_element(inner_unit, 'a'):
                                for download_file in inner_unit.find_elements_by_tag_name('a'):
                                    unit_name = download_file.text
                                    file_url = download_file.get_attribute('href')
                                    heading = inner_unit.find_element_by_tag_name('h3').text
                                    description = ''
                                    for paragraph in inner_unit.find_elements_by_tag_name('p'):
                                        description += paragraph.text + '\n'
                                    file_dict = {'course': course, 'heading': heading, 'description': description}
                                    self.download_file_or_doc(unit_name, file_url, download_file, path, file_dict)
                                    self.file_list.append(file_dict)


                        # download text for all
        self.browser.execute_script("window.history.go(-1)")

        return None


    def download_text(self, filename, text, path):

        if os.path.exists(path + filename + '.txt'):
            print('File already exists. Updating file.')
            os.remove(path + filename + '.txt')

        with open(path + filename + '.txt', 'w') as f:
            f.write(text)


    def download_file_or_doc(self, unit_name, file_url, unit, path, file_dict):
        
        s = requests.session()
        s.get(file_url, auth = (self.username, self.password))
        r = s.get(file_url, stream = True, auth = (self.username, self.password))  
        file_dict['format'] = r.headers.get('content-type')
        destination = '{:}/{:}/{:}/{:}'.format(self.default_folder, self.username, path, unit_name)
        file_dict['path'] = os.path.abspath(destination)
        with open(destination, 'wb') as f:  
            r.raw.decode_content = True
            f.write(r.content)
        if 'pdf' in file_dict['path']:
            file_dict['body'] = convert_pdf(file_dict['path'])
        elif 'txt' in file_dict['path']:
            file_dict['body'] = r.content
        else:
            file_dict['body'] = ''
        
    

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







